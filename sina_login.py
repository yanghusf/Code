# 导入所需模块
import urllib.error
import urllib.request
import urllib.parse
import re
import rsa
import http.cookiejar  #从前的cookielib
import base64
import json
import urllib
import binascii

# 简历Launcher类
class Launcher():
    # 初始化username和password这两个参数
    def __init__(self,username,password):
        self.username = username
        self.password = password

    #建立get_encrypted_name方法，获取base64加密后的用户名
    def get_encrypted_name(self):
        # 将字符串转化为url编码
        username_urllike = urllib.request.quote(self.username)
        username_encrypted = base64.b64encode(bytes(username_urllike, encoding='utf-8'))
        return username_encrypted.decode('utf-8')  # 将bytes对象转为str

    def get_prelogin_args(self):
        '''
        该函数用于模拟预登录过程,并获取服务器返回的 nonce , servertime , pubkey 等信息,用一个字典返回数据
        '''
        json_pattern = re.compile('\((.*)\)')
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&' + self.get_encrypted_name() + '&rsakt=mod&client=ssologin.js(v1.4.19)'
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            raw_data = response.read().decode('utf-8')
            # 利用正则取出json
            json_data = json_pattern.search(raw_data).group(1)
            # 讲json包装成字典
            data = json.loads(json_data)
            # print(data)
            return data
        except urllib.error as e:
            print("%d" % e.code)
            return None

    # 建立get_encrypeted_pw获取登录信息生成的rsa加密版密码
    def get_encrypted_pw(self, data):
        rsa_e = int('10001',16)  # 0x10001
        pw_string = str(data['servertime']) + '\t' + str(data['nonce']) + '\n' + str(self.password)
        key = rsa.PublicKey(int(data['pubkey'], 16), rsa_e)
        pw_encypted = rsa.encrypt(pw_string.encode('utf-8'), key)
        self.password = ''  # 安全起见清空明文密码
        passwd = binascii.b2a_hex(pw_encypted)
        print(passwd)
        return passwd

    def enableCookies(self):
        # 建立一个cookies 容器
        cookie_container = http.cookiejar.CookieJar()
        # 将一个cookies容器和一个HTTP的cookie的处理器绑定
        cookie_support = urllib.request.HTTPCookieProcessor(cookie_container)
        # 创建一个opener,设置一个handler用于处理http的url打开
        opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
        # 安装opener，此后调用urlopen()时会使用安装过的opener对象
        urllib.request.install_opener(opener)

    # 构造build_post_data方法，用于包装一个POST方法所需的数据
    def build_post_data(self, raw):
        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "qrcode_flag":'false',
            "useticket": "1",
            "pagerefer": "https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F",
            "vsnf": "1",
            "su": self.get_encrypted_name(),
            "service": "miniblog",
            "servertime": raw['servertime'],
            "nonce": raw['nonce'],
            "pwencode": "rsa2",
            "rsakv": raw['rsakv'],
            "sp": self.get_encrypted_pw(raw),
            "sr": "1680*1050",
            "encoding": "UTF-8",
            "prelt": "194",
            "url": "https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype": "META"
        }
        data = urllib.parse.urlencode(post_data).encode('utf-8')
        return data

    # 登录，注意这里需要进行三次跳转
    def login(self):
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        self.enableCookies()
        data = self.get_prelogin_args()
        post_data = self.build_post_data(data)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        try:
            request = urllib.request.Request(url=url, data=post_data, headers=headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('GBK')
            '''
            一开始用的是utf－8解码，然而得到的数据很丑陋，却隐约看见一个GBK字样。所以这里直接采用GBK解码
            '''
            # print(html)
        except urllib.error as e:
            print(e.code)

        p = re.compile('location\.replace\("(.*?)"\)')
        p2 = re.compile("location\.replace\('(.*?)'\)")
        p3 = re.compile(r'"userdomain":"(.*?)"')
        try:
            login_url = p.search(html).group(1)
            request = urllib.request.Request(login_url)
            response = urllib.request.urlopen(request)
            page = response.read().decode('GBK')
            # print(page)
            login_url2 = p2.search(page).group(1)
            request = urllib.request.Request(login_url2)
            response = urllib.request.urlopen(request)
            page2 = response.read().decode('utf-8')
            # print(page2)
            login_url = 'http://weibo.com/' + p3.search(page2).group(1)
            request = urllib.request.Request(login_url)
            response = urllib.request.urlopen(request)
            final = response.read().decode('utf-8')
            print(final)

            print("Login success!")
        except:
            print('Login error!')
            return 0