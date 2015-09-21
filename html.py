#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# by @aetsu
import sys
import requests
from dataBase import Url, Webpage, Base, Comment_html, Comment_js, Comment_css
import codecs

class Html:
    def __init__(self, tarurl, session):
        self.tarurl = tarurl
        self.session = session

    def getHeaders(self):
        r = requests.get(self.tarurl)
        headers = r.headers
        return headers

    def writeHtml(self, filename, content):
        f = codecs.open(filename, "w", "utf-8")
        f.write(content)
        f.close()


    def header(self):
        head = """
        <head>
        <meta charset="UTF-8" />
        <title>ComHunter</title>
        <meta name="viewport" content="width=device-width, initial-
        scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
        </head>
        """
        return head

    def menu(self, part):
        menu = """
        <body>
        <nav class="navbar navbar-inverse navbar-static-top">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <!--<span class="sr-only">Toggle navigation</span>-->
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <span class="navbar-brand">ComHunter</span>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
      """
        if 'index.html' in part:
            menu += """
        <li class="active"><a href="index.html">Summary <span class="sr-only"></span></a></li>
        <li><a href="urls.html">Urls</a></li>
          <li><a href="htmlC.html">HTML comments</a></li>
          <li><a href="jsC.html">JS comments</a></li>
          <li><a href="cssC.html">CSS comments</a></li>
        """
        elif 'urls.html' in part:
            menu += """
        <li><a href="index.html">Summary </a></li>
        <li class="active"><a href="urls.html">Urls<span class="sr-only"></span></a></li>
          <li><a href="htmlC.html">HTML comments</a></li>
          <li><a href="jsC.html">JS comments</a></li>
          <li><a href="cssC.html">CSS comments</a></li>
        """
        elif 'htmlC.html' in part:
            menu += """
        <li><a href="index.html">Summary </a></li>
        <li><a href="urls.html">Urls</a></li>
        <li class="active"><a href="htmlC.html">HTML comments<span class="sr-only"></span></a></li>
        <li><a href="jsC.html">JS comments</a></li>
        <li><a href="cssC.html">CSS comments</a></li>
        """
        elif 'jsC.html' in part:
                        menu += """
        <li><a href="index.html">Summary </a></li>
        <li><a href="urls.html">Urls</a></li>
          <li><a href="htmlC.html">HTML comments</a></li>
          <li class="active"><a href="jsC.html">JS comments<span class="sr-only"></span></a></li>
          <li><a href="cssC.html">CSS comments</a></li>
        """
        elif 'cssC.html' in part:
            menu += """
        <li><a href="index.html">Summary </a></li>
        <li><a href="urls.html">Urls</a></li>
          <li><a href="htmlC.html">HTML comments</a></li>
          <li><a href="jsC.html">JS comments</a></li>
          <li class="active"><a href="cssC.html">CSS comments<span class="sr-only"></span></a></li>
        """
        menu += """
          </ul>
        </div><!-- /.navbar-collapse -->
      </div><!-- /.container-fluid -->
    </nav>
        """
        return menu

    def footer(self):
        footer = """
        <div id="footer">
        <div class="container">
        <div class="text-muted pull-right"><a href="https://twitter.com/aetsu" target="_blank">@Aetsu</a></div>
        </div>
        </div>
                </body>
        """
        return footer

    def summaryBody(self):
        headerElements = self.getHeaders()
        content = """
        <div class="container">
        <div class="page-header"><h1><span class="glyphicon glyphicon-
        home"></span>&nbsp;Target url: <a href=\"""" + \
                  self.tarurl + "\">" + self.tarurl + "</a>" + \
                  """</h1></div>
                  <div class="row">
                  """
        urls = """
            <h3><a href="urls.html">Urls found  <span class="badge">
            """ + str(self.session.query(Webpage).count()) + """ </span> </a></h3>
            <h3><a href="htmlC.html">HTML comments found  <span class="badge"> """ \
               + str(self.session.query(Comment_html).count()) + """</span> </a></h3><h3>
               <a href="jsC.html">JS comments found  <span class="badge">""" \
               + str(self.session.query(Comment_js).count()) + """</span> </a></h3>
            <h3><a href="cssC.html">CSS comments found  <span class="badge">""" \
        + str(self.session.query(Comment_css).count()) + """</span></a></h3><br><br>"""
        headers = """
        <div class="panel panel-info">
        <div class="panel-heading">Headers</div>
        <ul class="list-group">
        """
        for h in headerElements:
            headers = headers + "<li class=\"list-group-item\">" + h + " : " + headerElements[h] + "</li>"

        endh = "</ul></div><br><br>"
        headers = headers + endh

        all = content + urls + headers
        return all

    def urlBody(self):
        content = """
        <div class="container">"""

        urlList = self.session.query(Url).order_by(Url.urlName).all()

        urls = """
        <div class="panel panel-default">
        <div class="panel-heading">Url list:</div>
        <table class="table"><tr><th>#</th><th>Url</th><th>Status code</th>
        """
        for u in range(0, len(urlList)):
            urls = urls + "<tr><td>" + str(u) + "</td><td><a href=\"" + urlList[u].urlName + "\"</a>"  \
                   + urlList[u].urlName + "</td><td>" + str(urlList[u].code) + "</tr>"

        endu = "</table></div><br><br>"
        urls = urls + endu

        all = content + urls
        return all

    def htmlCommentBody(self):
        content = """
        <div class="container">"""

        urlList = self.session.query(Url).order_by(Url.urlName).all()

        urls = ''
        for u in range(0, len(urlList)):
            urls = urls + "<div class=\"panel panel-default\"><div class=\"panel-heading\">" \
                   + urlList[u].urlName + "</div>"
            urls += "<ul class=\"list-group\">"
            commentList = self.session.query(Comment_html).filter(Comment_html.url_id == urlList[u].id).all()
            for c in commentList:
                urls += "<li class=\"list-group-item\">" + c.html_comment + "</li>"
            urls += "</ul></div><br><br>"
        endu = "</div><br><br>"
        urls = urls + endu

        all = content + urls
        return all

    def jsCommentBody(self):
        content = """
        <div class="container">"""

        urlList = self.session.query(Url).order_by(Url.urlName).all()

        urls = ''
        for u in range(0, len(urlList)):
            urls = urls + "<div class=\"panel panel-default\"><div class=\"panel-heading\">" \
                   + urlList[u].urlName + "</div>"
            urls += "<ul class=\"list-group\">"
            commentList = self.session.query(Comment_js).filter(Comment_js.url_id == urlList[u].id).all()
            for c in commentList:
                urls += "<li class=\"list-group-item\">" + c.js_comment + "</li>"
            urls += "</ul></div><br><br>"
        endu = "</div><br><br>"
        urls = urls + endu

        all = content + urls
        return all

    def cssCommentBody(self):
        content = """
        <div class="container">"""

        urlList = self.session.query(Url).order_by(Url.urlName).all()

        urls = ''
        for u in range(0, len(urlList)):
            urls = urls + "<div class=\"panel panel-default\"><div class=\"panel-heading\">" \
                   + urlList[u].urlName + "</div>"
            urls += "<ul class=\"list-group\">"
            commentList = self.session.query(Comment_css).filter(Comment_css.url_id == urlList[u].id).all()
            for c in commentList:
                urls += "<li class=\"list-group-item\">" + c.css_comment + "</li>"
            urls += "</ul></div><br><br>"
        endu = "</div><br><br>"
        urls = urls + endu

        all = content + urls
        return all

    def generateHtml(self, part):
        htmlHead = """
        <!DOCTYPE html>
        <html lang="es">
        """
        htmlBottom = "</html>"
        head = self.header()
        footer = self.footer()

        if 'index.html' in part:
            menu = self.menu(part)
            body = self.summaryBody()
        elif 'urls.html' in part:
            menu = self.menu(part)
            body = self.urlBody()
        elif 'htmlC.html' in part:
            menu = self.menu(part)
            body = self.htmlCommentBody()
        elif 'jsC.html' in part:
            menu = self.menu(part)
            body = self.jsCommentBody()
        elif 'cssC.html' in part:
            menu = self.menu(part)
            body = self.cssCommentBody()

        webpage = htmlHead + head + menu + body + footer + htmlBottom

        self.writeHtml(part, webpage)

    def generateReport(self, path):
        self.generateHtml(path + '/' + 'index.html')
        self.generateHtml(path + '/' + 'urls.html')
        self.generateHtml(path + '/' + 'htmlC.html')
        self.generateHtml(path + '/' + 'jsC.html')
        self.generateHtml(path + '/' + 'cssC.html')
