# -*- coding: utf-8 -*-
# !/usr/bin/env python3
###########################import package###################
import os
import pathlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# https://blog.csdn.net/geek64581/article/details/106052164
# matplotlib 中文字体解决方法
import matplotlib as mpl
import json
import re
import sys
# 解析命令行的工具
import argparse
from typing import Union # python3 类型检查
from typing import List, Dict, Tuple, Generator, Callable
import logging
import time
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
import click
from pathlib import Path
import datetime
# 处理中国节假日的包
from chinese_calendar import is_workday, is_holiday
import unittest
import gzip
from multiprocessing import Pool, cpu_count
import requests
from bs4 import BeautifulSoup
###########################import package###################

# 获取用户的家目录
HOME = os.path.expanduser("~")
_PROJECT_DIR = Path(__file__).parent.parent
PROJECT_DIR = _PROJECT_DIR
_PROJECT_LOG_DIR = _PROJECT_DIR / "log"
# 将一个列表套列表的对象展开（展开嵌套列表）
def flat(nums):
    res = []
    for i in nums:
        if isinstance(i, list):
            res.extend(flat(i))
        else:
            res.append(i)
    return res

# 将字符串中的英文标点符号转化为中文标点， 并将句子以中文句号结尾；
def change_en_to_cn_punctuation(string):
    new_string = string.replace(".","。").replace(",", "，").replace(":", "：").replace(";", "；").replace("\"","“").replace("!","！")
    if new_string.endswith("；"):
        new_string = new_string.replace("；","。")
    elif new_string.endswith("。"):
        pass
    else:
        new_string = new_string +"。"
    return new_string

# 讲一个python对象写入json文件中
# v1 to_json_file 20210201 废弃
def to_json_file(obj_name, file_name):
    with open(file_name, 'w') as f:
        json.dump(obj_name, f, ensure_ascii=False, indent=4)

class NpEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, set):
            return list(obj)
        else:
            return super(NpEncoder, self).default(obj)

# write a complex data to a json file
def obj_to_json(obj, file_path):
    json_str = json.dumps(obj, indent=4, cls=NpEncoder, ensure_ascii=False)
    with open(file_path, 'w') as json_file:
        json_file.write(json_str)

