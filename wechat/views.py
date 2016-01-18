# coding=utf-8
__author__ = 'zhangjingyuan'
import hashlib
import sys
import json
import math
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
import urllib2
import re
import urllib
reload(sys)
TOKEN = 'jingyuanz'
sys.setdefaultencoding('utf8')
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

AND = "AND"
PLUS = '+'
SPACE = ' '
QUOTE = '"'
def parse_content(content):
    if content == u"格式":
        return "A B C D?X Y Z\nABCD代表选项, XYZ代表条件关键词(关键词加强排序准确性),用空格隔开,选项和关键词间用问号隔开,\n比如\n\n 香蕉 火锅?好吃 便宜\n\n(记住问号是半角英文的问号)"
    content = content.strip().split('?')
    if len(content) != 2:
        return "格式错误, 发送'格式'获取帮助, 记住问号'?'一定要是英文的问号!!英文的问号!!英文的问号!!如有任何BUG或疑问请联系微信号minamotokyon"
    else:
        choices = content[0].split(' ')
        key_words = content[1].split(' ')
        choices = [i for i in choices if i != '' and i != ' ']
        key_words = [i for i in key_words if i != '' and i != ' ']
        if len(key_words) == 0:
            key_words.append("好")
        if len(choices) <= 1 or len(key_words) < 1:
            return "格式错误, 发送'格式'获取帮助,记住问号'?'一定要是英文的问号!!英文的问号!!英文的问号!!如有任何BUG或疑问请联系微信号minamotokyon"
        else:
            keys = QUOTE+(QUOTE+AND).join(key_words)+QUOTE
            # logging.error(keys)
            sum = 0
            content_dict = defaultdict(int)
            for item in choices:
                item_all_keys = QUOTE+item+QUOTE+AND+keys
                penalty = math.log(count_search_engine(QUOTE+item+QUOTE))
                starting_value = 1.0*count_search_engine(item_all_keys)/penalty
                content_dict[item] += starting_value
                sum += starting_value
                for key in key_words:
                    value = 1.0*count_search_engine(convert_into_search_query(item, key))/penalty
                    content_dict[item] += value
                    sum += value
            sorted_dict = sorted(content_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
            best_choice = sorted_dict[0][0]
            results = "搜索引擎(百度)对以上选项和各关键词的关联性:\n\n"
            for tup in sorted_dict:
                results += tup[0] + " " + str(round(1.0*tup[1]/sum*100, 2)) + "%\n\n"
            results += "综上, 最佳选项是 -- "+best_choice
            print best_choice
            return results


def count_search_engine(content):
    content = content.encode('utf-8')
    url_address = 'http://www.baidu.com/s?wd={}'.format(urllib.quote(content))
    f = urllib2.urlopen(url_address)
    buf = f.read()
    buf = buf.replace(',', "")
    num = re.findall(r'百度为您找到相关结果约(\d+)个',buf)
    if len(num) == 1:
        return math.log(int(num[0])+2, 1.01)
    return math.log(2, 1.01)


def convert_into_search_query(raw1, raw2):
    return QUOTE+raw1+QUOTE+"AND"+QUOTE+raw2+QUOTE