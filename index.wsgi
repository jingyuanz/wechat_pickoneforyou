#coding=utf-8
import sae
from wechat import wsgi

application = sae.create_wsgi_app(wsgi.application)