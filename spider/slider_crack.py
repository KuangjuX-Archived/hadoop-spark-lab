import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import io
import track
import random


BORDER = 6


class SliderCracker():
    # 初始化函数
    def __init__(self, url):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.url = url
        self.browser = webdriver.Chrome(options = options)
        self.wait = WebDriverWait(self.browser, 3)
        
    # 自动关闭浏览器
    def __del__(self):
        self.browser.close()
    
    
    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider
    
    
    def open(self):
        """
        打开网页
        :return: None
        """
        self.browser.get(self.url)
        # self.browser.delete_all_cookies()

        # for cookie in self.cookies:
        #     if cookie['domain'] == '.jiayuan.com':
        #         self.browser.add_cookie(cookie)
    
    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left
    
    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False
    
    # 获取到完整的图片
    def get_full_img(self):
        image_ori = self.browser.execute_script('return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("image/png")')
        image_ori = image_ori.split(',')[1]
        image_ori = base64.b64decode(image_ori)
        image_ori = Image.open(io.BytesIO(image_ori))
        image_ori.save("captcha1.png")
        return image_ori

    # 获取到带有缺口的图片
    def get_geetest_img(self):
        image_gap = self.browser.execute_script('return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("image/png")')
        image_gap = image_gap.split(',')[1]
        image_gap = base64.b64decode(image_gap)
        image_gap = Image.open(io.BytesIO(image_gap))
        image_gap.save("captcha2.png")
        return image_gap

    def __get_random_pause_scondes(self):
        return random.uniform(0.6, 0.9)

    def simulate_slide(self, slider, target_offset_x):
        """
        模仿人的拖拽动作：快速沿着X轴拖动（存在误差），再暂停，然后修正误差
        防止被检测为机器人，出现“图片被怪物吃掉了”等验证失败的情况
        :param source:要拖拽的html元素
        :param targetOffsetX: 拖拽目标x轴距离
        :return: None
        """
        action_chains = webdriver.ActionChains(self.browser)
        # 点击，准备拖拽
        action_chains.click_and_hold(slider)
        # 拖动次数，二到三次
        dragCount = random.randint(2, 3)
        if dragCount == 2:
            # 总误差值
            sumOffsetx = random.randint(-15, 15)
            action_chains.move_by_offset(target_offset_x + sumOffsetx, 0)
            # 暂停一会
            action_chains.pause(self.__get_random_pause_scondes())
            # 修正误差，防止被检测为机器人，出现图片被怪物吃掉了等验证失败的情况
            action_chains.move_by_offset(-sumOffsetx, 0)
        elif dragCount == 3:
            # 总误差值
            sumOffsetx = random.randint(-15, 15)
            action_chains.move_by_offset(target_offset_x + sumOffsetx, 0)
            # 暂停一会
            action_chains.pause(self.__get_random_pause_scondes())

            # 已修正误差的和
            fixedOffsetX = 0
            # 第一次修正误差
            if sumOffsetx < 0:
                offsetx = random.randint(sumOffsetx, 0)
            else:
                offsetx = random.randint(0, sumOffsetx)

            fixedOffsetX = fixedOffsetX + offsetx
            action_chains.move_by_offset(-offsetx, 0)
            action_chains.pause(self.__get_random_pause_scondes())

            # 最后一次修正误差
            action_chains.move_by_offset(-sumOffsetx + fixedOffsetX, 0)
            action_chains.pause(self.__get_random_pause_scondes())
        action_chains.release().perform()

    # 模拟登陆账户，不过并没用上
    def login(self):
        account = open("account.txt", "r")
        username = account.readline()
        password = account.readline()
        account.close()
        self.wait.until(EC.presence_of_element_located((By.ID, "login_email_new")))
        self.browser.find_element_by_id('login_email_new').send_keys(username)
        self.browser.find_element_by_id('login_password_new').send_keys(password)
        self.browser.find_element_by_class_name('login_btn').click()
    
    # 破解验证码
    def crack(self):
        # 输入用户名密码
        self.open()
        time.sleep(2)
        # 获取滑动按钮
        slider = self.get_slider()
        # 获取到没有缺口的图片
        image1 = self.get_full_img()
        # 获取到带有缺口的图片
        image2 = self.get_geetest_img()
        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)
        # 减去缺口位移
        gap -= BORDER
        # 模拟人类滑动滑块
        self.simulate_slide(slider, gap)
        
        try:
            # 首先验证是否是被识别为爬虫，若被识别为爬虫，则重新验证
            err1 = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_panel_error_code_text'), '113'))
            if err1:
                self.crack()
        except TimeoutException:
            # 验证是否位置不对，如果位置不对的话则重新开始验证
            try:
                err2 = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_result_content'), '请正确拼合图像'))
                if err2:
                    self.crack()
            except TimeoutException:
                return


    