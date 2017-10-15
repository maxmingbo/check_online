# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 15:30:08 2017

@author: 80374769
"""

import os
import time


def run_cmd(dsql_name):
	
	headstr = 'dsql -c D:\\online_test\\TD_LOGON.env -f D:\\online_test\\'
	cmd = headstr+dsql_name+'.dsql TX_DATE=20170531 > D:\\online_test\\'+dsql_name+".log"
#	if os.path.exists('D:\\online_test\\'+dsql+'.log'):
#		return 0


	os.popen(cmd)

def check_log_ok(dsql_path):
	f = open(dsql_path,"r")
	lines = f.readlines()#读取全部内容  
	f.close()
	if lines[-3].find('QUIT 0')!=-1 or lines[-3].find('quit 0')!=-1:
		return True
	else:
		print 'fail:'
		i = -8
		line_disorder = []
		while(lines[i].find('+---------+')==-1):
			line_disorder.append(lines[i])
			i = i-1
		while(not line_disorder == False and  line_disorder):
			print '    ',line_disorder[-1][:-1]
			line_disorder.pop()
			
		return False
def check_log_analyse(lines):
	pass
	
error_count = 0

f_error_dsql = open("D:\online_test\%s_error.txt"%date_online, 'w')

final_print_error = []


i = 0
for dsql in dsql_test_set:

	if  os.path.exists('D:\\online_test\\'+dsql+'.dsql'):
		run_cmd(dsql)
		time.sleep(0.2)
		i = i+1
		print i,
		if check_log_ok('D:\\online_test\\'+dsql+'.log'):
			print(dsql + '----PASS!')
		else:
			error_count += 1
			print(dsql + '---_FAIL!!!  '+ tvp_author[dsql.upper()])
			
			final_print_error.append(dsql + '---_FAIL!!!  '+ tvp_author[dsql.upper()])
			
			
			headstr = 'dsql -c D:\\online_test\\TD_LOGON.env -f D:\\online_test\\'
			cmd = headstr+dsql+'.dsql TX_DATE=20170531 > D:\\online_test\\'+dsql+".log"
			try:
				f_error_dsql.write(cmd+'\n')
			except:
				print('write backup error:')
		
	else:
		print(dsql+u'.dsql  ---文件不存在呀')
	
		
print '\n'
print u'  共 %d 个dsql报错 !!'%error_count

for er in final_print_error:
	print er

f_error_dsql.close()

		