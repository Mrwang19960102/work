# -*- coding: utf-8 -*-
# @File:       |   shop_meituan.py 
# @Date:       |   2021/2/24 10:27
# @Author:     |   ThinkPad
# @Desc:       |  美团数据信息抓取
import os
import re
import time
import math
import copy
import random
import json
import requests
import pandas as pd
from lxml import etree
from datetime import datetime
from multiprocessing import Pool
from model.spider_data import tools, conf
from model.spider_data.dao import dbmanager_mt