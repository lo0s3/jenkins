#!/usr/bin/python3

import os, sys, argparse, requests, gevent.monkey
from lxml.html import fromstring
from gevent.pool import Pool
gevent.monkey.patch_socket()
requests.packages.urllib3.disable_warnings()

parser = argparse.ArgumentParser(description="Jenkins Open Auth Script Console Scanner")
parser.add_argument('-i', dest='hosts', required=True, metavar="HOSTNAMES", help="hostname list file")
#parser.add_argument('-o', dest='outdir', required=False, metavar="FILE", type=str, default="output")
parser.add_argument('-t', dest="threads", required=False, type=int, default=16, metavar="THREADS", help="number of threads to use")

args = parser.parse_args()

def check_hosts(hosts, threads):
    def fetch(host):
        try:
            response = requests.request("GET", "http://" + host + ":8080/script", timeout=4, verify=False)
            #print("[*] Querying: " + "http://" + host + ":8080/script")
            data = fromstring(response.content)
            title = data.findtext('.//title')
            service = str(title)

            # <title> is jenkins
            if service == 'Jenkins':
                print("[*] Found " + service + " at: " + host)
            #with open(outdir + "/" + host, "w+") as fp:
            #    fp.write(response.text.encode("utf-8"))

        except Exception as e:
            print("[!] Exception:\n")
            print(e)
            pass

    N = len(hosts)
    pool = Pool(nthreads)
    for index, host in enumerate(hosts):
        #print(host)
        pool.spawn(fetch, host)
    pool.join()

#def check_dir(outdir):
    #if not os.path.isdir(outdir):
        #os.mkdir(outdir)

if __name__ == "__main__":
    filename = args.hosts
    #outdir   = args.outdir
    nthreads = args.threads

    #check_dir(outdir)
    hostnames = [line.strip() for line in open(filename, ).readlines()]
    check_hosts(hostnames, nthreads)
