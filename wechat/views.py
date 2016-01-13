#coding=utf-8
__author__ = 'zhangjingyuan'
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import time
import hashlib
import wechat_sdk
from wechat_sdk import WechatBasic
TOKEN = "jingyuanz"

@csrf_exempt
def wechat(request):
    wechat = wechat_sdk.WechatBasic(token=TOKEN)
    if wechat.check_signature(signature=request.GET['signature'],
                              timestamp=request.GET['timestamp'],
                              nonce=request.GET['nonce']):
        if request.method == 'GET':
            rsp = request.GET.get('echostr', 'error')
        else:
            wechat.parse_data(request.body)
            message = wechat.get_message()
            rsp = wechat.response_text(u'消息类型: {}'.format(message.type))
    else:
        rsp = wechat.response_text('check error')
    return HttpResponse(rsp)