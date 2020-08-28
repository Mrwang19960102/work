# -*- coding: utf-8 -*-
# @File:       |   project_cfg.py 
# @Date:       |   2020/7/20 11:20
# @Author:     |   ThinkPad
# @Desc:       |  
import os
import configparser

projtecName = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).split('\\')[-1]

currPath = os.path.dirname(os.path.abspath(__file__))
projectRoot = currPath[:currPath.find(projtecName)+len(projtecName)]
# 读取配置文件信息
projectCF = configparser.ConfigParser()
projectCF.read(projectRoot+'/conf/conf.cfg')