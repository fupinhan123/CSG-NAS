
import os
from warnings import simplefilter

import  gen_offspring_tree_all_pop_MVC_NS_2
indivial_set_weight = {}
simplefilter(action='ignore', category=FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tqdm import tqdm  ## 进度条s
import tensorflow as tf   ## 导入主要库
tf.get_logger().setLevel('ERROR')
import numpy as np
from os.path import join as pjoin
import random
from multiprocessing import Pool,Manager
import time
from  sklearn import  metrics
from best_fives import  best_fivess
import config
import  tree_to_strlist
import utils
from code2net_tree import code2net_tree_KT
import  split
import population_init_KT

paras = config.get_configs()
fusion_ways = paras['fusion_ways']
fused_nb_feats = paras['fused_nb_feats']
classes = paras['classes']
batch_size = paras['batch_size']
epochs = paras['epochs']
epochs_min = paras['epochs_min']
pop_size = paras['pop_size']
nb_iters = paras['nb_iters']
data_name = paras['data_name']
patience_min = paras['patience_min']
split_data = paras['split_data']
patience = paras['patience']

data_base_dir = os.path.join('', data_name)
manager = Manager()
shared_gpu_list = manager.list([0,2,3,4,5,6,7])
data_lists = split.load_data_features()
dict_data ={'a':0,'b':1,'c':2,'d':3,'e':4}


def metric(test_y, y_pred):
    num_test = test_y.shape[0]
    topk1 = tf.keras.metrics.top_k_categorical_accuracy(test_y, y_pred, k=1)
    topk5 = tf.keras.metrics.top_k_categorical_accuracy(test_y, y_pred, k=5)
    topk10 = tf.keras.metrics.top_k_categorical_accuracy(test_y, y_pred, k=10)

    # with tf.Session() as sess:
    topk1 = topk1.numpy()
    topk5 = topk5.numpy()
    topk10 = topk10.numpy()

    topk1 = topk1[topk1 == 1].shape[0] / num_test
    topk5 = topk5[topk5 == 1].shape[0] / num_test
    topk10 = topk10[topk10 == 1].shape[0] / num_test
    print(topk1, topk5, topk10)

    return topk1


def find_same_code_acc(individual_code, result_save_dir='.'):
    individual_code_str = '-'.join([str(ind) for ind in individual_code])
    return individual_code_str

def record_code(individual_code, result_save_dir='.'):
    individual_code_str = '-'.join([str(ind) for ind in individual_code])
    return individual_code_str


def list2str(list1):
    return '-'.join([str(i) for i in list1])

def list2str_tree(list1):  ## 转换
    return '+'.join([str(i) for i in list1])

def multi_proccess_train(i_iter, Q_t, Q_t_wight, shared_code_sets):  ## 开始训练


    gpu_list = paras['gpu_list']  ## 看看GPU
    gpus = len(gpu_list)  ## GPU个数多少
    gpu_idx = 0  ## 开始的时候是1
    pool = Pool(gpus)
    individual_code_str = []
    pop_size1 = len(Q_t)  ## 种群大小
    print(len(Q_t))
    for ind_i in np.arange(0, pop_size1): ## 一个一个取出来
        id = 0
        pop_num = 3
        print(len(Q_t), '==========', ind_i+1)
        code_str = list2str_tree(Q_t[ind_i]) ## 转换序列
        utils.write_result_file(','.join([str(i_iter+1), code_str]),fn=os.path.join(result_save_dir, 'history.csv'))
        ## 把生成的结果写进去
        code_str = code_str[:-2]
        if code_str not in shared_code_sets[id] or code_str in best_fivess:
            if code_str not in shared_code_sets[id]:
                is_exist = False
                shared_code_sets[id].add(code_str)

                individual_code_str.append(pool.apply_async(func=train_individual,args=(Q_t[ind_i],Q_t_wight[ind_i], result_save_dir, str(gpu_list[gpu_idx]),i_iter,is_exist,pop_num,ind_i))) #GPU +1
            gpu_idx += 1
        if gpu_idx == gpus or ind_i == (pop_size1-1):
            pool.close()
            pool.join()
            for ss in individual_code_str:
                resulits, weight = ss.get()
                split_result = resulits.split(',')
                first_part = split_result[0][:-2]
                indivial_set_weight[first_part] = weight
                utils.write_result_file(resulits, fn=os.path.join(result_save_dir, 'result.csv'))
            pool = Pool(gpus)
            gpu_idx = 0
            individual_code_str = []
def train():
    set1 = set()
    set4 = set()


    shared_code_sets = [set1,set4]

    # 1. population initialization
    print(f'The number of views: {len(data_lists[0][0][0])}')

    ini_population = population_init_KT.generate_population_tree(views=len(data_lists[0][0][0]), pop_size=pop_size, verbose=0)

    random.shuffle(ini_population)
    # 2.init population fitness
    start = time.time()
    P_t = ini_population
    multi_proccess_train(i_iter=-1, Q_t=P_t, Q_t_wight =  [0] * len(P_t),shared_code_sets=shared_code_sets)  ## pop_num 代表的子种群的编号
    # 3. gen_offspring
    for i in tqdm(range(paras['nb_iters'])):  ## 更迭多少次
        print(f'==================={i+1}/', paras['nb_iters'])
        Q_t,Q_wight = gen_offspring_tree_all_pop_MVC_NS_2.gen_offspring(P_t,indivial_set_weight,i)
        Q_t,Q_wight = sort_population(Q_t,Q_wight)
        multi_proccess_train(i_iter=i, Q_t=Q_t,Q_t_wight=Q_wight, shared_code_sets=shared_code_sets)
        P_t = gen_offspring_tree_all_pop_MVC_NS_2.selection(P_t, Q_t)
        print('=' * 60, i+1, 'End.')
        print(f'Total time is :{time.time()-start}')
        utils.write_result_file(str(time.time()-start), fn=os.path.join(result_save_dir, 'history.csv'))

def train_one_code(is_train=False, code='8-9-1-4-7-2-5-1-0-0-0-4-4'):
    codes = code.split('+')
    os.environ["CUDA_VISIBLE_DEVICES"] = '2'
    print("我是什么",result_save_dir)
    if  is_train == True:
        train_individual(codes, [], result_save_dir,'5',is_exist= True,pop_id = 3)

def train_individual(individual_code,individual_wight, result_save_dir='.', gpu='0', iter_pop = 0,is_exist = False,pop_id = 0,individual = 0):  ## 现在生成的就是一个融合序列



    K_T = int(individual_code[-1])
    individual_code = individual_code[:-1]


    os.environ["CUDA_VISIBLE_DEVICES"] = gpu

    if pop_id <= 2:
        epochss = epochs_min
        pat = patience_min
    else:
        epochss = epochs
        pat = patience

    data_list = split.get_split_data(data_lists, pop_id)
    view_train_xx, view_test_xx = [], []

    sta_data_list = []
    views = []
    for value in individual_code:
        if(value[1] >= 'a' and  value[1] <= 'z'):
            sta_data_list.append(dict_data[value[1]])
            views.append(int(value[0]))
    for index,num in enumerate(sta_data_list):
        if num >= 5:
            num = 2
        data = data_list[num]
        view_train_xx.append(data[0][views[index]])
        view_test_xx.append(data[2][views[index]])
    view_train_x1, train_y, view_test_x1, test_y = data_list[0]


    individual_code_tree, nb_view = tree_to_strlist.viewfusion(individual_code)

    individual_code_str = '+'.join([str(ind) for ind in individual_code])
    individual_code_str+= ( '+' + str(K_T))


    nb_feats = [i.shape[1] for i in view_train_xx]

    checkpoint_filepath = os.path.join(result_save_dir, individual_code_str  + '.h5')

    EMV_len = len(individual_code)

    if is_exist == False:

      model = code2net_tree_KT(individual_code=individual_code_tree,nb_feats=nb_feats,listtree = individual_code)

      if K_T == 1:
          for key,value in individual_wight.items():
              if len(value) != 1:
                  layer = model.get_layer(name = key)
                  layer.set_weights(value)
    else :
      print(checkpoint_filepath)
      model = tf.keras.models.load_model(checkpoint_filepath)

    if  K_T == 0:
       adam = tf.keras.optimizers.Adam()

    elif  K_T == 1:
       pat = 5
       epochss = 20
       adam = tf.keras.optimizers.SGD(learning_rate= 0.005)

    topk = tf.keras.metrics.top_k_categorical_accuracy
    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['acc', topk])
    checkpoint = tf.keras.callbacks.ModelCheckpoint(checkpoint_filepath, monitor='val_acc', verbose=0, save_best_only=True, save_weights_only=False) ## 回调以保存Keras模型或模型权重
    early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_acc', patience=pat)
    csv_filepath = os.path.join(result_save_dir, individual_code_str   + '.csv')
    csv_logger = tf.keras.callbacks.CSVLogger(csv_filepath)
    pop_list_id = tree_to_strlist.viewfusion_id(individual_code)
    model.fit(view_train_xx, train_y, batch_size=batch_size, epochs=epochss,
              verbose=0, validation_data=(view_test_xx, test_y),
              callbacks=[csv_logger, early_stop, checkpoint])

    model_best = tf.keras.models.load_model(checkpoint_filepath)
    weight_list = {}

    for i , num in enumerate(pop_list_id):
        model_layer = model_best.get_layer(name = num)
        model_layer_bn = model_best.get_layer(name = num + str('bn'))
        dense_layer_weights = model_layer.get_weights()
        bn_layer_weights    = model_layer_bn.get_weights()
        weight_list[num] = dense_layer_weights
        weight_list[num + str('bn')] = bn_layer_weights
    model_layer = model_best.get_layer(name='father_layer')
    weight_list['father_layer'] = model_layer.get_weights()  ### 拿到最后一层
    model_layer = model_best.get_layer(name='father_layer_bn')
    weight_list['father_layer_bn'] = model_layer.get_weights()

    pre_y = model_best.predict(view_test_xx)
    pre_y = np.argmax(pre_y, axis=1)
    true_y = np.argmax(test_y, axis=1)
    acc = metrics.accuracy_score(true_y, pre_y)
    total_params = model_best.count_params()
    print("我的参数大小",total_params)

    return (individual_code_str + ',' + str(acc) + ','  + str(total_params) + ',' + str(EMV_len),weight_list)





