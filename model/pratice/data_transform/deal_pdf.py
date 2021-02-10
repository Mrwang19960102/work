# -*- coding: utf-8 -*-
# @File:       |   deal_pdf.py 
# @Date:       |   2021/1/15 12:53
# @Author:     |   ThinkPad
# @Desc:       |  
import os
from win32com.client import Dispatch, constants, gencache, DispatchEx


class PDFConverter:
    def __init__(self, pathname, sheetnum, export='.'):
        self.sheetnum = sheetnum
        self._handle_postfix = ['xls', 'xlsx']
        self._filename_list = list()
        self._export_folder = os.path.join(os.path.abspath('.'), 'pdf文件夹')
        if not os.path.exists(self._export_folder):
            os.mkdir(self._export_folder)
        self._enumerate_filename(pathname)

    def _enumerate_filename(self, pathname):
        '''
        读取所有文件名
        '''
        full_pathname = os.path.abspath(pathname)
        if os.path.isfile(full_pathname):
            if self._is_legal_postfix(full_pathname):
                self._filename_list.append(full_pathname)
            else:
                raise TypeError('文件 {} 后缀名不合法！仅支持如下文件类型：{}。'.format(pathname, '、'.join(self._handle_postfix)))
        elif os.path.isdir(full_pathname):
            for relpath, _, files in os.walk(full_pathname):
                for name in files:
                    filename = os.path.join(full_pathname, relpath, name)
                    if self._is_legal_postfix(filename):
                        self._filename_list.append(os.path.join(filename))
        else:
            raise TypeError('文件/文件夹 {} 不存在或不合法！'.format(pathname))

    def _is_legal_postfix(self, filename):
        return filename.split('.')[-1].lower() in self._handle_postfix and not os.path.basename(filename).startswith(
            '~')

    def run_conver(self):
        '''
        进行批量处理，根据后缀名调用函数执行转换
        '''
        print('需要转换的文件数：', len(self._filename_list))
        for filename in self._filename_list:
            postfix = filename.split('.')[-1].lower()
            funcCall = getattr(self, postfix)
            print('原文件：', filename)
            funcCall(filename)
        print('转换完成！')

    def xls(self, filename):
        '''
        xls 和 xlsx 文件转换
        '''
        xlApp = DispatchEx("Excel.Application")
        xlApp.Visible = False
        xlApp.DisplayAlerts = 0
        books = xlApp.Workbooks.Open(filename, False)
        # 循环保存每一个sheet
        for i in range(1, self.sheetnum + 1):
            sheetName = books.Sheets(i).Name
            xlSheet = books.Worksheets(sheetName)
            name = sheetName + '.pdf'
            exportfile = os.path.join(self._export_folder, name)
            xlSheet.ExportAsFixedFormat(0, exportfile)
            print('保存 PDF 文件：', exportfile)
        books.Close(False)
        xlApp.Quit()

    def xlsx(self, filename):
        self.xls(filename)
