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

def adhoc_fetch(title,page,limit=10,tgtdir=os.getcwd(),debug=False) :
    def random_useragent() :
        ntvers = ["9.0","10.0","8.0"]
        os = [ "Windows NT "+str(v) for v in ntvers ] + ["Macintosh"] * 3
        firevers  = [str(i)+".0" for i in range(42,51)]
        o = random.choice(os)
        f = random.choice(firevers)
        return "Mozilla/5.0 ({0}; Win64; x64; rv:{1}) Gecko/20100101 Firefox/{1}".format(o,f)
    ss = requests.Session()
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
    try :
        user_agent = {'User-Agent': random_useragent()}
        if debug :
            print("# {}".format(page),file=sys.stderr,flush=True)
            print("# {}".format(user_agent),file=sys.stderr,flush=True)
        rsp = ss.get(page,headers=user_agent,timeout=20,verify=False)
    except :
        print("# {}".format(traceback.format_exc().splitlines()[-1]),file=sys.stderr,flush=True)
        return
    rsp.encoding = rsp.apparent_encoding
    rtext = rsp.text
    if debug :
        print(rtext)
    chapters = list()
    for m in re.findall(r"(<dd>|<li>)\s*<a\s+href=\"(\S*?\d+\.(htm|html))\"\s*>\s*(.*?)\s*</a>",rtext,re.DOTALL) :
        url=m[1].split("/")[-1]
        chapter=m[3]
        chapters.append((url,chapter))
    def cid(c) :
        s = c[0]
        if not s :
            return 2**31
        s = re.sub(r"(\.html|\.htm)",'',s)
        m = re.search(r"(\d+)",s)
        if m :
            return int(m.group(1))
        else :
            return 2**31
    chapters = sorted(list(set(chapters)),key=cid)
    if debug :
        print(chapters)
    report=""
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
        try :
            user_agent = {'User-Agent': random_useragent()}
            if debug :
                print("# {}".format(url),file=sys.stderr,flush=True)
                print("# {}".format(user_agent),file=sys.stderr,flush=True)
            rsp = ss.get(url,headers=user_agent,timeout=20,verify=False)
        except :
           print("# {}".format(traceback.format_exc().splitlines()[-1]),file=sys.stderr,flush=True)
           break
        rsp.encoding = rsp.apparent_encoding
        m = re.search(r"<div (class|id)=\"content\".*?>(.*?)</div>",rsp.text,re.DOTALL)
        context = ""
        if m :
            context = m.group(2).replace("<br/>","</br>\n")
            context = m.group(2).replace("<br/>","<br/>\n")
        else :
            lines = [ln for ln in rsp.text.splitlines()]
            started = False
            for _, ln in enumerate(lines) :
                if re.search(r"<\/*br\s*\/*>",ln) :
                    started = True
                    context += ln
                if started and re.search(r"</div>",ln)  :
                    break
                if started :
                    context += ln
        if len(context) < 200 :
            print("# context length abnormal. most likely hit with rate limiter", file=sys.stderr, flush=True)
            break
        if not re.search(r"<br/>\s*</br>",context,re.DOTALL) :
            context = context.replace("<br/>","</br></br>")
        if not re.search(r"<br/>\s*<br/>",context,re.DOTALL) :
            context = context.replace("<br/>","<br/><br/>")
        if ix == 0 :
            prevpg = "index.html"
            cdone += 1 
        else :
            prevpg = chapters[ix-1][0]
        if ix == len(chapters)-1 :
            nextpg = "index.html"
        else :
            nextpg = chapters[ix+1][0]
        rtext = "<html>\n"
        rtext += "<head>\n"
        rtext += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        rtext += '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>' + "\n"
        rtext += "<title>{}</title>\n".format(title+":"+chapter)
        ps = """<script type="text/javascript"> var preview_page = "prevpg"; var next_page = "nextpg"; var index_page = "index.html"; function jumpPage() { if (event.keyCode==37) location=preview_page; if (event.keyCode==39) location=next_page; if (event.keyCode==13) location=index_page; } document.onkeydown=jumpPage; </script> </head>\n"""
        rtext += ps.replace("prevpg",prevpg).replace("nextpg",nextpg)
        rtext += "</head>\n"
        rtext += "<body style=\"background-color: #EAF2F8;color: #000000;\">\n"
        rtext += "<a href=\"index.html\">INDEX of {}</a>\n".format(title)
        rtext += "<br/>\n"*2
        rtext += "<a href=\"{}\">PREV CHAPTER</a>\n".format(prevpg)
        rtext += "<br/>\n"*2
        rtext += "<a href=\"{}\">NEXT CHAPTER</a><br/>\n".format(nextpg)
        rtext += "<h3>{}</h3>".format(title) + "\n"
        rtext += "<h4>{}</h4>".format(chapter) + "\n"
        rtext += "<br/>\n"
        rtext += context + "\n"
        rtext += "<br/></br>\n"
        rtext += "<a href=\"{}\">PREV CHAPTER</a>\n".format(prevpg)
        rtext += "<br/>\n"*2
        rtext += "<a href=\"{}\">NEXT CHAPTER</a><br/>\n".format(nextpg)
        rtext += "<br/>\n"*2
        rtext += "<a href=\"index.html\">INDEX of {}</a>\n".format(title)
        rtext += "<br/>\n"*2
        rtext += "<a href=\"{}\">ORIGIN_SOURCE</a><br/>\n".format(url)
        rtext += "<br/>\n"*2
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
                if not report :
                    report += "{} :   {} ".format(title,chapter)
                else :
                    report += ", {}".format(chapter)
            downloaded.add(cname)
        cdone+=1
        time.sleep(float(random.choice([i for i in range(30)])/10.0))
    report = report.rstrip(",")
    print("# updates : {}".format(report), file=sys.stderr, flush=True)
    return report


def batch_fetch(cfgfile,debug=False) :
    report = ""
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
                    time.sleep(20+random.choice([i for i in range(60)]))
                title = m.group(1)
                tgtdir = m.group(2)
                page = m.group(3)
                print(title,"@", tgtdir, "from", page, file=sys.stderr, flush=True)
                try :
                    report += adhoc_fetch(title,page,10,tgtdir,debug) + "\n"
                except :
                    traceback.print_exc()
    return report

def novels_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--cfgfile", dest="cfgfile", default="~/.novels/novel.conf", help="input file")
    parser.add_argument("-t", "--title", dest="title", default=None, help="novel title")
    parser.add_argument("-n", "--number", dest="number", type=int, default=10, help="how many chapters to retrieve")
    parser.add_argument("-p", "--page", dest="page", default=None, help="Novel index page",)
    parser.add_argument("-d", "--dir", dest="dir", default=os.getcwd(), help="where to store books",)
    parser.add_argument("-X", "--debug", dest="debug", action="count", default=False, help="debug mode",)
    args = parser.parse_args()

    if args.title :
        adhoc_fetch(args.title,args.page,args.number,args.dir,args.debug)
        return
    args.cfgfile = os.path.expanduser(args.cfgfile)
    if os.path.isfile(args.cfgfile) :
        report = batch_fetch(args.cfgfile,debug=args.debug)
        print("# Summary :\n" + report)
    else :
        if not os.path.isdir(os.path.expanduser("~/.novels")) :
            os.mkdir(os.path.expanduser("~/.novels"))
        with open(args.cfgfile,"w") as f :
            f.write("#title,bookpage\n")


if __name__ == "__main__" :
    novels_main()
