import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import io
import track
import random

EMAIL = 'cqc@cuiqingcai.com'
PASSWORD = ''
BORDER = 6
INIT_LEFT = 60


class SliderCracker():
    # 初始化函数
    def __init__(self, url):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.url = url
        self.browser = webdriver.Chrome(options = options)
        self.wait = WebDriverWait(self.browser, 20)
        
    # 自动关闭浏览器
    def __del__(self):
        self.browser.close()
    
    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button
    
    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_window')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        print("top: {}, bottom: {}, left: {}, right: {}".format(top, bottom, left, right))
        return (top, bottom, left, right)
    
    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot
    
    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider
    
    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha
    
    def open(self):
        """
        打开网页
        :return: None
        """
        self.browser.get(self.url)
    
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
    
    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0
        
        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 10
            else:
                # 加速度为负3
                a = -10
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            if current + move < distance:
                track.append(round(move))
                current += move
            else:
                track.append(round(distance - current + 1))
                current = distance + random.randint(0,4)
            # 加入轨迹
        # track.append(round(distance))
        return track

        
    
    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.05)
        ActionChains(self.browser).release().perform()


    # 获取到完整的图片
    def get_full_img(self):
        image_ori = self.browser.execute_script('return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("image/png")')
        image_ori = image_ori.split(',')[1]
        image_ori = base64.b64decode(image_ori)
        image_ori = Image.open(io.BytesIO(image_ori))
        image_ori.save("captcha1.png")
        return image_ori

    # 获取到带有缺口的图片
    def get_crack_img(self):
        image_gap = self.browser.execute_script('return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("image/png")')
        image_gap = image_gap.split(',')[1]
        image_gap = base64.b64decode(image_gap)
        image_gap = Image.open(io.BytesIO(image_gap))
        image_gap.save("captcha2.png")
        return image_gap

    # def simulate_slide(self, slider, target_offset_x):
    #     # action_chains = webdriver.ActionChains(self.browser)
    #     # action_chains.click_and_hold(source).perform()
    #     ActionChains(self.browser).click_and_hold(slider).perform()
    #     ActionChains(self.browser).pause(0.2)
    #     ActionChains(self.browser).move_by_offset(xoffset=target_offset_x - 10, yoffset=0).perform()
    #     ActionChains(self.browser).pause(0.2)
    #     ActionChains(self.browser).move_by_offset(10, yoffset=0).perform()
    #     ActionChains(self.browser).pause(0.6)
    #     ActionChains(self.browser).release().perform()
        
        # action_chains = ActionChains(self.browser).click_and_hold(slider).perform()
        # action_chains.pause(0.2)
        # action_chains.move_by_offset(target_offset_x - 10, 0)
        # action_chains.pause(0.6)
        # action_chains.move_by_offset(10, 0)
        # action_chains.pause(0.6)
        # action_chains.release()
        # action_chains.perform()
    
    def crack(self):
        # 输入用户名密码
        self.open()
        time.sleep(2)
        # 获取滑动按钮
        slider = self.get_slider()
        # 获取到没有缺口的图片
        image1 = self.get_full_img()
        # 获取到带有缺口的图片
        image2 = self.get_crack_img()
        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)
        # 减去缺口位移
        gap -= BORDER
        # 获取移动轨迹
        track = self.get_track(gap)
        print('滑动轨迹', track)
        # 拖动滑块
        self.move_to_gap(slider, track)
        # self.simulate_slide(slider, gap)
        
        success = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
        print(success)
        
        # 失败后重试
        if not success:
            self.crack()
        else:
            self.login()


    