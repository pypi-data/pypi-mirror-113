import sys
import argparse
import os
import requests
import json
import yaml
import re
import traceback
import time
import random
import string
from collections import (deque,defaultdict)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def adhoc_fetch(title,page,limit,tgtdir,debug=False) :
    tgtdir = os.path.expanduser(tgtdir)
    if not os.path.isdir(tgtdir) :
        print("# tgtdir {} is missing.".format(tgtdir),file=sys.stderr,flush=True)
    if not os.path.isdir(os.path.join(tgtdir,title)) :
        os.mkdir(os.path.join(tgtdir,title))
        with open(os.path.join(tgtdir,title,"index.html"),"w") as f :
            header = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>book_title</title>
<body style="background-color: #EAF2F8;color: #000000;">
<table style="border-collapse:collapse">
"""
            f.write(header.replace("book_title",title))
        with open(os.path.join(tgtdir,title, "downloaded.txt"),"w") as f :
            pass
    downloded = set()
    last = ""
    if os.path.isfile(os.path.join(tgtdir,title, "downloaded.txt")) :
        with open(os.path.join(tgtdir,title, "downloaded.txt"),"r") as f :
            downloaded = set([ln.rstrip() for ln in f.readlines()])
            if downloaded :
                last = max(downloaded)
    rsp = requests.get(page,timeout=10,verify=False)
    rsp.encoding = rsp.apparent_encoding
    rtext = rsp.text
    chapters = list()
    for m in re.findall(r"(<dd>|<li>)\s*<a\s+href=\"(\S*\d+\.(htm|html))\"\s*>\s*(.*?)\s*</a>",rtext,re.DOTALL) :
        url=m[1]
        chapter=m[3]
        chapters.append((url,chapter))
    chapters = sorted(list(set(chapters)))
    if debug :
        print(chapters)
    cdone=0
    for ix, m in enumerate(chapters) :
        if cdone > limit :
            break
        url=m[0]
        cname = url
        # redownload the last chapter to fix the prev/next link
        if cname and cname < last :
            continue
        if not url.startswith("http") :
            url = page.rstrip("/") + "/" + url
        chapter=m[1]
        print("{:60}  ({})".format(url,chapter),file=sys.stderr,flush=True)
        rsp = requests.get(url,timeout=10,verify=False)
        rsp.encoding = rsp.apparent_encoding
        m = re.search(r"<div id=\"content\">(.*?)</div>",rsp.text,re.DOTALL)
        context = ""
        if m :
            context = m.group(1).replace("</br>","</br>\n\n")
        else :
            print("# cannot find content", file=sys.stderr, flush=True)
            break
        if len(context) < 200 :
            print("# context length abnormal. most likely hit with rate limiter", file=sys.stderr, flush=True)
            break
        if ix == 0 :
            prevpg = "index.html"
        else :
            prevpg = chapters[ix-1][0]
        if ix == len(chapters)-1 :
            nextpg = "index.html"
        else :
            nextpg = chapters[ix+1][0]
        rtext = "<html>\n"
        rtext = "<head>\n"
        rtext += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        rtext += '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>' + "\n"
        rtext += "<title>{}</title>\n".format(title+":"+chapter)
        ps = """<script type="text/javascript"> var preview_page = "prevpg"; var next_page = "nextpg"; var index_page = "index.html"; function jumpPage() { if (event.keyCode==37) location=preview_page; if (event.keyCode==39) location=next_page; if (event.keyCode==13) location=index_page; } document.onkeydown=jumpPage; </script> </head>\n"""
        rtext = "</head>\n"
        rtext += "<body style=\"background-color: #EAF2F8;color: #000000;\">\n"
        rtext += ps.replace("prevpg",prevpg).replace("nextpg",nextpg)
        rtext += "<a href=\"{}\">PREV CHAPTER</a>\n".format(prevpg)
        rtext += "&nbsp;"*10
        rtext += "<a href=\"{}\">NEXT CHAPTER</a></br>\n".format(nextpg)
        rtext += "</br></br>\n"
        rtext += context + "\n"
        rtext += "</br></br>\n"
        rtext += "<a href=\"{}\">PREV CHAPTER</a>\n".format(prevpg)
        rtext += "&nbsp;"*10
        rtext += "<a href=\"{}\">NEXT CHAPTER</a></br></br>\n".format(nextpg)
        rtext += "<a href=\"{}\">orignal link</a></br>\n".format(url)
        rtext += "</body>\n"
        rtext += "</html>\n"
        with open(os.path.join(tgtdir,title, cname),"w") as f :
            f.write(rtext)
        with open(os.path.join(tgtdir,title, "downloaded.txt"),"a") as f :
            f.write(cname+"\n")
        if cname not in downloaded :
            with open(os.path.join(tgtdir,title, "index.html"),"a") as f :
                hcontent = "<tr><td><a href=\"{}\">{}</a></td></tr>".format(cname,chapter) + "\n"
                f.write(hcontent)
            downloaded.add(cname)
        cdone+=1
        time.sleep(1)


def batch_fetch(cfgfile,debug=False) :
    with open(cfgfile,"r") as f :
        for ln in f.readlines() :
            if ln.startswith("#") :
                continue
            m = re.search(r"(\S+?),(\S+?),(\S+)",ln)
            thefirst = True
            if m :
                if not thefirst :
                    print("# delay 30s", file=sys.stderr, flush=True)
                    thefirst = False
                    time.sleep(30)
                title = m.group(1)
                tgtdir = m.group(2)
                page = m.group(3)
                print(title,"@", tgtdir, "from", page, file=sys.stderr, flush=True)
                try :
                    adhoc_fetch(title,page,30,tgtdir,debug)
                except :
                    traceback.print_exc()

def novels_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--cfgfile", dest="cfgfile", default="~/.novels/novel.conf", help="input file")
    parser.add_argument("-t", "--title", dest="title", default=None, help="novel title")
    parser.add_argument("-n", "--number", dest="number", type=int, default=30, help="how many chapters to retrieve")
    parser.add_argument("-p", "--page", dest="page", default=None, help="Novel index page",)
    parser.add_argument("-d", "--dir", dest="dir", default=os.getcwd(), help="where to store books",)
    parser.add_argument("-X", "--debug", dest="debug", action="count", default=False, help="debug mode",)
    args = parser.parse_args()

    if args.title :
        adhoc_fetch(args.title,args.page,args.number,args.dir,args.debug)
        return
    args.cfgfile = os.path.expanduser(args.cfgfile)
    if os.path.isfile(args.cfgfile) :
        batch_fetch(args.cfgfile,debug=args.debug)
    else :
        if not os.path.isdir(os.path.expanduser("~/.novels")) :
            os.mkdir(os.path.expanduser("~/.novels"))
        with open(args.cfgfile,"w") as f :
            f.write("#title,bookpage\n")


if __name__ == "__main__" :
    novels_main()
