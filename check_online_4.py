# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 10:48:58 2017

@author: 80374769
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 11:25:44 2017
对上线清单，依赖变更进行检查。
更改：2017/04/05
@author: 80374769
"""




'''
每次运行注意更改日期
'''
date_online = '20170928'


import os




artp_head_set = set(['ARTP_P_ARTP','ARTP_R_ARTP','BRTL_P_BRTL','NDS_C_NLF14','NDS_C_NLF54','NDS_C_NLU37',\
'NDS_C_NLF39','NDS_C_NS196','NDS_C_NL38','NDS_P_NLF14','NDS_P_NLA58','NDS_C_NSINT','NDS_C_NLR13',\
'NDS_P_NDS_P','NDS_P_NLF02','NDS_P_NLV20','NDS_C_NX102','NDS_P_NLH20','NDS_C_NX101','NDS_C_NLU60',\
'NDS_C_NLV27','NDS_P_NLN61','NDS_C_NLV24','NDS_C_NLV23','NDS_C_NLV22','NDS_C_NLV21','NDS_C_NLR14',\
'NDS_C_NLV20','NDS_C_NLF02','NDS_C_NLV25','NDS_C_NLV26','NDS_P_NLL56','NDS_P_NSINT','NDS_P_NLU60',\
'NDS_C_NB971','NDS_C_NLF53','NDS_P_NLF39','NDS_C_NLN57','NDS_P_NLN50','NDS_P_NLU77','NDS_C_NLR14',\
'DQC_C_KEY_A','SYS_FW_ARTP','ARTP_F_ARTP','SYS_FW_ARTP','NDS_C_NLV62','NDS_C_NLV48','NDS_C_NLH20',\
'NDS_C_NLU67','NDS_C_NLF33'])

id_name_set = {id_:name_}

all_id_name = {id_:name_}


dir_1 = u'D:/Firefly workspace/xxxx/01文档/09配置管理/03上线投产/'+date_online

tvp_author = {}

#集成包对应负责人

bao_author = {}




'''
#创建构建保存目录
如果存在，则不创建
'''
def creat_dir(date_online):

    dir_path = 'D:/RTC406Upgrade/' + date_online
    if os.path.exists(dir_path)!=True:
        os.makedirs(dir_path)
    dir_2 = dir_path + '/RTL2_TDW_ARTP'

    if os.path.exists(dir_2)!=True:
        os.makedirs(dir_2)
    dir_3_list = ['/DDL','/INIT']
    for dir_3 in dir_3_list:
        dir_3 = dir_2 + dir_3
        if os.path.exists(dir_3)!=True:
            os.makedirs(dir_3)

creat_dir(date_online)





"""2222222222
读取清单
保存dsql_test_set,写成测试清单
"""
import csv
import pandas as pd

dsql_test_set = set()

date_1 = str(int(date_online)-1)

csv_path = 'D:/RTC406Upgrade/RTL2_%s_01_InteObjList.csv'%date_1

if os.path.exists(csv_path)==False:
	print u'作业清单列表文件不存在!!!'
else:
	csvfile = file(csv_path, 'rb')
	reader = csv.reader(csvfile)
	
	cls_set = {}
#统计表，视图，作业，数量
i = 0
for row in reader:
	i += 1
	if i < 2:
		continue
	online_class = row[2]
	bao_name = row[1]
	bao_name_id = row[1].split('_')[-2]
	ob_name = row[4]
    
    
	
	if online_class.decode('gb2312') == u'作业':
		dsql_test_set.add(ob_name.lower())
  
	if online_class not in cls_set.keys():
		cls_set[online_class] = 1
	else:
		cls_set[online_class] += 1

	tvp_author[ob_name] = all_id_name[bao_name_id]

print '------------------'
for k in cls_set.keys():        
    print  k.decode('gb2312'),'  numbers is : ', int(cls_set[k])
print '------------------'

ft = open("D:\online_test\%s.txt"%date_online, 'w')

for entry in dsql_test_set:

	headstr = 'dsql -c D:\\online_test\\TD_LOGON.env -f D:\\online_test\\'
	write_str = headstr+entry.lower()+'.dsql TX_DATE=20170501 > D:\\online_test\\'+entry.lower()+".log"

	try:
		ft.write(write_str+'\n')
	except:
		print('write backup error:')
    #ft.write(write_str)
print '\n测试命令写入完成'
ft.close()



f_author = open("D:\RTC406Upgrade\%s_author.txt"%date_online, 'w+')
#import sys
#reload(sys) 
#sys.setdefaultencoding('utf-8')

for k in cls_set.keys():
	#print  k.decode('gb2312'),'  numbers is : ', int(cls_set[k])
	w_str = '%s,   %s'%(k,cls_set[k])
	try:
		f_author.writelines(w_str)
		f_author.writelines('\n')
	except:
		print('write backup error:')
    #ft.write(write_str)

f_author.writelines('\n')
#for k_dsql,val in tvp_author.items():
#    print val
#    #tvp_author[k_dsql] = bao_author[val].decode('gb2312')
#    w_str = u'%s,   %s'%(k_dsql, tvp_author[k_dsql])
#    
#    try:
#        f_author.write(w_str+'\n')
#    except:
#		print('write backup error:')
#
#print '\n上线负责人，内容，写入完成'
f_author.close()









