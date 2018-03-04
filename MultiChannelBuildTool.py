# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import zipfile
import shutil
import os

# 空文件 便于写入此空文件到apk包中作为channel文件
src_empty_file = 'info/czt.txt'
# 创建一个空文件（不存在则创建）
f = open(src_empty_file, 'w')
f.close()

# 获取当前目录中所有的apk源包
src_apks = []
# python3 : os.listdir()即可，这里使用兼容Python2的os.listdir('.')
for file in os.listdir('.'):
    if os.path.isfile(file):
        extension = os.path.splitext(file)[1][1:]
        if extension in 'apk':
            src_apks.append(file)


def fileListPkg():
    # 获取渠道列表
    channel_file = 'info/channel.txt'
    f = open(channel_file)
    lines = f.readlines()
    f.close()

    for src_apk in src_apks:
        # file name (with extension)
        src_apk_file_name = os.path.basename(src_apk)
        # 分割文件名与后缀
        temp_list = os.path.splitext(src_apk_file_name)
        # name without extension
        src_apk_name = temp_list[0]
        # 后缀名，包含.   例如: ".apk "
        src_apk_extension = temp_list[1]

        # 创建生成目录,与文件名相关
        output_dir = 'output_' + src_apk_name + '/'
        # 目录不存在则创建
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # 遍历渠道号并创建对应渠道号的apk文件
        for line in lines:
            # 获取当前渠道号，因为从渠道文件中获得带有\n,所有strip一下
            target_channel = line.strip()
            # 拼接对应渠道号的apk
            target_apk = output_dir + src_apk_name + "-" + target_channel + src_apk_extension
            # 拷贝建立新apk
            shutil.copy(src_apk, target_apk)
            # zip获取新建立的apk文件
            zipped = zipfile.ZipFile(target_apk, 'a', zipfile.ZIP_DEFLATED)
            # 初始化渠道信息
            empty_channel_file = "META-INF/cztchannel_{channel}".format(channel=target_channel)
            # 写入渠道信息
            zipped.write(src_empty_file, empty_channel_file)
            # 关闭zip流
            zipped.close()

    print u'打包完成'.decode('utf-8')
    os.system("pause")


def inputListPkg(fName, sNum, eNum):
    for src_apk in src_apks:
        # file name (with extension)
        src_apk_file_name = os.path.basename(src_apk)
        # 分割文件名与后缀
        temp_list = os.path.splitext(src_apk_file_name)
        # name without extension
        src_apk_name = temp_list[0]
        # 后缀名，包含.   例如: ".apk "
        src_apk_extension = temp_list[1]

        # 创建生成目录,与文件名相关
        output_dir = 'output_' + src_apk_name + '/'
        # 目录不存在则创建
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # 遍历渠道号并创建对应渠道号的apk文件
        for i in range(sNum, eNum + 1):
            # 拼接渠道名
            target_channel = fName + '_' + str(i)
            # 拼接对应渠道号的apk
            target_apk = output_dir + src_apk_name + "-" + target_channel + src_apk_extension
            # 拷贝建立新apk
            shutil.copy(src_apk, target_apk)
            # zip获取新建立的apk文件
            zipped = zipfile.ZipFile(target_apk, 'a', zipfile.ZIP_DEFLATED)
            # 初始化渠道信息
            empty_channel_file = "META-INF/cztchannel_{channel}".format(channel=target_channel)
            # 写入渠道信息
            zipped.write(src_empty_file, empty_channel_file)
            # 关闭zip流
            zipped.close()

    print u'打包完成'.decode('utf-8')
    os.system("pause")


if __name__ == '__main__':
    print u'\n\n\n--------------------- 欢迎使用批量打包工具 ---------------------\n\n\n'.decode('utf-8')
    x = raw_input(unicode('请输入打包方式：1、根据名称文件打包  2、自定义打包:\n','utf-8').encode('gbk'))
    if x == '1':
        print u'正在进行名称打包...请稍后'.decode('utf-8')
        fileListPkg()
    elif x == '2':
        firstName = raw_input(unicode('请输入渠道前缀\n','utf-8').encode('gbk'))
        startNum = int(raw_input(unicode('请输入后缀起始值\n','utf-8').encode('gbk')))
        endNum = int(raw_input(unicode('请输入后缀结束值\n','utf-8').encode('gbk')))
        print u'正在打包' + str(endNum - startNum) + '个文件...请稍后'.decode('utf-8')
        inputListPkg(firstName, startNum, endNum)
    else:
        print u'输入错误'.decode('utf-8')
