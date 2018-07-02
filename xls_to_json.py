#!/usr/bin/env python
# -*- coding: utf-8 -*-
#读取Excel表格中的信息，并将信息写入json文件中
from collections import OrderedDict
from pyexcel_xls import get_data
from pyexcel_xls import save_data
import json
map_filename='editor\\地图信息.xlsx'
current_sheet=1
while True:
	xls_data=get_data(map_filename)
	messages=xls_data[str(current_sheet)]
	save_filename='informations\\maps\\'+str(current_sheet)+'.json'
	with open(save_filename,'w') as f:
		json.dump(messages,f)
	current_sheet+=1
	if current_sheet==7:
		break

monster_filename='editor\怪物信息.xlsx'
current_sheet=1
while True:
	xls_data=get_data(monster_filename)
	messages=xls_data[str(current_sheet)]
	del messages[0]
	save_filename='informations\\monsters\\'+str(current_sheet)+'.json'
	with open(save_filename,'w') as f:
		json.dump(messages,f)
	current_sheet+=1
	if current_sheet==7:
		break

print('finished')
