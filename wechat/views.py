__author__ = 'zhangjingyuan'
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import time
import hashlib
TOKEN = "jingyuanz"

@csrf_exempt
def wechat(request):
    if request.method == 'POST':
        response = HttpResponse(checkSignature(request),content_type="text/plain")
        return response

    else:
        return "hello"

def checkSignature(request):
    global TOKEN
    signature = request.POST.get("signature", None)
    timestamp = request.POST.get("timestamp", None)
    nonce = request.POST.get("nonce", None)
    echoStr = request.POST.get("echostr",None)
    token = TOKEN
    tmpList = [token,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echoStr
    else:
        return echoStr