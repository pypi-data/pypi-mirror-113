import subprocess
import requests
import json
import re
import os
import shutil
import sys

regex_href = r"href=\"([^\"]+)\""


def pack(pakname, target_dir):
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    output = subprocess.check_output(
        f'pipdeptree -p={pakname} -j').decode('utf-8')
    deps = json.loads(output)
    for dep in deps:
        pname = dep['package']['package_name']
        pver = dep['package']['installed_version']
        resp = requests.get(f'https://mirrors.aliyun.com/pypi/simple/{pname}/')
        lines = resp.text.splitlines()
        for line in lines:
            if f'-{pver}.tar.gz' in line:
                print(f'download {pname}=={pver} ...')
                match = re.search(regex_href, line)
                url = f'https://mirrors.aliyun.com/pypi{match.group(1)[5:]}'
                download_tar(url, os.path.join(
                    target_dir, f'{pname}-{pver}.tar.gz'))
                break


def download_tar(url, filename):
    print(url)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)


pack(sys.argv[1], sys.argv[2])