def sort_population(ini_population, weights):
    def condition(individual):
        return individual[-1] == '1'

    individuals_1 = [x for x in ini_population if condition(x)]
    weights_1 = [weights[ini_population.index(x)] for x in individuals_1]
    individuals_0 = [x for x in ini_population if not condition(x)]
    weights_0 = [weights[ini_population.index(x)] for x in individuals_0]

    ini_population = individuals_1 + individuals_0
    weights = weights_1 + weights_0

    return ini_population, weights




def test_individual(individual_code, result_save_dir='.', gpu='0', iter_pop=0, is_exist=False,pop_id=0):  ## 现在生成的就是一个融合序列
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu
    data_list = split.get_split_data(data_lists, pop_id)
    view_train_xx, view_test_xx = [], []

    sta_data_list = []
    views = []


    K_T = individual_code[-1]

    individual_code = individual_code[:-1]

    for value in individual_code:
        if (value[1] >= 'a' and value[1] <= 'z'):
            sta_data_list.append(dict_data[value[1]])
            views.append(int(value[0]))

    for index, num in enumerate(sta_data_list):
        if num >= 5:
            num = 2
        data = data_list[num]
        view_train_xx.append(data[0][views[index]])
        view_test_xx.append(data[2][views[index]])
    view_train_x1, train_y, view_test_x1, test_y = data_list[0]

    individual_code_tree, nb_view = tree_to_strlist.viewfusion(individual_code)  ## 融合视图顺序 先进去了

    individual_code_str = '+'.join([str(ind) for ind in individual_code])  ##这是保存下来了
    individual_code_str +=   ( '+' + str(K_T))
    result_save_dir = '/export/datasetENAS/MMC_K_T_space/data_set_rgb_ske_view_result/CSG-NAS-64-GPU-result'
    nb_feats = [i.shape[1] for i in view_train_xx]
    checkpoint_filepath = os.path.join(result_save_dir, individual_code_str + '.h5')

    if is_exist == False:
        model = code2net_tree_KT(individual_code=individual_code_tree, nb_feats=nb_feats, listtree=individual_code)
    else:
        model = tf.keras.models.load_model(checkpoint_filepath)

    pre_yy = model.predict(view_test_xx)
    pre_y = np.argmax(pre_yy, axis=1)
    true_y = np.argmax(test_y, axis=1)
    acc = metrics.accuracy_score(true_y, pre_y)
    return pre_yy, test_y


if __name__ == '__main__':
    result_save_dir = pjoin(data_name+'_view_result', paras['result_save_dir'])
    print(result_save_dir)
    print(data_name, fused_nb_feats)
    is_trian = False
    os.makedirs(result_save_dir, exist_ok=True)
    is_train_one_code = False
    if is_train_one_code == True:
        train_one_code(is_train = True,code='6a+0a+-4+7a+3a+4a+5a+1a+-1+-1+-4+-0+-0+1')

    else :
        train()
    print(result_save_dir)
    print(data_name, fused_nb_feats)
