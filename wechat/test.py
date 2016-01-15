#coding=utf-8
__author__ = 'zhangjingyuan'
import random
from random import choice
from collections import defaultdict
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
                results += tup[0] + ":" + str(1.0*tup[1]/sum*100) + "%\n"

            results += "综上, 最佳选项是 -- "+best_choice + " "+best_portion+"%"
            return results


