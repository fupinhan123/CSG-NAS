
import random
import config
import utils
import  random_tree
import  tree_to_strlist
import utils_tree

feature_statistics = config.get_configs()['feature_statistics']
r = config.get_configs()['knowledge_rate']

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

def generate_population_tree(views=8, pop_size=10, verbose=0):  ##老师原来的程序


    '''
        种群初始化
        :param views: 视图个数
        :param pop_size: 种群大小
        :return:
    '''
    fusion_ways = config.get_configs()['fusion_ways']
    population = []
    population_set_tree = set()
    numbers = [2,4,6]   ## 核心结构搜索
    top_three_operators = [0,2,4]   ## 核心结构搜索
    while len(population) < pop_size:
        view_code = random.sample(numbers, k=random.randint(2, len(numbers)))
        fusion_code = random.choices(top_three_operators, k=len(view_code) - 1)
        sta_code = random.choices(range(0, len(feature_statistics)), k=len(view_code))
        str_list = [feature_statistics[num]for num in sta_code]
        view_code = [str(num) for num in view_code]

        view_codes = []
        for i in range(len(view_code)):
            view_codes.append(view_code[i] + str_list[i])

        pop_tree = random_tree.randomTree(view_codes,fusion_code)
        pop = utils_tree.tree_to_list2(pop_tree)

        pop_list = pop

        pop_list.append('0')
        if verbose == 1:
            print(f'view_code:{view_code}')
            print(f'fusion_code:{fusion_code}')
            print(f'pop:{pop_list}')
            print('=' * 30)

        if tree_to_strlist.tree_list2str(pop_list[:-1]) not in population_set_tree:
            population.append(pop_list)
            population_set_tree.add(utils.list2str(pop_list[:-1]))
    return population

if __name__ == '__main__':
    population = generate_population_tree()
    # for i in population:
    #     print(i)