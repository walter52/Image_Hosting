#!/usr/bin/python3
# @Time    : 2018/12/19 14:58
# @Author  : Walter52
# @File    : image_hosting.py
# @Software: PyCharm

from optparse import OptionParser
import rsa
import re
import requests
import json
import urllib.parse
import base64
import binascii


def ages_info():
    usage = "Usage: %prog [options] arg"
    opt_parser = OptionParser(usage)
    opt_parser.add_option("-f", "--file", action="store", type="string", dest="file", help="file path")
    opt_parser.add_option("-u", "--username", action="store", type="string", dest="user_name", help="user name")
    opt_parser.add_option("-p", "--password", action="store", type="string", dest="user_pwd", help="user password")
    return opt_parser.parse_args()


def login_weibo(user_name=None, user_pwd=None):
    prelogin_url = "http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.2)" % user_name
    prelogin_res = requests.get(prelogin_url).text
    prelogin_res_regex = r'\((.*?)\)'
    prelogin_pattern = re.search(prelogin_res_regex, prelogin_res)
    prelogin_content = None
    if prelogin_pattern.group():
        pre_content = prelogin_pattern.group(1)
    else:
        print("预登陆失败")
        return
    # 获取预登陆数据
    prelogin_jason = json.loads(pre_content)
    servertime = prelogin_jason.get("servertime")
    nonce = prelogin_jason.get("nonce")
    pubkey = prelogin_jason.get("pubkey")
    rsakv = prelogin_jason.get("rsakv")

    # 生成登陆参数
    login_name = base64.encodebytes(urllib.parse.quote(user_name))
    key = rsa.PublicKey(int(pubkey, 16), 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(user_pwd)
    login_pwd = binascii.b2a_hex(rsa.encrypt(message, key))

    form_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': 'http://weibo.com/p/1005052679342531/home?from=page_100505&mod=TAB&pids=plc_main',
        'vsnf': '1',
        'su': login_name,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': login_pwd,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }



if __name__ == "__main__":
    options, arges = ages_info()
    image_file = options.file
    user_name = options.user_name
    user_pwd = options.user_pwd

    login_weibo("walter52")
