# iOSProjectClean
iOSProjectClean
###Python脚本 清理iOS项目里无用资源
####需求介绍
iOS项目迭代版本时间长，会有一部分冗余的资源（图片，视频，音频等），不及时清理会影响IPA包的大小。对引流和用户体验都有一定的影响，故写一脚本练习Python，并做点有意思的事情。

####功能分析
___
* *目标文件*

	   	已处理文件类型 .png .jpeg .mp3 .mp4 @1x @2x @3x .gif
	   	
	   	
		  
* <label style="color:black">大体思路</label>
			
        遍历所有文件并存入allMap
        筛选allMap中资源文件resourceMap
        筛选出resourceMap中未引用资源文件delMap
        清理delMap
          .imageset 直接删除文
          引用文件  先删除project.pbxproj引用,再删除文件
        清理完毕
      
* **代码结构**

		#过滤文件类型
		def	isResource(file_path) 
		
		#查询全部文件
		def searchAllResName(file_dir):
		
		#搜索工程目录文件地址
		def serachProjectCode(file_dir):

		#查询资源是否被使用
		def findResNameAtFileLine(tmp_path):
		
		#删除全部无效资源
		def delAllRubRes():
		
		#删除imageset
		def delImagesetFolder(rootdir):
		
		#删除工程文件中无效引用
		def delResAtProjectPbxproj():
		
		#执行方法
		def starCleanRubRes(file_dir,ignoreList):
<!--* Email:<fsl_666888@163.com>-->


