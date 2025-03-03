import numpy as np
import random
import config
import utils
import  random_tree
import  tree_to_strlist
import utils_tree
feature_statistics = config.get_configs()['feature_statistics']

def generate_population(views=10, pop_size=10, verbose=0):
    fusion_ways = config.get_configs()['fusion_ways']
    population = []
    population_set = set()


    while len(population) < pop_size:
        view_code = random.sample(range(0, views), k=random.randint(2, views))
        fusion_code = random.choices(range(0, len(fusion_ways)), k=len(view_code)-1)
        pop = view_code+fusion_code
        if verbose == 1:
            print(f'view_code:{view_code}')
            print(f'fusion_code:{fusion_code}')
            print(f'pop:{pop}')
            print('='*30)
        if utils.list2str(pop) not in population_set:
            population.append(pop)
            population_set.add(utils.list2str(pop))
    return population

def generate_population_list(views=8, pop_size=10, verbose=0):
    print("种群大小",views)
    print("里面含有的元素",pop_size)
    fusion_ways = config.get_configs()['fusion_ways']

    population = []
    population_set_list = set()

    while len(population) < pop_size:
        list_MVC = []
        view_code = random.sample(range(0, views), k=pop_size)
        view_code_w =  [random.random() for _ in range(pop_size)]      ## 对应方法的权值
        for i in range(len(view_code)):
            num1 = view_code[i]
            num2 = view_code_w[i]
            list_MVC.append((num1, num2))

        threshold = random.uniform(0.2, 0.7)

        list_MVC.append(threshold)
        cnt = 0
        for pop in list_MVC[:-1]:
            if pop[1] < list_MVC[-1]:
                cnt += 1
        if cnt == pop_size:
            random_index = random.randint(0, pop_size - 1)
            list_MVC[random_index] = (list_MVC[random_index][0], random.uniform(threshold, 1.0))

        fusion_code = random.choices(range(0, len(fusion_ways)), k=len(view_code) - 1)
        sta_code = random.choices(range(0, len(feature_statistics)), k=len(view_code))
        str_list = [feature_statistics[num]for num in sta_code]
        view_code = [str(num) for num in view_code]

        pop =  list_MVC

        if verbose == 1:
            print(f'view_code:{view_code}')
            print(f'fusion_code:{fusion_code}')
            print(f'pop:{pop}')
            print('=' * 30)
        if tree_to_strlist.tree_list2str(pop) not in population_set_list:
            population.append(pop)
            population_set_list.add(utils.list2str(pop)) ## 如果已经存在就不放进去 防止重复
    return population




if __name__ == '__main__':
    population = generate_population_list()