from pdf2image import convert_from_path
from aip import AipOcr
import os

pdf_file = r'C:\Users\76656\Desktop\pdf\prime LA 3.2 D_page_1.pdf'
APP_ID = '59237326'
API_KEY = '2d61mYvFP0K5ikXDUKhDziRP'
SECRET_KEY = 'jg65E03YzdF15LNQ5lDmMCo0B4Dsm70I'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def baidu_ocr(pdf_path):
    # 创建结果文件，路径与PDF文件路径一致
    result_file = os.path.join(os.path.dirname(pdf_path), 'result.txt')
    f = open(result_file, 'w', encoding='utf-8')
    
    # 创建目录用于保存图片，路径与PDF文件路径一致
    dirname = pdf_path.rsplit('.', 1)[0]
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    
    # 将PDF转换为图像
    images = convert_from_path(pdf_path, fmt='png', output_folder=dirname)
    
    # 遍历每一页图像进行OCR识别
    for img in images:
        with open(img.filename, 'rb') as fimg:
            img_data = fimg.read()  # 读取图片为二进制数据
            msg = client.basicGeneral(img_data)
            
            # 将识别结果写入文件
            for i in msg.get('words_result'):
                f.write('{}\n'.format(i.get('words')))
            f.write('\f\n')  # 分隔不同页面的识别结果
    
    # 关闭文件
    f.close()

# 调用函数并传入PDF文件路径
baidu_ocr(pdf_file)
