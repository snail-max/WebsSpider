# -*-coding:utf-8-*-
"""
    实现12306模拟登录步骤
        1.selenium访问12306主页
        2.对当前的的页面进行截图，获取整张图片
        3.对当前页面的验证码部分进行截取，
            1.好处将登录页面的一一对应
        4.使用全球鹰对验证码识别并返回坐标
"""

import os
import time
import configparser
import requests
from hashlib import md5
from selenium import webdriver
from selenium.webdriver import ActionChains
from PIL import Image


def GetInform():
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, 'UserAndPasswd.ini')
    print(cfgpath)  # 输出存储密码的路径

    # 创建管理对象
    conf = configparser.ConfigParser()

    # 读取ini文件
    conf.read(cfgpath, encoding='utf-8')

    # 获取所有的的section
    sections = conf.sections()
    print(sections)

    items = conf.items('UseInform')
    return items


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


class Login12306():
    def __init__(self, name, passwd, id):
        self.name = name
        self.passwd = passwd
        self.id = id
        self.bro = webdriver.Chrome(executable_path='../chromedriver.exe')

    # 读取网页获取截取的图片保存图片
    def login(self):
        self.bro.get('https://kyfw.12306.cn/otn/resources/login.html')
        time.sleep(1)
        # 跳转到账号登录页面
        self.bro.find_element_by_link_text('账号登录').click()
        time.sleep(1)

        # 识别账户和密码的文本框填入数据
        self.bro.find_element_by_id('J-userName').send_keys('ssssssssss')
        time.sleep(0.3)
        self.bro.find_element_by_id('J-password').send_keys('sssssssss')
        time.sleep(0.3)

        # 检测当前路径下是否有同名的文件，有删除
        if os.path.exists('./temp_png/full.png'):
            os.remove('./temp_png/full.png')
        # 将当前页面的进行截图并保存
        self.bro.save_screenshot('./temp_png/full.png')
        # 获取验证码页面的图片
        code_image_ele = self.bro.find_element_by_id('J-loginImg')
        location = code_image_ele.location
        size = code_image_ele.size
        # 获取验证对应的坐标
        rangle = (
            int(location['x']), int(location['y']),
            int(location['x'] + size['width']), int(location['y'] + size['height'])
        )
        full_image = Image.open('./temp_png/full.png')
        code_image_name = './temp_png/code.png'
        frame = full_image.crop(rangle)
        frame.save(code_image_name)
        return code_image_ele

    def run(self):
        code_image_ele = self.login()
        # 使用超级鹰识别验证码返回函数
        login123 = Chaojiying_Client(self.name, self.passwd, self.id)  # 用户中心>>软件ID 生成一个替换 96001
        im = open('./temp_png/code.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        print(login123.PostPic(im, 9004))
        result = login123.PostPic(im, 9004)['pic_str']
        # {'err_no': 0, 'err_str': 'OK', 'pic_id': '1138221556081800003', 'pic_str': '33,134', 'md5': '218014cc4a8cd46475ef4d484170b5f3'}
        # 对获取的坐标进行解析
        all_list = []
        if '|' in result:
            list_1 = result.split('|')
            count_1 = len(list_1)
            for i in range(count_1):
                xy_list = []
                x = int(list_1[i].split(',')[0])
                y = int(list_1[i].split(',')[1])
                xy_list.append(x)
                xy_list.append(y)
                all_list.append(xy_list)
        else:
            x = int(result.split(',')[0])
            y = int(result.split(',')[1])
            xy_list = []
            xy_list.append(x)
            xy_list.append(y)
            all_list.append(xy_list)
        # 遍历列表，使用动作链对一系列的动作
        for i in all_list:
            x = i[0]
            y = i[1]
            ActionChains(self.bro).move_to_element_with_offset(code_image_ele, x, y).click().perform()
            time.sleep(0.5)
        self.bro.find_element_by_id('J-login').click()
        time.sleep(5)
        self.bro.close()


if __name__ == '__main__':
    lis_info = GetInform()
    name = lis_info[0][1]
    passwd = lis_info[1][1]
    id = lis_info[2][1]
    print(name, id, passwd)
    g = Login12306(name, passwd, id)
    g.run()