# read a object form json file
def json_file_to_obj(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# 创建目录，如果目录不存在则创建，如果目录存在则不做任何操作
def mkdir(outdir):
    try:
        os.makedirs(outdir)
        # os.mkdir(outdir)
    except FileExistsError:
        # print("{} exist...".format(outdir))
        pass

###########################在bash中执行命令 start##########################
# 运行没有返回值（不需要在执行后的返回值）的命令
def run_command(command: str):
    if os.system(command) == 0 :
        return True
    else:
        return False

# 运行具有返回值（在命令行输出的值）的命令
def run_command_popen(command: str) -> str:
    return os.popen(command).read()

def run_command_status(command: str) -> Union[str, None]:
    import subprocess
    status, res = subprocess.getstatusoutput(command)
    if status == 0:
        return res
    else:
        return None
###########################在bash中执行命令 end##########################
# 获取今天的字符串: 2021_01_15
def get_today_str() -> str:
    import time
    return time.strftime("%Y_%m_%d",time.localtime(time.time()))

# 获取程序运行时刻的时间字符串: 2020-12-18T14:47:23.226216
def get_now_str() -> str:
    import datetime
    return datetime.datetime.now().isoformat().replace(':', '_')

# 从文件中读取表型结构数据
def read_data(fpath: str) -> pd.DataFrame:
    if fpath.endswith('gz'):
        try:
            df = pd.read_excel(fpath,compression='gzip')
        except:
            df = pd.read_csv(fpath, sep='\t',compression='gzip')
    else:
        try:
            df = pd.read_excel(fpath)
        except:
            df = pd.read_csv(fpath, sep='\t')
    # 这个是什么意思？
    dica = {}
    for key in df.keys():
        dica[key] =str(key)
    if dica:
        df.rename(columns=dica,inplace=True)
    return df

# 获取目录下的所有文件（包括子目录的文件）
def walks(path_dir, #文件夹路径
          file_name, # 要搜索的文件名
          fileend, # 要搜索的文件后缀名
          ):
    import os
    file_path = []
    a = os.walk(path_dir)
    for root, dirs, files in a:
        for name in files:
            if file_name:
                if name == file_name:
                    file_path.append(os.path.join(root, name))
            elif fileend:
                if name.endswith(fileend):
                    file_path.append(os.path.join(root, name))
            else:
                file_path.append(os.path.join(root, name))
    return file_path


# 将路径里面的不合法字符替换为合法字符
def path_remake(path):
    return path.replace(' ', '\ ').replace('(','\(').replace(')','\)').replace('&','\&')

# 将pdf文件合并到一起
def merge_pdf_file(pdf_list_join:list=None, # 待合并的文件列表
                   pdf_dir:str=None, # 待合并的文件所在的文件夹路径
                   out_path_file_name:str=None # 生成的文件的路径和名称
                   ):
    if out_path_file_name:
        pass
    else:
        print("您没有指定生成的文件夹路径，默认文件夹名字为：default.pdf。")
        out_path_file_name = "default.pdf"
    # 待合并文件列表
    pdf_merge_list = []
    # 如果pdf_list_join中有文件
        # 判断是否为列表，如何不为列表则抛出错误
    if isinstance(pdf_list_join, list):
        for item in pdf_list_join:
            item = path_remake(item)
            if os.path.split(item)[-1].endswith('.pdf'):
                pdf_merge_list.append(item)
    else:
        raise("'pdf_list_join' must be a list!!!!!")
    # 如果存在pdf_dir，则遍历其中的pdf文件，
        # 否则抛出文件不存在的错误
    if os.access(pdf_dir, os.F_OK):
        temp_list = walks(pdf_dir, None, '.pdf')
        for item in temp_list:
            item = path_remake(item)
            if os.path.split(item)[-1].endswith('.pdf'):
                pdf_merge_list.append(item)
    else:
        raise (f"{pdf_dir} not exist!!!!!")
    if not pdf_merge_list:
        os.system(f'gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile={out_path_file_name} -f {" ".join(pdf_merge_list)}')

# 提取pdf中的页面
def split_pdf_file(pdf_path:str=None, # 原始文件路径
                   out_pdf_path:str=None, # 提取后的文件路径
                   start_page:int=None, # 提取的开始页面
                   end_page:int=None): # 提取的结束页面
    if pdf_path and out_pdf_path and start_page and end_page:
            os.system(f'gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile={out_pdf_path} -dFirstPage={str(start_page)} -dLastPage={str(end_page)} {pdf_path}')
    else:
        raise ("您有参数没有传入。")

# 装饰器：用于统计从；程序运行的时间
def timethis(func):
    from functools import wraps
    import time
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print("use time：",end-start)
        return r
    return wrapper
#############################################

# 绘图函数区 start
def draw_pie(labels=None, # 每份数据的标签
             quants=None, # 数据组成的列表
             title_name="未知标题", # 饼图的标题
             colors=None, # 显示的颜色列表，循环显示列表
             highlight=None, # 突出显示
             deviation_distance=0.1, # 突出显示的块离圆心的距离
             png_path = "pie.jpg"
             ):
    # make a square figure
    if quants is None:
        quants = []
    if len(labels) != len(quants):
        raise Exception("quants和labels列表长度不相同！")
    # 如何自定义图片的大小，根据数据大小自适应？？？？？？
    plt.figure(1, figsize=(6,6))
    # 将图分多少份；
    split_pie_num = len(quants)
    # 如何创建一个初始值为0的大小为split_pie_num的列表
    expl = [0 for item in range(split_pie_num)]
    # 如何找到那个分组的数最大，及其下标
    import heapq
    highlight = highlight if highlight else 0
    for item in range(highlight):
        max_index = list(map(quants.index, heapq.nlargest(3, quants)))[item]
        expl[max_index] = deviation_distance

    # Colors used. Recycle if not enough.
    colors  = colors if colors else ["blue","red","coral","green","yellow","orange"]  #设置颜色（循环显示）
    # Pie Plot
    # autopct: format of "percent" string;百分数格式
    plt.pie(quants, explode=expl, colors=colors, labels=labels, autopct='%1.1f%%',pctdistance=0.8, shadow=True)
    plt.title(title_name, bbox={'facecolor':'0.8', 'pad':5})
    plt.savefig(png_path)
    # plt.show()
    plt.close()
# 绘图函数区 end
##########################tag：数据分析#################################
# 对table型文件的处理函数区 start
# 将列表转化为以tab分割的字符串
def list_to_line(column_list):
    column_list = (str(item).strip() for item in column_list)
    return '\t'.join(column_list)

# 将以tab分割的字符串(一般是从文件中读取的一行）转化为列表
def line_to_list(line):
    # return line.strip().split('\t')
    line_list = line.replace("\n", "").replace("\r", "").split("\t")
    return [item.strip() if item.strip() else "null" for item in line_list]

# 对dataframe按照列字段进行去重
def drop_duplicates(df, colums_name=None):
    if colums_name is None:
        return df.drop_duplicates(inplace=False)
    else:
        return df.drop_duplicates(subset=colums_name,keep='first',inplace=False)

# 将dataframe对象写到文件中
def df_to_tsv(df: pd.DataFrame, file_name=None):
    if file_name is None:
        file_name = 'default.tsv'
    df.to_csv(file_name, sep='\t', header=True, index=False)

def tsv_to_df(file_name: Union[str, pathlib.Path]) -> pd.DataFrame:
    return pd.read_csv(file_name, sep="\t")
# 将dataframe对象写到文件中
def df_to_excel(df, file_name=None, sheet_name=None):
    if file_name is None:
        file_name = 'default.exls'
    if sheet_name is None:
        sheet_name = "sheet1"
    df.to_excel(file_name, sheet_name=sheet_name, index=False)

# 多个dataframe对象写到一个excel文件中，
def dfs_to_one_excel(df_list=None, # dataframe列表
                     sheet_list=None, # 表单列表名称
                     excel_name=None, # 输出的excel文件名
                     df_sheet_map=None # [（df，sheet_name), ...]
                     ):
    if excel_name is None:
        excel_name = "default.exls"
    if df_sheet_map is not None:
        # 检查数据格式
        if isinstance(df_sheet_map, list):
            for item in df_sheet_map:
                isinstance(item, (list, tuple))
        else:
            print("df_sheet_map格式错误：需要有(df,sheet_nem)形式的元素组成的列表；")
        return
    else:
        if df_list is not None:
            if sheet_list is not None:
                if isinstance(df_list, (list, tuple))  and isinstance(sheet_list, (list, tuple)):
                    df_sheet_map = zip(df_list,sheet_list)
            else:
                if isinstance(df_list, list) or isinstance(df_list, tuple):
                    sheet_list = [ "sheet"+str(i) for i in range(len(df_list))]
                    df_sheet_map = list(zip(df_list,sheet_list))
        else:
            print("请传入dataframe对象列表！")
            return
    with pd.ExcelWriter(excel_name) as writer:
        for df, sheet_name in df_sheet_map:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

# 将一个列表形式的表格结构数据转化为dataframe数据结构
def listTable_to_df(listTable, # 表格[[],]
                    header=None, # 表格的第一行为columns
                    columns=None, # 指定表格的columns
                    ):
    if header==1:
        title_name = listTable[0]
        list_table = listTable[1:]
        return pd.DataFrame(list_table, columns=title_name)
    else:
        title_name = columns
        list_table = listTable
        return pd.DataFrame(list_table, columns=title_name)


# 对dataframe数据类型进行逐行迭代，对行数据进行操作后在将数据已dataframe数格式返回
def handle_data_by_row_df(df, # dataframe数据格式
                          handle_func # 行数据处理函数，接受一个series格式数据，并返回修改后的数据
                          ):
    series_list = []
    for _, row in df.iterrows():
        row = handle_func(row)
        series_list.append(row)
    df_out = pd.DataFrame(series_list)
    return df_out

# 删除dataframe数据表中某列值为是什么的行
def del_row_by_coloum_value(df:pd.DataFrame,column_index, column_value:list) ->pd.DataFrame:
    """
    删除dataframe数据表中某列值为是什么的行
    df = df[~df['pos'].isin(["-"])]
    :param df: pd.DataFrame
    :param column_index: 列的索引
    :param column_value: 包含要删除行中column_index值的列表
    :return: 删除不需要的行的新表
    """
    return df[~df[column_index].isin(column_value)]
# 只保留dataframe数据表中某列值使ＸＸ的行
def save_row_by_coloum_value(df:pd.DataFrame,column_index, column_value:list) ->pd.DataFrame:
    """
    只保留dataframe数据表中某列值使ＸＸ的行
    df = df[~df['pos'].isin(["-"])]
    :param df: pd.DataFrame
    :param column_index: 列的索引
    :param column_value: 包含要保留行中column_index值的列表
    :return: 保留需要的行的新表
    """
    return df[df[column_index].isin(column_value)]

# 如何使用
class MyJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, pd.DataFrame):
            return json.loads(obj.to_dict(orient="index"))
        return json.JSONEncoder.default(self, obj)

