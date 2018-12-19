#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
1.爬取http://www.runoob.com/返回的html代码
2.解析出其中的目录、目录中的标题/描述/图片(限定使用BeautifulSoup)
3.按照目录名称创建文件夹，下载图片，图片命名用：标题.后缀
4.目录、标题、描述、图片信息，保存到excel中，按照模板格式存放

作业要求：
1.包含HTML爬取解析和Excel操作二个类
2.if __name__ == “__main”中，不要放任何逻辑代码，最好只放一个调用

执行下面代码需要事先安装：bs4、xlwt第三方库
执行命令如下：
pip install xlwt
pip install beautifulsoup4
pip install lxml
'''

from bs4 import BeautifulSoup
import urllib2
import os
import base64
import xlwt
# 线程安全的队列
import Queue
import threading
import logging
import json
# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
'''
    爬取页面，解析数据
'''


class HtmlParse(object):
    # 初始化要爬取的页面地址
    def __init__(self, url):
        self.__url = url
        # 当前python文件所在磁盘位置
        current_file_location = os.getcwd()
        jy_xu_dir = current_file_location + os.path.sep + "jy_xu_4"
        # 当前文件夹下没有jy_xu_4文件夹则创建
        if not os.path.exists(jy_xu_dir):
            os.mkdir(jy_xu_dir)
        self.__jy_xu_dir = jy_xu_dir
        # 创建队列存放图片信息
        self.image_queue = Queue.Queue()
        self.log = Logger(self.__jy_xu_dir, "jy_xu.log", logging.INFO)

    # 将base64编码的图片解码并保存

    def save_image(self, image_data, path, image_name, suffix=".jpg"):
        img_data = base64.b64decode(image_data)
        path = path + os.path.sep + image_name + suffix
        f = open(path, 'wb')
        f.write(img_data)
        f.close()

    # 启动线程保存、下载图片  注：这里可以使用线程池 不浪费资源  pip install threadpool

    def save_image_threading(self):
        while not self.image_queue.empty():
            # image_dict = {'image_data': img_data, 'path': dir_m, 'image_name': h4.get_text().replace("/", "")}
            q = self.image_queue.get()
            self.log.logger.info(u"保存图片到本地，该图片具体信息如下：%s",json.dumps(q, ensure_ascii=False))
            t = threading.Thread(target=self.save_image, name='image_threading', kwargs=q)
            t.start()
            t.join()

    # 获取爬取页面的内容
    def get_response_content(self):
        req = urllib2.Request(self.__url)
        self.log.logger.info(u"请求的URL地址：%s", self.__url)
        try:
            res_data = urllib2.urlopen(req)
            # 请求返回的页面信息
            html_content = res_data.read()
            # self.log.logger.info(u"爬取页面完成,内容如下\n：%s", html_content)
            return html_content
        except Exception, e:
            self.log.logger.error(u"爬取页面异常：%s", e)
            return ""

    # 解析页面内容，获取需要的信息
    def get_content(self):
        self.log.logger.info(u"开始过滤页面内容。。。。。")
        content = self.get_response_content()
        excel = []
        if content == "":
            return excel
        soup = BeautifulSoup(content, 'lxml')
        code_list_desktop = soup.select(".codelist-desktop")
        for div in code_list_desktop:
            # 获取目录标签 <h2></h2>
            h2 = div.select("h2")[0].get_text(strip=True)
            # h2.replace("/", "") 去掉特殊字符，HTML / CSS无法创建文件夹
            dir_name = h2.replace("/", "")
            # 文件夹完整路径
            dir_m = self.__jy_xu_dir + os.path.sep + dir_name
            # 判断文件夹是否存在，不存在则创建
            if not os.path.exists(dir_m):
                os.mkdir(dir_m)
                self.log.logger.info(u"创建目录：%s", dir_m)
            # 获取a标签<a></a>
            a_tag = div.select("a")
            for a in a_tag:
                excel_row = []
                # 标题
                h4 = a.select_one("h4")
                excel_row.append(h4.get_text())
                # 图片
                img = a.select_one("img")
                # 获取图片的src属性
                img_data = img['src'].split(",")[1]
                excel_row.append(h4.get_text() + ".jpg")
                # 保存图片 h4.get_text().replace("/", "") 处理特殊名称的标题
                image_dict = {'image_data': img_data, 'path': dir_m, 'image_name': h4.get_text().replace("/", "")}
                # self.save_image(img_data, dir_m, h4.get_text().replace("/", ""))
                self.image_queue.put(image_dict, block=False)
                # 描述
                strong = a.select_one("strong")
                excel_row.append(strong.get_text())
                excel.append(excel_row)
                self.log.logger.info(u"子标题完整内容：%s", json.dumps(excel_row, ensure_ascii=False))
        self.log.logger.info(u"过滤页面内容结束。。。。。")
        return excel

    def content_to_excel(self):
        excel = ExcelUtil()
        excel_data = self.get_content()
        self.log.logger.info(u"开始生成Excel，Excel原始数据如下：%s", json.dumps(excel_data, ensure_ascii=False))
        excel.write_to_file(self.__jy_xu_dir, excel_data)
        self.log.logger.info(u"Excel文件生成完毕。。。。")
        self.log.logger.info(u"开始进行图片下载及保存。。。。")
        self.save_image_threading()
        self.log.logger.info(u"图片下载及保存结束。。。。")


'''
    讲解析出来的数据保存到Excel文件
'''


class ExcelUtil(object):
    def __init__(self):
        # 创建workbook和sheet对象
        self.workbook = xlwt.Workbook(encoding='UTF-8')

    # 将数据写入Excel
    def write_to_file(self, dir_, data):
        if len(data) == 0:
            print u"未爬取到数据，请检查URL是否正确"
            return
        # 注意Workbook的开头W要大写
        sheet1 = self.workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        for x, row in enumerate(data):
            for y, cell in enumerate(row):
                sheet1.write(x, y, cell)
                # 设置列宽
                sheet1.col(y).width = 256 * 40
                if y == 2:
                    sheet1.col(y).width = 256 * 60
        excel_path = dir_ + os.path.sep + "jy_xu_4.xls"
        self.workbook.save(excel_path)

'''
    日志记录类
'''


class Logger(object):
    def __init__(self, log_path, log_name, log_level):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        full_path = log_path + os.path.sep + log_name
        fh = logging.FileHandler(full_path, mode='w')
        # 输出到file的log等级的开关
        fh.setLevel(log_level)
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(fh)

    def get_log(self):
        return self.logger


if __name__ == '__main__':

    html = HtmlParse("http://www.runoob.com/")
    html.content_to_excel()