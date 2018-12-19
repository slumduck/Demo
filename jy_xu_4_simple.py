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

# 将base64字符串转为图片并保存


def save_image(base64strs,dir, image_name, suffix=".jpg"):
    imgdata = base64.b64decode(base64strs)
    path = dir + os.path.sep + image_name + suffix
    f = open(path, 'wb')
    f.write(imgdata)
    f.close()

# 发送http请求获取页面内容


url = "http://www.runoob.com/"
req = urllib2.Request(url)
res_data = urllib2.urlopen(req)
# 请求返回的页面信息
htmlContent = res_data.read()
soup = BeautifulSoup(htmlContent, 'lxml')
codeListDesktop = soup.select(".codelist-desktop")
# 当前python文件所在磁盘位置
currentFileLocation = os.getcwd()
jy_xu_dir = currentFileLocation + os.path.sep + "jy_xu_4"
if not os.path.exists(jy_xu_dir):
    os.mkdir(jy_xu_dir)
excel = []
for div in codeListDesktop:
    # 获取目录标签 <h2></h2>
    h2 = div.select("h2")[0].get_text(strip=True)
    # h2.replace("/", "") 去掉特殊字符，HTML / CSS无法创建文件夹
    dirName = h2.replace("/", "")
    # 文件夹完整路径
    dir = currentFileLocation + os.path.sep + "jy_xu_4" + os.path.sep + dirName
    # 判断文件夹是否存在，存在则删除
    if not os.path.exists(dir):
        # 创建文件夹
        os.mkdir(dir)
    # 获取a标签<a></a>
    a = div.select("a")
    for a_ in a:
        excelRow_1 = []
        # 标题
        h4 = a_.select_one("h4")
        excelRow_1.append(h4.get_text())
        # 图片
        img = a_.select_one("img")
        # 获取图片的src属性
        imgData = img['src'].split(",")[1]
        excelRow_1.append(h4.get_text()+".jpg")
        # 保存图片
        save_image(imgData, dir, h4.get_text().replace("/", ""))
        # 描述
        strong = a_.select_one("strong")
        excelRow_1.append(strong.get_text())
        excel.append(excelRow_1)

# 将数据写入Excel
# 创建workbook和sheet对象
workbook = xlwt.Workbook(encoding='UTF-8')
# 注意Workbook的开头W要大写
sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
for x, row in enumerate(excel):
    for y, cell in enumerate(row):
        sheet1.write(x, y, cell)
        # 设置列宽
        sheet1.col(y).width = 256*40
        if y == 2:
            sheet1.col(y).width = 256 * 60

excelPath = jy_xu_dir + os.path.sep + "jy_xu_4.xls"
workbook.save(excelPath)




