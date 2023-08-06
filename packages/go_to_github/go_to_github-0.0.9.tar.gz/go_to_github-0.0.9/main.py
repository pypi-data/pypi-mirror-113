import os
import sys
import glob
import shutil
import filecmp
from pathlib import Path
import requests
from lxml import etree
from fake_user_agent.main import user_agent
import settings


ua = user_agent()
headers = {"User-Agent": ua}


def fetch(url, proxies=None):
    try:
        with requests.get(url, headers=headers, proxies=proxies) as r:
            r.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        print(
            f"Connection rejected to <{url}>.\nReason: <{repr(e)}>.\nWill retry once.\n"
        )
    except requests.exceptions.ConnectTimeout:
        print(f"Connection to <{url}> timed out. Will retry  once.\n")
    except requests.exceptions.ReadTimeout:
        print(f"Read from <{url}> timed out. Will retry once.\n")
    except Exception as e:
        print(f"{repr(e)} when fetching <{url}>. Will retry once.\n")
    else:
        return r


def parse(response):
    lxml_element = etree.HTML(response)
    ip_address = lxml_element.xpath(
        "/html/body/div/main/section[2]/table/tbody/tr[9]/td/div/a/text()"
    )
    return ip_address[0]


def read_and_write(parsed_ip):
    if os.access(settings.HOSTS_PATH, os.W_OK):
        with open(settings.HOSTS_PATH, "r+") as f:
            hosts_data = f.readlines()
            for index, line in enumerate(hosts_data):
                host_list = line.strip().split()
                if host_list:
                    if (
                        host_list[-1] == settings.GITHUB_HOST_NAME
                        and host_list[0] != parsed_ip
                    ):
                        hosts_data.remove(line)
                    elif (
                        host_list[-1] == settings.GLOBAL_HOST_NAME
                        and host_list[0]
                        != settings.CONFIG_DICT[settings.GLOBAL_HOST_NAME]
                    ):
                        hosts_data.remove(line)

                    elif (host_list[-1] == settings.CDN_HOST_NAME) and (
                        host_list[0] not in settings.CONFIG_DICT[settings.CDN_HOST_NAME]
                    ):
                        hosts_data.remove(line)
                    else:
                        hosts_data[index] = " ".join(host_list)
                else:
                    hosts_data.remove(line)
            github_line = str(parsed_ip) + " " + settings.GITHUB_HOST_NAME
            config = settings.CONFIG_LIST
            config.append(github_line)
            for line in config:
                if line not in hosts_data:
                    hosts_data.append(line)
            f.seek(0)
            for line in hosts_data:
                f.writelines(line + "\n")
            f.truncate()
    else:
        print(
            "You aren't permitted to writing hosts file. Please switch to root user and retry.\n"
        )
        sys.exit()


def get_hosts_githubip():
    hosts_github_ip = ""
    with open(settings.HOSTS_PATH, "r") as f:
        for line in f:
            if line.strip().split(" ")[-1] == settings.GITHUB_HOST_NAME:
                hosts_github_ip = line.strip().split(" ")[0]
    return hosts_github_ip


def backup():
    if not glob.glob(str(settings.LOCAL_DIR)):
        settings.LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    if not filecmp.cmp(settings.HOSTS_PATH, settings.BACKUP_FILE):
        shutil.copy2(settings.HOSTS_PATH, settings.BACKUP_FILE)
        print(
            f"hosts file[{settings.HOSTS_PATH}] has been backuped in [{settings.LOCAL_DIR}].\n"
        )


def restore_backup():
    shutil.copy2(settings.BACKUP_FILE, settings.HOSTS_PATH)
    print(f"[{settings.HOSTS_PATH}] has been restored to the original version.\n")


def test_url(url, proxies=None):
    attempt = 0
    while True:
        if attempt == 2:
            return False

        r = fetch(url, proxies=proxies)
        attempt += 1

        if r and r.status_code < 400:
            return True


def get_server_ip(url, proxies=None):
    try:
        with requests.get(url, headers=headers, stream=True, proxies=proxies) as r:
            r.raise_for_status()
            # NOTE `stream=True`, outside context manager, r is Nonetype
            ip, port = r.raw.connection.sock.getpeername()
    except requests.exceptions.ConnectionError:
        print(f"Connection rejected to <{url}>.\n")
    except requests.exceptions.ConnectTimeout:
        print(f"Connection to <{url}> timed out.\n")
    except requests.exceptions.ReadTimeout:
        print(f"Read from <{url}> timed out.\n")
    except Exception as e:
        print(f"{repr(e)} when fetching <{url}>.\n")
    else:
        return ip


def main():
    print(f"Testing <{settings.GITHUB_URL}> reachability...\n")
    is_reachable = test_url(settings.GITHUB_URL)
    if is_reachable:
        print("You are good to go!\n")
        sys.exit()
    else:
        print("You can not reach Github.The program is starting to nail it...\n")
        res = fetch(settings.URL)
        if res and res.status_code < 400:
            parsed_ip = parse(res.text)
            backup()
            read_and_write(parsed_ip)
            is_reachable = test_url(settings.GITHUB_URL)
            if is_reachable:
                print("Problem has been fixed. Now, you are good to go!\n")
                sys.exit()
            else:
                server_ip = get_server_ip(settings.GITHUB_URL)
                print(f"Github server IP is <{server_ip}>")
                hosts_github_ip = get_hosts_githubip()
                print(f"Github parsed IP is <{parsed_ip}>.")
                print(f"Github hosts IP is <{hosts_github_ip}>.\n")
                if parsed_ip == hosts_github_ip:
                    print("Github is slow to respond. Try again.\n")
                else:
                    print("Something went wrong. Try again.\n")
                    restore_backup()
                sys.exit()
        else:
            sys.exit()
