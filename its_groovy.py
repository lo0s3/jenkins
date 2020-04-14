#!/usr/bin/python3

import os, sys, argparse, requests, gevent.monkey
from lxml.html import fromstring
from gevent.pool import Pool
gevent.monkey.patch_socket()
requests.packages.urllib3.disable_warnings()

parser = argparse.ArgumentParser(description="Multithreaded stuff")
parser.add_argument('-i', dest='infile', required=True, metavar="FILE")
#parser.add_argument('-o', dest='outdir', required=False, metavar="FILE", type=str, default="output")
parser.add_argument('-t', dest="threads", required=False, type=int, default=16)

args = parser.parse_args()


def check_urls(urls, threads):
    def fetch(url):
        try:
            response = requests.request("GET", "http://" + url + ":8080/script", timeout=4, verify=False)
            #print("[*] Querying: " + "http://" + url + ":8080/script")
            data = fromstring(response.content)
            title = data.findtext('.//title')
            service = str(title)

            # <title> is jenkins
            if service == 'Jenkins':
                print("[*] Found " + service + " at: " + url)
            #with open(outdir + "/" + url, "w+") as fp:
            #    fp.write(response.text.encode("utf-8"))

        except Exception as e:
            print("[!] Exception:\n")
            print(e)
            pass

    N = len(urls)
    pool = Pool(nthreads)
    for index, url in enumerate(urls):
        #print(url)
        pool.spawn(fetch, url)
    pool.join()


#def check_dir(outdir):
    #if not os.path.isdir(outdir):
        #os.mkdir(outdir)


if __name__ == "__main__":
    filename = args.infile
    #outdir   = args.outdir
    nthreads = args.threads

    #check_dir(outdir)
    ips = [line.strip() for line in open(filename, ).readlines()]
    check_urls(ips, nthreads)