def df_to_json_file(df:pd.DataFrame, json_file_path:str)->None:
    """
    将一个pd.DataFrame对象写入json文件中
    :param df: pd.DataFrame对象
    :param json_file_path: 待写入文件的路径
    :return:
    """
    df.to_json(json_file_path, force_ascii=False, orient="records", indent=4)

def json_file_to_df(json_file_path:str) ->pd.DataFrame:
    """
    从json文件中读取表格型数据并返回pd.DataFrame对象
    :param json_file_path:
    :return:
    """
    with open(json_file_path, "r") as f:
        return pd.DataFrame(json.loads(f.read())).T

def df_to_dict(df: pd.DataFrame) -> dict:
    """
    从dataFrame生成字典，第一列为key，第二列为value
    | key | value |
    | --- | --- |
    | bar | 123 |
    | foo | 456 |
    >>> df = pd.DataFrame([{"key": "bar", "value": 123}, {"key": "foo", "value": 456}])
    >>> df
       key  value
    0  bar    123
    1  foo    456
    >>> df_to_dict(df)
    {'bar': 123, 'foo': 456}
    """
    return df.set_index([df.columns[0]])[df.columns[1]].to_dict()

def dict_to_df(dict: dict, columns=None) -> pd.DataFrame:
    """
    将key-value 字典形式的数据转换为dataFrame数据
    >>> foo = { "bar":123 , "foo": 456}
    >>> dict_to_df(foo, columns=["key", "value"])
       key  value
    0  bar    123
    1  foo    456
    """
    res = []
    if columns is None:
        columns = ["key", "value"]
    for key, value in dict.items():
        temp_dict = {}
        temp_dict[columns[0]] = key
        temp_dict[columns[1]] = value
        res.append(temp_dict)
    return pd.DataFrame(res)

