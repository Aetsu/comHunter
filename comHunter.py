#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# by @aetsu
import re
import time
import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataBase import Url, Webpage, Base, Comment_html, Comment_js, Comment_css
from html import *


def getUrls(tarurl, session):
    urls = {}

    print (" [+] Finding urls....")
    url = requests.get(tarurl)
    urls[str(tarurl)] = ''
    for u in re.findall('''href=["'](.[^"']+)["']''', url.text, re.I):
        try:
            if u[:4] == "http":
                if tarurl in u:
                    urls[str(u)] = ''
            elif u[0] == "/":
                combline = tarurl + u
                urls[str(combline)] = ''
            else:
                combline = tarurl + '/' + u
                urls[str(combline)] = ''
        except:
            pass

    for k, v in urls.iteritems():
        r = requests.get(k)
        new_url = Url(urlName=k, code=r.status_code)
        session.add(new_url)
        new_content = Webpage(url=new_url, content=r.text)
        session.add(new_content)

        print (" [+] Searching " + k)

        print ("    [-] Searching html comments")
        if k[-4:] != ".css" and k[-3:] != ".js":
            html_c = re.findall('<!--(.*)-->', r.text)
            for comment in html_c:
                new_comment = Comment_html(url=new_url, html_comment=comment)
                session.add(new_comment)

        print ("    [-] Searching css comments")
        css_t = re.findall('<style>[\s\S]*</style>', r.text)

        if k[-4:] == ".css":
            css_c = re.findall('(?s)/\*.*?\*/', r.text)
            for comment in css_c:
                new_comment = Comment_css(url=new_url, css_comment=comment)
                session.add(new_comment)
        elif len(css_t) > 0:
            for c in css_t:
                css_c = re.findall('(?s)/\*.*?\*/', c)
                for comment in css_c:
                    new_comment = Comment_css(url=new_url, css_comment=comment)
                    session.add(new_comment)

        print ("    [-] Searching js comments")
        script_t = re.findall('<script>[\s\S]*</script>', r.text)
        if k[-3:] == ".js":
            js_c = re.findall('(?s)/\*.*?\*/', r.text)
            for comment in js_c:
                new_comment = Comment_js(url=new_url, js_comment=comment)
                session.add(new_comment)

            js_c = re.findall('(\?!:|.*[ ])//(.*)', r.text)
            for comment in js_c:
                new_comment = Comment_js(url=new_url, js_comment=comment[1])
                session.add(new_comment)
        elif len(script_t) > 0:
            for j in script_t:
                js_c = re.findall('(?s)/\*.*?\*/', j)
                for comment in js_c:
                    new_comment = Comment_js(url=new_url, js_comment=comment)
                    session.add(new_comment)

                js_c = re.findall('(\?!:|.*[ ])//(.*)', j)
                for comment in js_c:
                    new_comment = Comment_js(url=new_url, js_comment=comment[1])
                    session.add(new_comment)

    session.commit()


def main():
    if len(sys.argv) != 2:
        print("usage: %s targeturl" % (sys.argv[0]))
        print("Example: %s http://www.cni.es" % (sys.argv[0]))
        sys.exit(0)

    path = 'session.' + time.ctime().replace(' ', '_')
    dbname = 'session.' + path + '.db'

    if not os.path.exists(path):
        os.mkdir(path)

    liteEng = 'sqlite:///' + path + '/' + dbname
    engine = create_engine(liteEng)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    getUrls(sys.argv[1], session)

    print (" [+] Generating report... ")
    h = Html(sys.argv[1], session)
    h.generateReport(path)
    print ("    [-] Saved in " + path)



if __name__ == "__main__":
    main()
