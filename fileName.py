# -*- coding: utf-8 -*-

# https://github.com/euske/pdfminer/tree/2103e5875ef04cfaf424b25d2fd0dc9535a90714/pdfminer/cmap
from io import StringIO
from io import open
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfinterp import PDFResourceManager, process_pdf, PDFPageInterpreter
from pdfminer.pdfparser import PDFDocument, PDFParser
import csv
import re
import os

input = []

def read_pdf(pdf, fileName):
    # 创建一个一个与文档关联的解释器
    parser = PDFParser(pdf)
    # PDF文档的对象
    doc = PDFDocument()
    # 连接解释器和文档对象
    parser.set_document(doc)
    doc.set_parser(parser)
    # 初始化文档,当前文档没有密码，设为空字符串
    doc.initialize("")
    # 创建PDF资源管理器
    resource = PDFResourceManager()
    # 参数分析器
    laparam = LAParams()
    # 创建一个聚合器
    device = PDFPageAggregator(resource, laparams=laparam)
    # 创建PDF页面解释器
    interpreter = PDFPageInterpreter(resource, device)

    for index, page in enumerate(doc.get_pages()):
        if index == 0: 
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            lines = []
            for index, x in enumerate(layout):
                if (isinstance(x, LTTextBoxHorizontal)):
                        #需要写出编码格式
                        #解决\u8457\u5f55\u683c\u5f0f\uff1a\u67cf\u6167乱码
                        results = x.get_text().encode('raw_unicode_escape').decode('unicode_escape')
                        print(x)
                        lines.append(results)
            
            if len(lines) != 0:
                info = []
                info.append(fileName)
                for index, str in enumerate(lines):
                    if ('经营者姓名' in str or '身份证号码' in str):
                        times = str.count('\n', 0, len(str))

                        # 出现两次\n过滤出数据
                        if times == 2: 
                            reList = re.findall(".*\n(.*)\n.*", str)
                            if len(reList) != 0:
                                print('过滤取数据 = ' +reList[0])
                                info.append(reList[0])

                        else:
                            # 直接取下一个元素
                            if ((index+1) < len(lines)):
                                print('取下一个下标数据 = ' + lines[index+1].strip())
                                info.append(lines[index+1].strip())
                
            
                if len(info) == 3:
                    input.append(info)
        break

def inputCSV(data):
    header = ['文件名', '名字', '身份证']
    with open('result.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

if __name__ == '__main__':
    fileList = os.listdir()
    print("所有文件名 = ", fileList)
    for name in fileList:
        if '.pdf' in name:
            with open(name, "rb") as my_pdf:
                read_pdf(my_pdf, name)


    inputCSV(input)