


def get_configs():
    paras = {
        'data_name': 'nus_wide',  # 128
        'idx_split': 0,
        'fusion_ways': ['add', 'mul', 'cat', 'max', 'avg'],
        'feature_statistics': ['a', 'a', 'a', 'a', 'a'],
        'fused_nb_feats':128,
        'nb_view':7,
        'pop_size': 28,
        'nb_iters': 15, # 15
        'nb_iters_MVC': 15,  # 15
        'result_save_dir': 'CSG-' + '-128-' + 'result',
        'gpu_list': [0,1,6,7],
        'epochs': 100,
        'epochs_min' : 100,
        'batch_size':64,
        'patience':10,
        'patience_min':10,
        'is_remove':  False,
        'crossover_rate': 0.9,
        'mutation_rate': 0.2,
        'knowledge_rate':0.5,
        'noisy': False,
        'max_len':40,
        'image_size': {
            'w': 224, 'h': 224, 'c': 3},
        'classes': 10,
        'split_data' :[2,4,6,8,10],
        'fusion_L' : 4,
        'fusion_C' : 512,
    }
    return paras