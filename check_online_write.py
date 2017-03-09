# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 11:25:44 2017
对上线清单，依赖变更进行检查。
@author: 80374769
"""

import os
import xlrd

import shutil

date_online = '20170209'
#import sys
#print sys.getdefaultencoding()
#bk=xlrd.open_workbook(Filename)
#import json, yaml



artp_head_set = set(['ARTP_P_ARTP','ARTP_R_ARTP','BRTL_P_BRTL','NDS_C_NLF14',\
'NDS_C_NLF39','NDS_C_NS196','NDS_C_NL38','NDS_P_NLF14','NDS_P_NLA58','NDS_C_NSINT',\
'NDS_P_NDS_P','NDS_P_NLF02','NDS_P_NLV20','NDS_C_NX102','NDS_P_NLH20','NDS_C_NX101',\
'NDS_C_NLV27','NDS_P_NLN61','NDS_C_NLV24','NDS_C_NLV23','NDS_C_NLV22','NDS_C_NLV21',\
'NDS_C_NLV20','NDS_C_NLF02','NDS_C_NLV25','NDS_C_NLV26','NDS_P_NLL56','NDS_P_NSINT',\
'NDS_C_NB971','NDS_C_NLF53','NDS_P_NLF39','NDS_C_NLN57','NDS_P_NLN50','NDS_P_NLU77'])

id_name_set = {'name_id':'name'}


dir_1 = u'D:\\Firefly workspace\\P165231e_（TD四期）零售信息应用-绩效考核集市系统迁移\\01文档\\09配置管理\\03上线投产\\'+date_online
dir_2 = u'D:\\Firefly workspace\\P1629191\\01文档\\09配置管理\\03上线投产\\'+date_online

src_path_1 = u'D:/Firefly workspace/P165231e_（TD四期）零售信息应用-绩效考核集市系统迁移/01文档/03设计文档/02详细设计类文档/ARTP_SDM/'
src_path_2 = u'D:/Firefly workspace/P1629191/01文档/03设计文档/02详细设计类文档/RMP_SDM_2017/'
tar_path = u'D:/SDM/01文档/03设计文档/02详细设计文档/ARTP_SDM/'

dsql_move_set1 = set()
dsql_move_set2 = set()

'''
检查填写错误
'''

for dir_path in (dir_1,dir_2):
    print '\n'
    
    print dir_path

    
    dsql_new_set = {}
    depend_dsql_set = set()
    
    
    for filename in os.listdir(dir_path):

        '''
        *************************************对依赖变更进行检查*****************************
        '''
        if filename.find(u'CMB_RTL作业依赖变更登记表') != -1:
#        if filename.decode('gb2312').find(u'CMB_RTL作业依赖变更登记表') != -1:.
            print filename
            #print filename.decode('gb2312').encode('utf-8')
            data = xlrd.open_workbook(dir_path+'\\'+filename)
            table1 = data.sheet_by_name(u'作业关系配置变更')
            #table2 = data.sheet_by_name(u'下线作业列表')
            dsql1_dsql2_set = set()
            
            for i in range(2,table1.nrows):
                dsql1_name = table1.cell(i,0).value
                dsql2_name = table1.cell(i,2).value
                dsql1_dsql2 = dsql1_name + dsql2_name
                id_name = table1.cell(i,8).value
                author_id  = table1.cell(i,9).value
                    
                if author_id not in id_name_set.keys() and type(author_id) != float:
                    print u'依赖变更: ididididid作业一事通号码不正确：'
                    print '     ',i+1,'id is: ',author_id,'    ',table1.cell(i,10).value,id_name
                if dsql1_name[0:11] not in artp_head_set or dsql2_name[0:11] not in artp_head_set:
                    print u'依赖变更: !!!!!!!!!!!作业前缀不正确：'
                    print '  ',i+1,dsql1_name,dsql2_name,id_name
                if dsql1_name.islower() or dsql2_name.islower():
                    print u'依赖变更: @@@@@@@@@@@@作业名没有大写：'
                    print '  ',i+1,dsql1_name,dsql2_name,id_name

                if dsql1_dsql2 not in dsql1_dsql2_set:
                    dsql1_dsql2_set.add(dsql1_dsql2)
                else:
                    print u'依赖变更: $$$$$$$$$$$$$依赖填写重复：'
                    print '  ',i+1,dsql1_name,dsql2_name,id_name
                    
                if dsql1_name not in  depend_dsql_set: 
                    depend_dsql_set.add(dsql1_name)
                if dsql2_name not in depend_dsql_set:
                    depend_dsql_set.add(dsql2_name)
#                if id_name not in id_name_set:
#                    id_name_set.add(id_name)
#                artp_head_set.add(dsql1_name)
#                artp_head_set.add(dsql2_name)
                    
        '''
        *****************对上线清单进行检查*****************************************
        '''                           
        if filename.find(u'上线内容清单') != -1 :        
#        if filename.decode('gb2312').find(u'上线内容清单') != -1 :
            print filename
            #print filename.decode('gb2312').encode('utf-8')                       
            data = xlrd.open_workbook(dir_path+ '\\'+ filename)
            table = data.sheet_by_name(u'上线内容清单')
            dsql_name_set = set()
            dsql_count = 0
            dsql_null_count = 0
            
            
            
            for i in range(8,table.nrows):
                
                author = table.cell(i,2).value
                author2 = table.cell(i,3).value
                if len(author)<1 or len(author2)<1:
                    print i+1,u'---------负责人没有填写-------'

                if table.cell(i,0).value in (u'作业',u'空作业'):
                    #artp_head_set.add(table.cell(i,1).value[0:11].upper())
                    dsql_name = table.cell(i,1).value

                    if table.cell(i,0).value == u'作业':
                        dsql_count += 1
                        if dir_path == dir_1:
                            dsql_move_set1.add(dsql_name.replace('.dsql',''))
                        else:
                            dsql_move_set2.add(dsql_name.replace('.dsql',''))

                        if table.cell(i,4).value.find(u'新') != -1:
                            dsql_new_set[dsql_name.replace('.dsql','')] = author
                    if table.cell(i,0).value == u'空作业':
                        dsql_null_count += 1
                        dsql_new_set[dsql_name.replace('.dsql','')] = author


                    if dsql_name not in dsql_name_set:
                        dsql_name_set.add(dsql_name)
                    else:
                        print u'作业清单+++++++++++作业名重复：'
                        print '  ',i+1,dsql_name,author
                    if dsql_name[0:11] not in ('artp_p_artp','artp_r_artp'):
                        print u'作业清单**********作业名前缀不正确：'
                        print '  ',i+1,dsql_name,author
                    if dsql_name.isupper():
                        print u'作业清单%%%%%%%%%%作业名没有小写：'
                        print '  ',i+1,dsql_name,author
                    if dsql_name.find(' ') != -1:
                        print u'作业清单__________作业名有空格：'
                        print '  ',i+1,dsql_name,author
                    if dsql_name.find('.dsql') == -1:
                        print u'作业清单..........作业名漏了.dsql：'
                        print '  ',i+1,dsql_name,author
                        
    for add_dsql in dsql_new_set.keys():
        if add_dsql.upper() not in depend_dsql_set:
            print u'新上线作业没有配置依赖000000'
            print '  ' , add_dsql,dsql_new_set[add_dsql]


'''
移动两个文件目录中的SDM到一个文件夹中
'''

for file_name in dsql_move_set1:
    file_name = file_name.upper() + '.xlsm'
    sourceFile = os.path.join(src_path_1,file_name) 
    targetFile = os.path.join(tar_path,file_name)
    
    #shutil.copyfile(sourceFile,targetFile)
    if os.path.isfile(targetFile) and targetFile.find(file_name)>0:
        os.remove(targetFile)
        
    if os.path.isfile(sourceFile) and sourceFile.find(file_name)>0:
        shutil.copyfile(sourceFile,targetFile)
        print file_name,u'      从核心仓库移动成功'
    else:
        print file_name,u'---------核心仓库文件夹中不存在'
        
for file_name in dsql_move_set2:
    file_name = file_name.upper() + '.xlsm'
    sourceFile = os.path.join(src_path_2,file_name)
    targetFile = os.path.join(tar_path,file_name)
    
    #shutil.copyfile(sourceFile,targetFile)
    if os.path.isfile(targetFile) and targetFile.find(file_name)>0:
        os.remove(targetFile)
        
    if os.path.isfile(sourceFile) and sourceFile.find(file_name)>0:
        shutil.copyfile(sourceFile,targetFile)
        print file_name,u'      从零售仓库移动成功'
    else:
        print file_name,u'--------零售仓库文件夹中不存在'

''''
将两处填写的上线内容合并到一处
'''


import xlwt

xlsm =[u'上线内容清单.xlsm',u'CMB_RTL作业依赖变更登记表(CTM版本)_ARTP.xlsm',\
u'CMB_RTL作业依赖变更登记表(CTM版本)_ARTP_RMP.xlsm',u'CMB_RTL作业依赖变更登记表(CTM版本)_ARTP_RMP_MT.xlsm']


for xl in xlsm:
    
    file = xlwt.Workbook()
    table = file.add_sheet(u'合并内容')
    start_row = 0
    
    print xl
    
    for dir_src in (dir_1,dir_2):
        
        try:
            src_tab = xlrd.open_workbook(dir_src +'\\'+ xl)
        except:
            print u"no xlsm %s named in dir: %s" %(xl,dir_src)
        
        start_read_row = 0
        if xl == u'上线内容清单.xlsm':
            sheet_name = u'上线内容清单'
            start_read_row = 9
        else:
            sheet_name = u'作业关系配置变更'
            start_read_row = 2
        
        try:
            src_sheet = src_tab.sheet_by_name(sheet_name)
        except:
            print u"no sheet %s in xlsm %s named"%(sheet_name,xl)
        nrow = src_sheet.nrows
        ncol = src_sheet.ncols
        
        if xl == u'上线内容清单.xlsm' and nrow==9:
            continue
        if xl.find('CMB_RTL')!= -1 and nrow == 2:
            continue

        
        
        for i in range(start_read_row,nrow):
            for j in range(0,ncol):
                table.write(start_row,j,src_sheet.cell(i,j).value)
            start_row += 1
            
    save_path = 'D:\\SDM\\'+date_online+'\\'+ xl[:-1]
    file.save(save_path)


















