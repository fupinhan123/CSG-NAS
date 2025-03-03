
import tensorflow as tf
import numpy as np
import os
import config
import nus_wide
import chembook
opt = os.path
paras = config.get_configs()
nb_view = paras['nb_view']
image_size = paras['image_size']
w, h, c = image_size['w'], image_size['h'], image_size['c']
data_name = paras['data_name']
idx_split = paras['idx_split']

def get_data(data_base_dir='..'):
    print('Data loading ......')
    train_x = np.load(os.path.join(data_base_dir, 'train_X.npy'))
    test_x = np.load(os.path.join(data_base_dir, 'test_X.npy'))
    if c == 1:
        train_x = np.expand_dims(train_x, axis=-1)
        test_x = np.expand_dims(test_x, axis=-1)
    train_x = (train_x / 127.5) - 1.
    test_x = (test_x / 127.5) - 1.
    train_y = np.load(os.path.join(data_base_dir, 'train_Y.npy'))
    test_y = np.load(os.path.join(data_base_dir, 'test_Y.npy'))
    train_y = tf.keras.utils.to_categorical(train_y)
    test_y = tf.keras.utils.to_categorical(test_y)
    print('Data loading finished！！！')
    return train_x, train_y, test_x, test_y


def get_views(view_data_dir='views'):
    if data_name == 'nus_wide':
        view_train_x, train_y, view_test_x, test_y = nus_wide.load_nus_wide(
            view_data_dir=view_data_dir, idx_split=idx_split)
    elif data_name == 'ChemBookv22':
        view_train_x, train_y, view_test_x, test_y = chembook.load_chembookv2(
            view_data_dir=view_data_dir, idx_split=idx_split)
    else:
        models_ls  = ['rgb2','rgb3','rgb4','rgb5','ske2','ske3','ske4','ske5']  # NTU 'tags1k'
        if nb_view == 11:
            models_ls = models_ls+['resnet18', 'resnet34', 'desnet169', 'desnet201', 'NASNetMobile'] ## 可能是10个
        view_train_x = []
        view_test_x = []
        for model in models_ls:
            view_train_x.append(np.load(os.path.join(view_data_dir, model+'train.npy')))
            view_test_x.append(np.load(os.path.join(view_data_dir, model+'test.npy')))
        train_y = np.load(os.path.join(view_data_dir, 'train_YY.npy'))
        test_y = np.load(os.path.join(view_data_dir, 'test_YY.npy'))
    train_y = tf.keras.utils.to_categorical(train_y)
    test_y = tf.keras.utils.to_categorical(test_y)

    return view_train_x, train_y, view_test_x, test_y

def add_gaussian_noise(features, mean=0, std=0.1):
    noise = np.random.normal(mean, std, features.shape)
    noisy_features = features + noise
    return noisy_features

if __name__ == '__main__':
    base_dir = opt.join('data_utils/fn')