# 将列表写到文件中
def list_to_file(list_obj: list, title: str, file_path: Union[str, Path]):
    df_to_tsv(pd.DataFrame(list_obj, columns=[title,]), file_path)

# 按照索引横向合并表格
def merge_two_df_by_left_index(df_left: pd.DataFrame, df_right: pd.DataFrame) -> pd.DataFrame:
    return pd.merge(df_left, df_right, right_index=True, left_index=True,)  # how='left'




def init_logger(logger_name, log_dir=_PROJECT_LOG_DIR):
    if logger_name not in Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        # handler all
        handler = TimedRotatingFileHandler( log_dir /'all.log', when='midnight',backupCount=7)
        datefmt = "%Y-%m-%d %H:%M:%S"
        format_str = "[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s"
        formatter = logging.Formatter(format_str, datefmt)
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        # handler error
        handler = TimedRotatingFileHandler( log_dir / 'error.log', when='midnight',backupCount=7)
        datefmt = "%Y-%m-%d %H:%M:%S"
        format_str = "[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s"
        formatter = logging.Formatter(format_str, datefmt)
        handler.setFormatter(formatter)
        handler.setLevel(logging.ERROR)
        logger.addHandler(handler)


    logger = logging.getLogger(logger_name)
    return logger

# how to use logging
# try:
#     ...
# except (SystemExit,KeyboardInterrupt):
#     raise
# except Exception:
#     logger.error("Faild to open sklearn.txt from logger.error",exc_info = True)
#     logger.exception("Faild to open sklearn.txt from logger.error")


# if __name__ == '__main__':
#     logger = init_logger("utils_slliu_test")
#     logger.error("test-error")
#     logger.info("test-info")
#     logger.warning("test-warn")



######################################
# 工具函数测试区
# if __name__ == '__main__':
#     labels   = ['USA', 'China', 'test']
#     quants   = [15094025.0, 11299967.0, 11299967.0 ]
#     title_name = 'usa china pie'
#     # colors = ['green', 'yellow']
#     colors = ['#BBFFFF', '#EE6363','#9400D3']
#     draw_pie(labels=labels,
#              quants=quants,
#              title_name=title_name,
#              colors=colors,
#              highlight=1)




