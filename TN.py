from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import fitz  # PyMuPDF
import re
from PyPDF2 import PdfReader, PdfWriter
import os
import glob
import datetime

def process_page(page, page_num):
    # 获取页面尺寸
    width, height = page.size
    
    # 计算上半部分的高度
    upper_half_height = height // 6
    
    # 定义裁剪区域 (left, upper, right, lower)
    box = (0, 0, width, upper_half_height)
    
    # 裁剪图像
    upper_half_image = page.crop(box)
    
    # 保存裁剪后的上半部分图像为 JPEG 并进行识别
    path_image = os.path.join(os.path.dirname(pdf_file), f'{page_num}_upper_half.jpg')
    upper_half_image.save(path_image, "JPEG")
    image = Image.open(path_image)
    label_text = pytesseract.image_to_string(image)
    print(f"第{page_num}页识别完成:")
    
    return label_text

def extract_number(text):
    """
    从文本中提取以指定前缀开头的数字序列
    
    参数：
    - text: 要搜索的文本字符串
    - prefix: 要匹配的前缀字符串
    
    返回值：
    - 如果找到匹配的数字序列，则返回该序列，否则返回 None
    """
    pattern = re.compile(r'\b\d{4}\s+\d{4}\s+\d{4}\b')
    # pattern = re.compile(r'\b\d{4}\s+\d{4}\s+\d{4}\b')

    match = pattern.search(text)
    if match:
        return match.group()
    else:
        return None

# pdf_file = r'C:\Users\76656\Desktop\pdf处理\TN.pdf'
# 获取当前脚本所在目录

# 构建新的PDF文件路径
pdf_file =  'TN.pdf'

results_dict = {}

# 获取PDF页数
doc = fitz.open(pdf_file)
total_pages = doc.page_count
doc.close()

for i in range(1,total_pages + 1):
    page = convert_from_path(pdf_file, 350, first_page=i, last_page=i+1)[0]
    results_dict[i] = process_page(page, i)

page_list = []
other_page_list = []
for page_num, details in results_dict.items():
    # print(page_num)
    if "Newacme LLC" in details:
        page_list.append(page_num)
        print(f"页码 {page_num} 包含 'Newacme LLC'.")
    else:
        other_page_list.append(page_num)
        print(f"页码 {page_num} 不包含 'Newacme LLC'.")

        
# 原始PDF文件路径
# pdf_path = r'C:\Users\76656\Desktop\pdf处理\TN.pdf'

# 构建新的PDF文件路径
pdf_path =  'TN.pdf'
# 创建一个新的PDF写入对象
pdf_writer = PdfWriter()

# 打开PDF文件
with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = PdfReader(pdf_file)

    # 遍历字典列表中的每个项，根据页码范围截取PDF中对应页数的内容
    for item in page_list:
        page_num = item
        # 将指定页码的内容写入新的PDF中
        pdf_writer.add_page(pdf_reader.pages[page_num - 1])

# 新PDF文件保存路径（与原始PDF相同路径）
# output_pdf_path = os.path.join(os.path.dirname(pdf_path), '处理结果', 'output_pdf.pdf')
# 获取当前日期
current_date = datetime.datetime.now().strftime("%m.%d")

# 将日期格式从两位数字改为单个数字
current_date = current_date.lstrip("0").replace(".0", ".")

# 新的文件名
new_file_name = f"prime TN shipping {current_date} (SecondPriority).pdf"

# 生成新的完整路径
output_pdf_path = os.path.join(os.path.dirname(pdf_path), new_file_name)
# 保存新的PDF文件
with open(output_pdf_path, 'wb') as output_pdf:
    pdf_writer.write(output_pdf)

print(f'已经成功截取指定页码范围的内容，并保存至：{output_pdf_path}')

# 原始PDF文件路径
# pdf_path = r'C:\Users\76656\Desktop\pdf处理\TN.pdf'


# 构建新的PDF文件路径
pdf_path = 'TN.pdf'
# 创建一个新的PDF写入对象
pdf_writer = PdfWriter()

# 打开PDF文件
with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = PdfReader(pdf_file)

    # 遍历字典列表中的每个项，根据页码范围截取PDF中对应页数的内容
    for item in other_page_list:
        page_num = item
        # 将指定页码的内容写入新的PDF中
        pdf_writer.add_page(pdf_reader.pages[page_num - 1])

# 新PDF文件保存路径（与原始PDF相同路径）
# output_pdf_path = os.path.join(os.path.dirname(pdf_path), 'other_pdf.pdf')
# 获取当前日期
current_date = datetime.datetime.now().strftime("%m.%d")

# 将日期格式从两位数字改为单个数字
current_date = current_date.lstrip("0").replace(".0", ".")

# 新的文件名
new_file_name = f"prime TN shipping {current_date} (FirstPriority).pdf"

# 生成新的完整路径
output_pdf_path = os.path.join(os.path.dirname(pdf_path), new_file_name)

# 保存新的PDF文件
with open(output_pdf_path, 'wb') as output_pdf:
    pdf_writer.write(output_pdf)

print(f'已经成功截取除指定页码范围外的所有内容，并保存至：{output_pdf_path}')


# # 目标文件夹路径
# folder_path = r'C:\Users\76656\Desktop\pdf处理'

# # 构造要匹配的PNG文件路径模式
# pattern = os.path.join(folder_path, '*.jpg')

# # 获取当前脚本所在目录
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # # 目标文件夹相对路径
# # relative_folder_path = os.path.relpath(folder_path, current_dir)

# # 构造要匹配的PNG文件路径模式
# pattern = os.path.join(current_dir, '*.jpg')
pattern ='*.jpg'

# 查找匹配的PNG文件
png_files = glob.glob(pattern)

# 删除每个PNG文件
for png_file in png_files:
    os.remove(png_file)

print('所有PNG图片已成功删除。')