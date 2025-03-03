
import tensorflow as tf
import os
import config
paras = config.get_configs()
data_name = paras['data_name']
idxx = 0

idnum = 0
def get_nb_view_by_individal_code(code):
    nb_view = (len(code) + 1) // 2  # 视图个数
    return nb_view
def write_result_file(str, fn='result.csv'):
    with open(fn, 'a+') as f:
        f.write(str)
        f.write('\n')
        f.flush()
def load_result_new(result_fn=os.path.join(data_name+'_view_result', paras['result_save_dir'], 'result.csv')):
    shared_code_acc = {}
    shared_code_acc_set = set()
    with open(result_fn) as f:
        for item in f.readlines():
            items = item.strip().split(',')
            if items[0][:-2] not in shared_code_acc_set:
                shared_code_acc[items[0][:-2]] = float(items[1])
                shared_code_acc_set.add(items[0][:-2])
    return shared_code_acc


def load_result_new_par(result_fn=os.path.join(data_name+'_view_result', paras['result_save_dir'], 'result.csv')):
    shared_code_acc = {}
    shared_code_acc_set = set()
    with open(result_fn) as f:
        for item in f.readlines():
            items = item.strip().split(',')
            if items[0][:-2] not in shared_code_acc_set:
                shared_code_acc[items[0][:-2]] = float(items[3])
                shared_code_acc_set.add(items[0][:-2])
    return shared_code_acc

def load_result(result_fn=os.path.join(data_name+'_view_result', paras['result_save_dir'], 'result.csv')):
    shared_code_acc = {}
    shared_code_acc_set = set()
    with open(result_fn) as f:
        for item in f.readlines():
            items = item.strip().split(',')
            if items[0]not in shared_code_acc_set:
                shared_code_acc[items[0]] = float(items[1])
                shared_code_acc_set.add(items[0])
    return shared_code_acc




def load_result_Acc(result_fn=os.path.join(data_name+'_view_result', paras['result_save_dir'], 'result.csv')):
    shared_code_acc = {}
    shared_code_acc_set = set()
    with open(result_fn) as f:
        for item in f.readlines():
            items = item.strip().split(',')
            if items[0] not in shared_code_acc_set:
                shared_code_acc[items[0]] = float(items[1])
                shared_code_acc_set.add(items[0])
    return shared_code_acc

def load_result_Par(result_fn=os.path.join(data_name+'_view_result', paras['result_save_dir'], 'result.csv')):
    shared_code_acc = {}
    shared_code_acc_set = set()
    with open(result_fn) as f:
        for item in f.readlines():
            items = item.strip().split(',')
            if items[0] not in shared_code_acc_set:
                shared_code_acc[items[0]] = int(items[3])
                shared_code_acc_set.add(items[0])
    return shared_code_acc


def load_result_MVC(result_fn=os.path.join(data_name+'_view_result', paras['result_save_dir'], 'result_list_MVC')):
    result_fn = '/export/result_list_MVC.csv'
    shared_code_acc = {}
    shared_code_acc_set = set()
    with open(result_fn) as f:
        for item in f.readlines():
            items = item.strip().split(',')
            if items[0] not in shared_code_acc_set:
                print("没转变之前",items[0])
                items[0] = replace_minus_with_comma(items[0])
                print("转变之后",items[0])
                shared_code_acc[items[0]] = float(items[1])
                shared_code_acc_set.add(items[0])
    return shared_code_acc

def load_result_MVC_par(result_fn=os.path.join(data_name+'_view_result', paras['result_save_dir'], 'result_list_MVC')):
    result_fn = '/export/result_list_MVC.csv'
    shared_code_acc = {} # 这是一个字典
    shared_code_acc_set = set()  ## 保存每一种融合方式的 精度
    with open(result_fn) as f:
        for item in f.readlines():
            items = item.strip().split(',')
            if items[0] not in shared_code_acc_set:
                print("没转变之前",items[0])
                items[0] = replace_minus_with_comma(items[0])
                print("转变之后",items[0])
                shared_code_acc[items[0]] = float(items[2])  ## 返回每一种方式的精度
                shared_code_acc_set.add(items[0])## 这里应该要添加进去吧
    return shared_code_acc ##  得到了所有方式的精度  返回的是一个字典

def load_result_histories(result_fn=os.path.join(data_name+'_view_result', paras['result_save_dir'], 'history.csv')):
    shared_code_acc = [] # 这是一个字典
    result_fn = '/export/datasetENAS/ChemBookv2_view_result/history.csv'
    with open(result_fn) as f:
        for item in f.readlines():
            items = item.strip().split(',')
            if len(items) == 2 and int(items[0])  >= 1:
                shared_code_acc.append(items[1][:-2])  ##所有的都加进去
    return shared_code_acc  ##  拿到了所有种群的融合方式


def list2str(list1):
    return '-'.join([str(i) for i in list1])

def sign_sqrt(x):
    return tf.keras.backend.sign(x) * tf.keras.backend.sqrt(tf.keras.backend.abs(x) + 1e-10)

def l2_norm(x):
    return tf.keras.backend.l2_normalize(x, axis=-1)

import re


def replace_comma_with_minus(input_str):   ## 转化为-号
    return re.sub(r'\(([^,]+),\s([^)]+)\)', r'(\1-\2)', input_str)

def replace_minus_with_comma(input_str):   ## 转化回来
    return re.sub(r'\(([^-]+)-([^)]+)\)', r'(\1, \2)', input_str)


import random
import string

generated_strings = set()

def generate_unique_string():
    while True:
        unique_string = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
        if unique_string not in generated_strings:
            generated_strings.add(unique_string)
            return unique_string

