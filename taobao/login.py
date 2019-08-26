import requests
import re
import json
import os

s = requests.Session()
COOKIES_FILE_PATH = './cookies'


class TaobaoLogin(object):
    def __init__(self, username, ua, TPL_password_2):
        """

        :param username: 用户名
        :param ua: 登录的ua参数
        :param TPL_password_2: 加密后的密码
        """
        # 判断是否需要验证码
        self.user_check_url = 'https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8'

        # 验证密码
        self.verify_password_url = 'https://login.taobao.com/member/login.jhtml'

        # 个人主页
        self.my_taobao_url = 'http://i.taobao.com/my_taobao.htm'

        # 访问st码URL
        self.vst_url = 'https://login.taobao.com/member/vst.htm?st={}'

        # 淘宝加密参数，可重复使用
        self.ua = ua

        # 加密后的密码
        self.TPL_password_2 = TPL_password_2

        self.username = username
        self.timeout = 3

    def _user_need_verification_check(self):
        """
        判断用户是否需要验证码
        :return:
        """
        data = {
            'username': self.username,
            'ua': self.ua,
        }
        try:
            response = s.post(self.user_check_url, data=data, timeout=self.timeout)
        except Exception as e:
            raise e
        needcode = response.json()['needcode']
        print('是否需要滑块验证：{}'.format(needcode))
        return needcode

    def _verify_password(self):
        """
        验证用户名密码，并获取st码申请url
        :return: 返回st码的申请地址
        """
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-length": "2616",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://login.taobao.com",
            "pragma": "no-cache",
            "referer": "https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d9E1Eohx&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        }
        data = {
            'TPL_username': self.username,
            'ncoToken': 'cdf05a89ad5104403ebb12ebc9b7626af277b066',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': 0,
            'newlogin': 0,
            'TPL_redirect_url': 'https://s.taobao.com/search?q=%E9%80%9F%E5%BA%A6%E9%80%9F%E5%BA%A6&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'loginType': '3',
            'gvfdcname': '10',
            'gvfdcre': '68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61323330722E312E3735343839343433372E372E33353836363032633279704A767526663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246732E74616F62616F2E636F6D25324673656172636825334671253344253235453925323538302532353946253235453525323542412532354136253235453925323538302532353946253235453525323542412532354136253236696D6766696C65253344253236636F6D6D656E64253344616C6C2532367373696425334473352D652532367365617263685F747970652533446974656D253236736F75726365496425334474622E696E64657825323673706D253344613231626F2E323031372E3230313835362D74616F62616F2D6974656D2E31253236696525334475746638253236696E69746961746976655F69642533447462696E6465787A5F3230313730333036',
            'TPL_password_2': self.TPL_password_2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'oslanguage': 'zh-CN',
            'sr': '1440*900',
            'osVer': 'macos|10.145',
            'naviVer': 'chrome|76.038091',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'osPF': 'MacIntel',
            'appkey': '00000000',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?redirectURL=https://s.taobao.com/search?q=%E9%80%9F%E5%BA%A6%E9%80%9F%E5%BA%A6&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&useMobile=true',
            'showAssistantLink': '',
            'um_token': 'T898C0FDF1A3CEE5389D682340C5F299FFE590F51543C8E3DDA8341C869',
            'ua': self.ua
        }
        try:
            response = s.post(self.verify_password_url, headers=headers, data=data, timeout=self.timeout)
        except Exception as e:
            raise e
        apply_st_url_match = re.search(r'<script src="(.*?)"></script>', response.text)
        if apply_st_url_match:
            print('验证用户名密码成功，st码申请地址：{}'.format(apply_st_url_match.group(1)))
            return apply_st_url_match.group(1)
        else:
            raise RuntimeError('用户名密码验证失败！response：{}'.format(response.text))

    def _apply_st(self):
        """
        申请st码
        :return: st码
        """
        apply_st_url = self._verify_password()
        try:
            response = s.get(apply_st_url)
            response.raise_for_status()
        except Exception as e:
            print('申请st码请求失败，原因：')
            raise e
        st_match = re.search(r'"data":{"st":"(.*?)"}', response.text)
        if st_match:
            print('获取st码成功，st码：{}'.format(st_match.group(1)))
            return st_match.group(1)
        else:
            raise RuntimeError('获取st码失败！response：{}'.format(response.text))

    def _load_cookies(self):
        # 1、判断cookies序列化文件是否存在
        if not os.path.exists(COOKIES_FILE_PATH):
            return False
        # 2、加载cookies
        s.cookies = self._deserialization_cookies()
        # 3、判断cookies是否过期
        try:
            self.get_taobao_nick_name()
        except Exception as e:
            os.remove(COOKIES_FILE_PATH)
            print('cookies过期，删除cookies文件！')
            return False
        print('加载淘宝登录cookies成功!!!')
        return True

    def _deserialization_cookies(self):
        """
        反序列化cookies
        :return:
        """
        with open(COOKIES_FILE_PATH, 'r+', encoding='utf-8') as file:
            cookies_dict = json.load(file)
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            return cookies

    def _serialization_cookies(self):
        """
        序列化cookies
        :return:
        """
        cookies_dict = requests.utils.dict_from_cookiejar(s.cookies)
        with open(COOKIES_FILE_PATH, 'w+', encoding='utf-8') as file:
            json.dump(cookies_dict, file)
            print('保存cookies文件成功！')

    def get_taobao_nick_name(self):
        """
        获取淘宝昵称
        :return: 淘宝昵称
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = s.get(self.my_taobao_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('获取淘宝主页请求失败！原因：')
            raise e
        # 提取淘宝昵称
        nick_name_match = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', response.text)
        if nick_name_match:
            print('登录淘宝成功，你的用户名是：{}'.format(nick_name_match.group(1)))
            return nick_name_match.group(1)
        else:
            raise RuntimeError('获取淘宝昵称失败！response：{}'.format(response.text))

    def login(self):
        """
        使用st码登录
        :return:
        """
        # 加载cookies文件
        if self._load_cookies():
            return True
        # 判断是否需要滑块验证
        self._user_need_verification_check()
        st = self._apply_st()
        headers = {
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = s.get(self.vst_url.format(st), headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('st码登录请求，原因：')
            raise e
        # 登录成功，提取跳转淘宝用户主页url
        my_taobao_match = re.search(r'top.location.href = "(.*?)"', response.text)
        if my_taobao_match:
            print('登录淘宝成功，跳转链接：{}'.format(my_taobao_match.group(1)))
            self._serialization_cookies()
            return True
        else:
            raise RuntimeError('登录失败！response：{}'.format(response.text))


if __name__ == '__main__':
    user = '登录用户名或手机号'
    # ua 淘宝重要参数，从浏览器或抓包工具中复制，可重复使用
    ua = '119#MlKXPFmGMLYa4MMztwBzngNzxBHq3t7g+Jl4YDN4Sm0wfdL7TtJT8jdZ5JxagOZwmKlW0NnoPbZYSxYkq9ulUwU6QkzIUnazlT7LK0JsziTGqMI8RJBONt72fHo05/qcXtALbeEV46RRFoAF6G9jlL8GfeASRBsU3DSPPUjhB9RHMsxMT+aU8oxmodAXB/I3FeoFaJ+zB9y8rEDLRgK7Nt8G9eAz1SSed/Wkg2WzjPgLFoA8R2OsNtFLZbAzKBBUFF8fmHTqR99LM033R46VNtxn9AASRSSMrgse9/sds6nrzsMylMvESCqOfoDAiS3eojY2/HsZvxEJJDCEBYxWhJIIsreU5JDfB+kysij0sU1hrvtpqUmNJdX2ZoKWdcRcz/qj5a79eehQk3NjRdubuzqNRzx671dNr61pDwYGbnZPBUJZlWihnqWQcFb18y7mND4u6B9Oc9/xjrq0O+Uj9ov1EForrtPq1xQa5O6IvH+r58yN+h+GayLjPj9V053E+i5WWLn7sf9YrfXhbB/S/qHDRjAXHw4zGqGX38CGdJfINlDjNsFN9Kg/jKHboUA4t+pZy/jsOMdjuhiZy0EXdLPd19zBf4fur2aXz6xo6Cr1LhOGULxJavMSPtfADh6Usm9Di/uM8gy1HLub95WaVYOcSztglwKSxkNFcZT62FNTsOEWpybUGq3VaN8dvdrnrXHzmXfNlOKx2PE2s52h6RJ/8o+89kmCKq5/UgfUJ2RdokuuTR6O+s1m6u5SthtrYVOVnQ5C3OVri0IrghUnt1WSsdxIr5GPE5gnKt7F1tUHqIZhjoWJtTDl9gQOF7uWmvZI3Xm9eaXJodAigH+OSAbnzLUf6XjfNo38eLxR9KXvx0QjHfTPFKJFQs7FNfrfTNrLnOnlwEZ8Iiz/oewieIqUNLpkoF/v4Q18qY3t5uCaXwYzTr5V/BPCAz5wvuuZk37Kxn/U/loHKOpr3CQCVLEDg4SEtwSGsBpVuT3jnkyIRXZE7pEMKMzZ9WKdIY4ai0NgyKH='
    # 加密后的密码 淘宝重要参数，从浏览器或抓包工具中复制
    TPL_password_2 = ''
    t = TaobaoLogin(user, ua, TPL_password_2)
    t.login()
