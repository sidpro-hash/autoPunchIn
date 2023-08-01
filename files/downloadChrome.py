import requests
import json
import detectChrome
from datetime import date
import os
import time
import zipfile, io, shutil



def get_version(version):
    version = version.split(".")
    return "{0}.{1}.{2}".format(version[0],version[1],version[2])

def download(isStable=True):
    URL = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json' if isStable else 'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'
    chromeVersion = detectChrome.get_chrome_version()
    timestamp = str(date.today().strftime('%d/%m/%Y'))
    folder_path = ".\\.wdm\\drivers\\chromedriver\\win32\\{}".format(chromeVersion)
    driver_json = ".\\.wdm\\drivers.json"
    driver_json = os.path.normcase(driver_json)
    folder_path = os.path.normcase(folder_path)

    try:
        os.makedirs(folder_path)
    except OSError as error:
        pass

    binary_path = ".\\.wdm\\drivers\\chromedriver\\win32\\{}\\chromedriver.exe".format(chromeVersion)
    driver_json_data = {
        "timestamp": timestamp,
        "binary_path": binary_path
    }
    chromeVersion_json = {}
    chrome_key = "win32_chromedriver_{0}_for_{1}".format(chromeVersion, chromeVersion)
    chromeVersion_json[chrome_key] = driver_json_data
    json_object = json.dumps(chromeVersion_json, indent=4)

    with open(driver_json, "w") as outfile:
        outfile.write(json_object)

    tries = 3
    chrome_driver_url = ""
    response_API = {}
    for i in range(tries):
        try:
            dest = get_version(chromeVersion)
            response_API = requests.get(URL)
            response_json = response_API.json()
            if isStable:
                channels = response_json["channels"]["Stable"]["downloads"]["chromedriver"]
                for chromeDriver in channels:
                    if chromeDriver["platform"] == "win32":
                        chrome_driver_url = chromeDriver["url"]
            else:    
                versions = response_json["versions"]
                for version in versions:
                    if dest == get_version(version["version"]):
                        for chromeDriver in version["downloads"]["chromedriver"]:
                            if chromeDriver["platform"] == "win32":
                                chrome_driver_url = chromeDriver["url"]
        except requests.exceptions.RequestException as e:
            if i < tries - 1: # i is zero indexed
                print("Getting your files please wait....")
                time.sleep(10)
                continue
            else:
                raise
        break



    r = requests.get(chrome_driver_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(folder_path)


    with z as zip_file:
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue
        
            # copy file (taken from zipfile's extract)
            source = zip_file.open(member)
            target = open(os.path.join(folder_path, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)