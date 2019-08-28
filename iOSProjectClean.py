#!/usr/bin/python
# -*- coding :utf-8 -*-
#

import os
import shutil
import sys 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f','--file', default='./',help='Your project path.Deafult curent ./ path. ')
parser.add_argument('-i','--ignore',nargs = '*', default=[], help='Igonre list.')

args = parser.parse_args()

_resNameMap = {}
_hadDelMap = {}
_isCleaning = False
_projectPbxprojPath = ''
_file_dir = ''

#过滤文件类型
def isResource(file_path):
	if os.path.isfile(file_path):
		if '.mp4' in file_path or '.png' in file_path or '@2x' in file_path or '@3x' in file_path or '@1x' in file_path or '.mp3' in file_path or 'png' in file_path or 'jpg' in file_path or 'gif' in file_path:
			return True
	return False

#查询全部文件
def searchAllResName(file_dir):
		
		fs = os.listdir(file_dir)
		for dir in fs:

			tmp_path = os.path.join(file_dir,dir)
			
			if not os.path.isdir(tmp_path):
				if isResource(tmp_path) == True and '/Pods/' not in tmp_path and '.appiconset' not in tmp_path and '.launchimage' not in tmp_path:
					imageName = tmp_path.split('/')[-1].split('.')[0]
					_resNameMap[imageName] = tmp_path
					

			elif os.path.isdir(tmp_path) and tmp_path.endswith('.imageset') and '/Pods/' not in tmp_path:
				imageName = tmp_path.split('/')[-1].split('.')[0]
				_resNameMap[imageName] = tmp_path
				

			else:
				searchAllResName(tmp_path)

#搜索工程目录文件地址
def serachProjectCode(file_dir):

	global _projectPbxprojPath

	fs = os.listdir(file_dir)
	for dir in fs:
		tmp_path = os.path.join(file_dir,dir)
		
		if tmp_path.endswith('project.pbxproj') and '/Pods/' not in tmp_path:
			print(tmp_path)
			_projectPbxprojPath = tmp_path

		if not os.path.isdir(tmp_path):
			if '/Pods/' not in tmp_path:
				try:
					findResNameAtFileLine(tmp_path)
				except Exception as e:
					pass
				else:
					pass
				finally:
					pass
		else:
			serachProjectCode(tmp_path)
#查询资源是否被使用
def findResNameAtFileLine(tmp_path):
	global _resNameMap
	Ropen = open(tmp_path,'r')
	for line in Ropen:
		lineList = line.split('"')
		for item in lineList:
			if item in _resNameMap or item.split('.')[0] in _resNameMap or item + '@1x' in _resNameMap or item + '@2x' in _resNameMap or item+'@3x' in _resNameMap:
				del _resNameMap[item]
				
	Ropen.close()

#删除全部无效资源
def delAllRubRes():
	global _resNameMap, _hadDelMap

	for resName in list(_resNameMap.keys()):
		tmp_path = _resNameMap[resName]
		if tmp_path.endswith('.imageset'):
			if os.path.exists(tmp_path) and os.path.isdir(tmp_path):
				try:
					_hadDelMap[resName] = tmp_path
					delImagesetFolder(tmp_path)
					del _resNameMap[resName]
					print('[del rub res ok]' + tmp_path)
				except OSError as e:
					print('[del rub res fail]['+ str(e) +']' + tmp_path)
			else:
				print('[del rub res fail][not exists]' + tmp_path)

	delResAtProjectPbxproj()
	
#删除imageset
def delImagesetFolder(rootdir):
	fileList = []
	fileList = os.listdir(rootdir)

	for f in fileList:
		fielpath = os.path.join(rootdir,f)
		
		if os.path.isfile(fielpath):
			os.remove(fielpath)
		elif os.path.isfile(fielpath):
			shutil.rmtree(fielpath,True)
	shutil.rmtree(rootdir,True)

#删除工程文件中无效引用且删除资源文件
def delResAtProjectPbxproj():
	global _projectPbxprojPath
	print(_projectPbxprojPath+'-'*10+'_projectPbxprojPath'+'-'*10)
	if _projectPbxprojPath != None:
		# 需要删除的先备份
		_needDelResName = []

		file_data = ''
		Ropen = open(_projectPbxprojPath,'r')
		for line in Ropen:
			idAdd = True
			for resName in _resNameMap:
				if resName in line:
					idAdd = False
					if resName not in _needDelResName:
						_needDelResName.append(resName)

			if idAdd == True:
				file_data += line
		Ropen.close()

		Wopen = open(_projectPbxprojPath,'w')
		Wopen.write(file_data)
		Wopen.close()
		# 已清理过 project.pbxproj 中引用的资源文件,开始从_resNameMap中移除已被处理过的资源文件
		# 并删除本地对应资源文件
		for item in _needDelResName:
			tmp_path = _resNameMap[item]
			if os.path.exists(tmp_path) and not os.path.isdir(tmp_path):
				#已删除的元素
				_hadDelMap[item] = tmp_path
				os.remove(tmp_path)
				del _resNameMap[item]

				print('[del rub res ok]' + tmp_path)
			else:
				pass
#执行方法
def starCleanRubRes(file_dir,ignoreList):
	global _isCleaning
	if _isCleaning == True:
		return
	_isCleaning = True
	
	print('-'*30 + '开始清理资源文件' + '-'*30)
	serachProjectCode(file_dir)
	if _projectPbxprojPath is None:
		print('Please enter effective paht.')
		return
	searchAllResName(file_dir)
	print('-'*20 + '全部资源文件列表' + '-'*20)
	print(_resNameMap)
	for x in ignoreList:
		if  item in list(_resNameMap.keys()):
			del _resNameMap[item]
	print(ignoreList)
	print(file_dir)
	print('-'*20 + '需要删除的文件 start' + '-'*20)
	for t in list(_resNameMap.keys()):
		print(t+'\n')
	print('-'*20 + '需要删除的文件 end' + '-'*20)
	
	delAllRubRes()
	print('-'*20 + '删除成功的资源文件' + '-'*20)
	print(_hadDelMap)
	print('-'*20 + '删除失败的资源文件' + '-'*20)


def main():
	
	starCleanRubRes(args.file,args.ignore)
	
if __name__ == '__main__':
	main()





