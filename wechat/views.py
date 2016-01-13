#coding=utf-8
__author__ = 'zhangjingyuan'
import hashlib
import json
from lxml import etree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context,Template,loader
TOKEN = 'jingyuanz'

@csrf_exempt
def wechat(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
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
            return HttpResponse(echostr)
        else:
            return HttpResponse(echostr)
    else:
        xml_str = smart_str(request.body)
        request_xml = etree.fromstring(xml_str)
        response_xml = parse_message(request_xml)
        return HttpResponse(response_xml)


def parse_message(request_xml):
    t = loader.get_template('reply_text.xml')
    content=request_xml.find("Content").text#获得用户所输入的内容
    msgType=request_xml.find("MsgType").text
    fromUser=request_xml.find("FromUserName").text
    toUser=request_xml.find("ToUserName").text
    c = {
        'toUser' : fromUser,
        'fromUser' : toUser,
        'createTime': 1234,
    }
    result = t.render(Context(c))
    return result