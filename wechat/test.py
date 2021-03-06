#coding=utf-8
__author__ = 'zhangjingyuan'
import random
from random import choice
from collections import defaultdict
import urllib2
import re
AND = "AND"
PLUS = '+'
SPACE = ' '
QUOTE = '"'
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
            keys = QUOTE+(QUOTE+"AND").join(key_words)+QUOTE
            sum = 0
            content_dict = defaultdict(int)
            for item in choices:
                item_all_keys = QUOTE+item+QUOTE+AND+keys
                print item_all_keys
                penalty = count_search_engine(QUOTE+item+QUOTE)
                starting_value = 5.0*(count_search_engine(item_all_keys)/penalty)
                content_dict[item] += starting_value
                sum += starting_value
                for key in key_words:
                    print key
                    value = 1.0*count_search_engine(convert_into_search_query(item, key))/penalty
                    content_dict[item] += value
                    sum += value

            sorted_dict = sorted(content_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
            # best_choice = sorted_dict[0][0]
            # best_portion = str(round(1.0*sorted_dict[0][1]/sum*100, 2))
            results = ""
            for tup in sorted_dict:
                results += tup[0] + str(round(1.0*tup[1]/sum*100, 2)) + "%\n\n"

            # results += u"综上, 最佳选项是 -- "+best_choice + u" "+best_portion+u"%"
            # logging.error(results)
            print results
            return results


def count_search_engine(content):
    url_address = 'http://www.baidu.com/s?wd={}'.format(urllib2.quote(content))
    print url_address
    f = urllib2.urlopen(url_address)
    buf = f.read()
    buf = buf.replace(',', "")
    num = re.findall(r'百度为您找到相关结果约(\d+)个',buf)
    if len(num) == 1:
        return int(num[0])+1
    return 1


def convert_into_search_query(raw1, raw2):
    return QUOTE+raw1+QUOTE+"AND"+QUOTE+raw2+QUOTE


parse_content('香蕉 大饼?好吃 上火')
