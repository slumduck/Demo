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
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

'''
    设置字符串的编码为终端支持的编码，非终端设置为utf-8
'''


def set_encoding(str):
    # 获取终端默认编码
    # default_encoding = sys.getdefaultencoding()
    encoding_out = sys.stdout.encoding
    print encoding_out
    if encoding_out is None:
        encoding_out = "UTF-8"
    # encoding_in = sys.stdin.encoding
    # if encoding_in is None:
    #    encoding_in = "UTF-8"
    return str.encode(encoding_out)

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

    # 将base64编码的图片解码并保存

    def save_image(self, base64strs, dir, image_name, suffix=".jpg"):
        img_data = base64.b64decode(base64strs)
        path = dir + os.path.sep + image_name + suffix
        f = open(path, 'wb')
        f.write(img_data)
        f.close()

    # 获取爬取页面的内容

    def get_response_content(self):
        req = urllib2.Request(self.__url)
        try:
            res_data = urllib2.urlopen(req)
            # 请求返回的页面信息
            html_content = res_data.read()
            return html_content
        except:
            print set_encoding(u"访问地址%s异常") %self.__url
            return ""

    # 解析页面内容，获取需要的信息

    def get_content(self):
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
            # 判断文件夹是否存在，存在则删除
            if not os.path.exists(dir_m):
                # 创建文件夹
                os.mkdir(dir_m)
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
                self.save_image(img_data, dir_m, h4.get_text().replace("/", ""))
                # 描述
                strong = a.select_one("strong")
                excel_row.append(strong.get_text())
                excel.append(excel_row)
        return excel

    def content_to_excel(self):
        excel = ExcelUtil()
        excel.write_to_file(self.__jy_xu_dir, self.get_content())


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
            print set_encoding(u"未爬取到数据，请检查URL是否正确")
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


if __name__ == '__main__':

    # html = HtmlParse("http://www.runoob.com/")
    # html.content_to_excel()
    print u"中文"
    print set_encoding(u"中文")
    '''
        print sys.getdefaultencoding()
        print sys.stdin.encoding
        print sys.stdout.encoding
        print u"中文"
    '''