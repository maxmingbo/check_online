#-*- coding: utf8 -*-
import xlrd
from pyExcelerator import *
  
w = Workbook() 
ws = w.add_sheet('Sheet1') 
 
fname = "reflect.xls"
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
try:
 sh = bk.sheet_by_name("Sheet1")
except:
 print "no sheet in %s named Sheet1" % fname
 
nrows = sh.nrows
ncols = sh.ncols
print "nrows %d, ncols %d" % (nrows,ncols)
  
cell_value = sh.cell_value(1,1)
#print cell_value
  
row_list = []
mydata = []
for i in range(1,nrows):
	row_data = sh.row_values(i)
	pkgdatas = row_data[3].split(',')
	#pkgdatas.split(',')
	#获取每个包的前两个字段
	for pkgdata in pkgdatas:
	 pkgdata = '.'.join((pkgdata.split('.'))[:2])
	 mydata.append(pkgdata)
	#将列表排序
	mydata = list(set(mydata))
	print mydata
	#将列表转化为字符串
	mydata = ','.join(mydata)
	#写入数据到每行的第一列
	ws.write(i,0,mydata)
	mydata = []
	row_list.append(row_data[3])
	#print row_list
	 
	w.save('mini.xls')


导入

import xlrd

打开excel

data = xlrd.open_workbook('demo.xls') #注意这里的workbook首字母是小写

查看文件中包含sheet的名称

data.sheet_names()

得到第一个工作表，或者通过索引顺序 或 工作表名称

table = data.sheets()[0]

table = data.sheet_by_index(0)

table = data.sheet_by_name(u'Sheet1')

获取行数和列数

nrows = table.nrows

ncols = table.ncols

获取整行和整列的值（数组）

table.row_values(i)

table.col_values(i)

循环行,得到索引的列表

for rownum in range(table.nrows):

print table.row_values(rownum)

单元格

cell_A1 = table.cell(0,0).value

cell_C4 = table.cell(2,3).value

分别使用行列索引

cell_A1 = table.row(0)[0].value

cell_A2 = table.col(1)[0].value



简单的写入

row = 0

col = 0

ctype = 1 # 类型 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error

value = 'lixiaoluo'

xf = 0 # 扩展的格式化 (默认是0)

table.put_cell(row, col, ctype, value, xf)

table.cell(0,0) # 文本:u'lixiaoluo'

table.cell(0,0).value # 'lixiaoluo'

xlwt

http://pypi.python.org/pypi/xlrd

简单使用

导入xlwt

import xlwt

新建一个excel文件

file = xlwt.Workbook() #注意这里的Workbook首字母是大写，无语吧

新建一个sheet

table = file.add_sheet('sheet name')

写入数据table.write(行,列,value)

table.write(0,0,'test')

如果对一个单元格重复操作，会引发

returns error:

# Exception: Attempt to overwrite cell:

# sheetname=u'sheet 1' rowx=0 colx=0

所以在打开时加cell_overwrite_ok=True解决

table = file.add_sheet('sheet name',cell_overwrite_ok=True)

保存文件

file.save('demo.xls')



另外，使用style

style = xlwt.XFStyle() #初始化样式

font = xlwt.Font() #为样式创建字体

font.name = 'Times New Roman'

font.bold = True

style.font = font #为样式设置字体

table.write(0, 0, 'some bold Times text', style) # 使用样式

xlwt 允许单元格或者整行地设置格式。还可以添加链接以及公式。可以阅读源代码，那里有例子：

dates.py, 展示如何设置不同的数据格式

hyperlinks.py, 展示如何创建超链接 (hint: you need to use a formula)

merged.py, 展示如何合并格子

row_styles.py, 展示如何应用Style到整行格子中.





from xlsxwriter.workbook import Workbook 
# Create an new Excel file and add a worksheet.
workbook = Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()

# Widen the first column to make the text clearer.
worksheet.set_column('A:A', 20)

# Add a bold format to highlight cell text.
bold = workbook.add_format({'bold': 1})

# Write some simple text.
worksheet.write('A1', 'Hello')

# Text with formatting.
worksheet.write('A2', 'World', bold)

# Write some numbers, with row/column notation.
worksheet.write(2, 0, 123)
worksheet.write(3, 0, 123.456)

workbook.close()