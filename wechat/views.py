#coding=utf-8
__author__ = 'zhangjingyuan'
import hashlib
import json
from lxml import etree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context,Template,loader
import time
from random import choice
TOKEN = 'jingyuanz'

@csrf_exempt
def wechat(request):
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr, content_type="text/plain")
        else:
            return ""
    elif request.method == "POST":
        xml_str = smart_str(request.body)
        request_xml = etree.fromstring(xml_str)
        response_xml = parse_message(request_xml)
        return HttpResponse(response_xml, content_type="application/xml")


def parse_message(request_xml):
    # t = loader.get_template('reply_text.xml')
    content=request_xml.find("Content").text
    msgType=request_xml.find("MsgType").text
    fromUser=request_xml.find("FromUserName").text
    toUser=request_xml.find("ToUserName").text
    parsed_content = parse_content(content)
    reply = """<xml>
                <ToUserName><![CDATA[{}]]></ToUserName>
                <FromUserName><![CDATA[{}]]></FromUserName>
                <CreateTime>{}</CreateTime>
                <MsgType><![CDATA[{}]]></MsgType>
                <Content><![CDATA[{}]]></Content></xml>"""\
        .format(fromUser, toUser, str(int(time.time())), msgType, parsed_content)
    return reply


def parse_content(content):
    if content == u"格式":
        return "A,B,C,D?X,Y,Z\nA,B,C,D代表选项, XYZ代表关键词/关键句或条件,用逗号隔开,并在两组间用问号隔开,\n比如 香蕉,火锅,中药?好吃,不上火\n就能得到科学选择"
    content = content.split('?')
    if len(content) != 2:
        return "格式错误, 发送'格式'获取帮助"
    else:
        choices = content[0].split(',')
        str_choices = str(choices).replace('u\'','\'')
        str_choices = str_choices.decode("unicode-escape")
        key_words = content[1].split(',')
        if len(choices) <= 1 or len(key_words) <= 1:
            return "格式错误, 发送'格式'获取帮助"
        else:
            return str_choices
