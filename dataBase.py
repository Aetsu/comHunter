#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# by @aetsu
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Url(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    urlName = Column(String, nullable=False)
    code = Column(Integer, nullable=True)


class Webpage(Base):
    __tablename__ = 'webpage'
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('url.id'))
    url = relationship(Url)
    content = Column(String, nullable=True)


class Comment_html(Base):
    __tablename__ = 'comment_html'
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('url.id'))
    url = relationship(Url)
    html_comment = Column(String, nullable=True)


class Comment_js(Base):
    __tablename__ = 'comment_js'
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('url.id'))
    url = relationship(Url)
    js_comment = Column(String, nullable=True)


class Comment_css(Base):
    __tablename__ = 'comment_css'
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('url.id'))
    url = relationship(Url)
    css_comment = Column(String, nullable=True)


