# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 09:40:51 2017

@author: 80374769
"""

import shutil
import os

src_path_1 = u'D:/Firefly workspace/P165231e_（TD四期）零售信息应用-绩效考核集市系统迁移/01文档/03设计文档/02详细设计类文档/ARTP_SDM/'
src_path_2 = u'D:/Firefly workspace/P1629191/01文档/03设计文档/02详细设计类文档/RMP_SDM_2017/'
tar_path = u'D:/SDM/01文档/03设计文档/02详细设计文档/ARTP_SDM/'


#os.remove(tar)
#shutil.copyfile(src,tar)

#shutil.move(r'',r'')  移动文件夹到另外一个地方

for file_name in dsql_move_set:
    file_name = file_name.upper() + '.xlsm'
    sourceFile = os.path.join(src_path_1,file_name) 
    targetFile = os.path.join(tar_path,file_name)
    
    #shutil.copyfile(sourceFile,targetFile)
    if os.path.isfile(targetFile) and targetFile.find(file_name)>0:
        os.remove(targetFile)
        
    if os.path.isfile(sourceFile) and sourceFile.find(file_name)>0:
        shutil.copyfile(sourceFile,targetFile)
    else:
        print file_name,u'------目标文件不存在不存在'
      
        
        
from xlutils.copy import copy
import xlwt
import xlrd
dir_src = u'E:\py\上线内容清单.xlsm'
import os


src_tab = xlrd.open_workbook(dir_src,formatting_info=True)
src_tab = xlrd.open_workbook(dir_src)


file = xlwt.Workbook()
table = file.add_sheet('sheet_name')
table.write(5,5,'test')
table = file.add_sheet('sheet name',cell_overwrite_ok=True)
file.save('demo.xls')

