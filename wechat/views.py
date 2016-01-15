# -*- coding:utf8 -*-
__author__ = 'zhangjingyuan'
import hashlib
import json
import logging
from lxml import etree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context,Template,loader
import time
import random
from collections import defaultdict
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
            return HttpResponse(echostr, content_type="text/plain")
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
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[%s]]></MsgType>
                <Content><![CDATA[%s]]></Content></xml>"""\
        % (fromUser, toUser, str(int(time.time())), msgType, parsed_content)
    return reply


# def parse_content(content):
#     if content == u"格式":
#         return "A B C D?X Y Z\nA,B,C,D代表选项, XYZ代表关键词/关键句或条件,用空格隔开,并在两组间用问号隔开,\n比如 香蕉 火锅 中药?好吃 不上火\n就能得到科学选择\n(记住问号是半角英文的问号,目前只是随机)"
#     content = content.split('?')
#     if len(content) != 2:
#         return "格式错误, 发送'格式'获取帮助, 记住问号'?'一定要是英文的问号!!"
#     else:
#         choices = content[0].split(' ')
#         key_words = content[1].split(' ')
#         if len(choices) <= 1 or len(key_words) < 1 or key_words == "":
#             return "格式错误, 发送'格式'获取帮助,记住问号'?'一定要是英文的问号!!"
#         else:
#             best_choice = choice(choices)
#             logging.error(best_choice)
#             return best_choice

def parse_content(content):
    if content == u"格式":
        return "A B C D?X Y Z\nA,B,C,D代表选项, XYZ代表关键词/关键句或条件,用空格隔开,并在两组间用问号隔开,\n比如 香蕉 火锅 中药?好吃 不上火\n就能得到科学选择\n(记住问号是半角英文的问号,目前只是随机)"
    content = content.split('?')
    if len(content) != 2:
        return "格式错误, 发送'格式'获取帮助, 记住问号'?'一定要是英文的问号!!"
    else:
        choices = content[0].split(' ')
        key_words = content[1].split(' ')
        if len(choices) <= 1 or len(key_words) < 1 or key_words == "":
            return "格式错误, 发送'格式'获取帮助,记住问号'?'一定要是英文的问号!!"
        else:
            sum = 0
            content_dict = defaultdict(int)
            for item in choices:
                for key in key_words:
                    value = random.randint(0,100)
                    content_dict[item] += value
                    sum += value

            sorted_dict = sorted(content_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

            best_choice = sorted_dict[0][0]
            best_portion = str(1.0*sorted_dict[0][1]/sum*100)

            results = ""
            for tup in sorted_dict:
                results += tup[0] + ":" + str(1.0*tup[1]/sum*100) + "\n"

            results += "综上, 最佳选项是 -- "+best_choice + " "+best_portion
            return results