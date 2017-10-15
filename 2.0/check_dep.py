# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 16:54:33 2017

@author: 80374769
"""


import xlrd
import re

#检查作业是否有在线区依赖近线区的
def sel_dsql_his_flag(up_dsql,down_dsql):
	import MySQLdb
	conn= MySQLdb.connect(
			host='localhost',
			port = 3306,
			user='root',
			passwd='xxxx',
			db ='test',
			)

	cur = conn.cursor()

#检查上游依赖的作业是否是在线区：	
	sel_sql = "select his_flag from artp_dsql_dep_his where dsql_name='%s'"%up_dsql
	
	res = cur.execute(sel_sql)
	flag = cur.fetchmany(res)
	


	ret = 0
	if len(flag) == 0:
		ret =  -1
		
		print u'   %s  作业没上线>>>>>>>>'%up_dsql
	elif flag[0][0] == '0':
		ret = 0 
		#print u' %s  作业在在线区'%up_dsql
	elif flag[0][0] == '1':
		ret = 1
		print u'    在线区作业%s 依赖近线区作业%s>>>>>>>>'%(down_dsql,up_dsql)
#检查下游作业是否已经在维护表里，如果不在，插入到维护表artp_dsql_dep_his
	sel_sql = "select his_flag from artp_dsql_dep_his where dsql_name='%s'"%down_dsql
	res = cur.execute(sel_sql)
	flag = cur.fetchmany(res)

	if len(flag) == 0:
		insert_sql = "insert into artp_dsql_dep_his(dsql_name,his_flag) values('%s','%s')"%(down_dsql,'0')
		cur.execute(insert_sql)

	cur.close()
	conn.commit()
	conn.close()

	return ret


#检查依赖填写情况
def check_dep(dir_path,filename,dsql_test_set,depend_dsql_set):
    

	#print filename.decode('gb2312').encode('utf-8')
	data = xlrd.open_workbook(dir_path+'\\'+filename)
	table1 = data.sheet_by_name(u'作业关系配置变更')
	#table2 = data.sheet_by_name(u'下线作业列表')
	dsql1_dsql2_set = set()
	dsql_new_flag = {}

	if  table1.nrows>2:
		print filename,u' 检查: '
	else:
		print filename,u'无填写内容\n'
		return 0
	for i in range(2,table1.nrows):
		dsql1_name = table1.cell(i,0).value
		dsql1_flag = table1.cell(i,1).value

		dsql2_name = table1.cell(i,2).value
		dsql2_flag = table1.cell(i,3).value
		add_del = table1.cell(i,6).value

		dsql1_dsql2 = dsql1_name + dsql2_name
		id_name = table1.cell(i,8).value
		author_id  = table1.cell(i,9).value

		run_fq = table1.cell(i,5).value
		run_day = str(table1.cell(i,11).value)

		if run_fq == 'M' and len(run_day)<1:
			print i+1,u'  月调度未填写具体调度日期    ',id_name

		if dsql1_flag == 'Y' and dsql1_name.lower() not in dsql_test_set:
			#print dsql1_name.lower()
			print i,dsql1_name,id_name,u'作业新上线，不在打包内容里!!!!>>>>'
		if dsql2_flag == 'Y' and dsql2_name.lower() not in dsql_test_set:
			#print dsql2_name.lower()
			print i,dsql2_name,id_name,u'作业新上线，不在打包内容里!!!!>>>>'

		if str(int(author_id)) not in id_name_set.keys():     #and type(author_id) != float:
			#print type(author_id)
			print u'依赖变更: ididididid作业一事通号码不正确：>>>>>'
			print '     ',i+1,'id is: ',int(author_id),'    ',table1.cell(i,10).value,id_name
		if dsql1_name[0:11] not in artp_head_set or dsql2_name[0:11] not in artp_head_set:
			print u'依赖变更: !!!!!!!!!!!作业前缀不正确：>>>>>'
			print '  ',i,dsql1_name,dsql2_name,id_name
		if len(re.findall('[a-z]',dsql1_name))>0 or len(re.findall('[a-z]',dsql2_name))>0:
			print u'依赖变更: @@@@@@@@@@@@作业名没有完全大写>>>>>>：'
			print '  ',i+1,dsql1_name,dsql2_name,id_name

		if dsql1_dsql2 not in dsql1_dsql2_set:
			dsql1_dsql2_set.add(dsql1_dsql2)
		else:
			print u'依赖变更: $$$$$$$$$$$$$依赖填写重复：>>>>>>'
			print '  ',i+1,dsql1_name,dsql2_name,id_name
		if (dsql1_flag=='Y'or dsql2_flag=='Y') and add_del == 'DEL' :
			print u'新上线作业，就删除依赖，傻逼吗!!!!!!!!!!'
			print '  ' ,i+1,dsql1_name,dsql2_name,id_name
			
			
		if dsql1_name not in dsql_new_flag.keys():
			dsql_new_flag[dsql1_name] = dsql1_flag
		else:
			if dsql_new_flag[dsql1_name] != dsql1_flag:
				print i+1,' ',dsql1_name,u'作业是否新增前后不一致',id_name
		if dsql2_name not in dsql_new_flag.keys():
			dsql_new_flag[dsql2_name] = dsql2_flag
		else:
			if dsql_new_flag[dsql2_name] != dsql2_flag:
				print i+1,' ',dsql2_name,u'作业是否新增前后不一致',id_name
				
		
		if dsql1_flag == 'Y' and dsql2_flag == 'N' and dsql2_name.find('ARTP') !=-1 :
			sel_dsql_his_flag(dsql2_name , dsql1_name)

		if dsql1_name not in  depend_dsql_set:
			depend_dsql_set.add(dsql1_name)
		if dsql2_name not in depend_dsql_set:
			depend_dsql_set.add(dsql2_name)
		
	print '---------------------------------check done!\n'

#检查作业清单填写情况;


def check_list(dir_path,filename):

    data = xlrd.open_workbook(dir_path+ '\\'+ filename)
    table = data.sheet_by_name(u'上线内容清单')


    if table.nrows > 8:
        print filename,u' 检查: '
    else:
         return 0

    bao_set = set()
    

    for i in range(9,table.nrows):


		cls = table.cell(i,0).value
		author = table.cell(i,2).value
		#nbr = table.cell(i,3).value
		dsql_name = table.cell(i,1).value
		

		#bao_author[dsql_name] = author
		#pvt_author[dsql_name] = author

		if dsql_name not in bao_set:
			bao_set.add(dsql_name)
		else:
			print i,dsql_name,author,u'填写重复'

		if len(author) < 1:
			print i+1,u'---------负责人没有填写-------'
			


    print '---------------------------------check done！\n'
	




def sel_new_dsql(dsql_test_set):
	import MySQLdb
	conn= MySQLdb.connect(
			host='localhost',
			port = 3306,
			user='root',
			passwd='xxxx',
			db ='test',
			)

	cur = conn.cursor()

	new_dsql_list = []
                                 
                        
	for dsql in dsql_test_set:
		recd_num = cur.execute("select * from artp_list where dsql_name='%s'"%dsql)
		dsql_no_dis = cur.fetchmany(recd_num)
			#print dsql_no_dis[0][0]
		if len(dsql_no_dis[0])<0:
			new_dsql_list.append(dsql)
			print u'新上线的DSQL:'
			print dsql

	cur.close()
	conn.commit()
	conn.close()

	return new_dsql_list

'''
检查填写错误3333333333333333333333
'''




dsql_new_set = {}
depend_dsql_set = set()



for filename in os.listdir(dir_1):
    
	'''
	*************************************对依赖变更进行检查**********************
	'''
 
	if filename.find(u'CMB_RTL作业依赖变更登记表') != -1:
		check_dep(dir_1,filename,dsql_test_set,depend_dsql_set)
#
	'''
	*****************对上线清单进行检查*****************************************
	'''
	if filename.find(u'上线内容清单.xlsm') != -1 :
		check_list(dir_1,filename )
  