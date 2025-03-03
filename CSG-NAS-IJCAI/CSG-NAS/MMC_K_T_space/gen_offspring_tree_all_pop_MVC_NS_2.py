import random
import copy
import utils_tree
from config import get_configs
import NSGA2_NS
import NSGA_TO
import  math
paras = get_configs()
nb_fusion_way = len(paras['fusion_ways'])
nb_view = 5
is_remove = paras['is_remove']
knowledge_rate = paras['knowledge_rate']
import  utils

def tree_edit_distance(tree1, tree2):
    m = len(tree1)
    n = len(tree2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif tree1[i - 1] == tree2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                insert_cost = dp[i][j - 1] + 1
                delete_cost = dp[i - 1][j] + 1
                replace_cost = dp[i - 1][j - 1] + 1
                dp[i][j] = min(insert_cost, delete_cost, replace_cost)

    return dp[m][n]



def get_all_nodes_identifier(tree):
    nodes = tree.all_nodes()
    identifiersfph = []
    for node in nodes:
        if(tree.parent(node.identifier) != None):
            identifiersfph.append(node.identifier)
        else:
            nodes.remove(node)
    return nodes, identifiersfph

def get_leaf_nodes_identifier(tree):
    nodes = tree.leaves()
    identifiers = [node.identifier for node in nodes]
    return nodes, identifiers

def split_tree(tree, nid):  ## 分割
    tree_copy = copy.deepcopy(tree)
    removed_tree = tree_copy.remove_subtree(nid=nid, identifier=nid)
    return tree_copy, removed_tree

def get_branch_nodes_identifier(tree):
    all_nodes = tree.all_nodes()
    branch_nodes = []
    identifiersfph = []
    for node in all_nodes[:]:
        if len(tree.is_branch(node.identifier)) != 0  and tree.parent(node.identifier) is not None:
            branch_nodes.append(node)
            identifiersfph.append(node.identifier)
        else:
            all_nodes.remove(node)
    return branch_nodes,identifiersfph


def crossover_KT(tree1, tree2, crossover_rate, is_remove=is_remove, max_deep=15):

    if len(tree1) == 0 or len(tree2) == 0 or len(tree1) == 1 or len(tree2) == 1:
        return tree1, tree2
    r = random.random()
    if (r < crossover_rate):

        tree1_nodes, tree1_identifiers = get_branch_nodes_identifier(tree1)
        if len(tree1_nodes) == 0:
           tree1_nodes, tree1_identifiers = get_all_nodes_identifier(tree1)


        tree2_nodes, tree2_identifiers = get_branch_nodes_identifier(tree2)
        if len(tree2_nodes) == 0:
           tree2_nodes, tree2_identifiers = get_all_nodes_identifier(tree2)

        if len(tree1) == 1:
            print("出现问题")
        tree1_split_point = random.choice(tree1_nodes)
        tree2_split_point = random.choice(tree2_nodes)

        tree1_split_node = tree1_split_point
        tree2_split_node = tree2_split_point
        node = tree1.parent(tree1_split_node.identifier)
        if (node == None):
            tree1_split_node_parent = tree1_split_node.identifier
        else:
            tree1_split_node_parent = node.identifier
        node = tree2.parent(tree2_split_node.identifier)
        if (node == None):
            tree2_split_node_parent = tree2_split_node.identifier
        else:
            tree2_split_node_parent = node.identifier
        tree1_left, tree1_right = split_tree(tree1, tree1_split_point.identifier)
        tree2_left, tree2_right = split_tree(tree2, tree2_split_point.identifier)
        tree1_left.paste(tree1_split_node_parent, tree2_right)
        tree2_left.paste(tree2_split_node_parent, tree1_right)
        if is_remove == True:
            tree1_left = quchong(tree1_left)
            tree2_left = quchong(tree2_left)
        if tree1_left.depth() > max_deep:
            tree1_left = quchong(tree1_left)
        if tree2_left.depth() > max_deep:
            tree2_left = quchong(tree2_left)

        return tree1_left, tree2_left  ## 返回交叉变异的树
    else:
        if is_remove:
            tree1 = quchong(tree1)
            tree2 = quchong(tree2)
        if tree1.depth() > max_deep:
            tree1 = quchong(tree1)
            tree2 = quchong(tree2)
        return tree1, tree2

def crossover_add(tree1, tree2, crossover_rate, is_remove = is_remove,max_deep = 15):  ## 交叉

    if len(tree1) == 0 or len(tree2) == 0 or len(tree1) == 1 or len(tree2) == 1:  ### 这里特判一下就好了
        return tree1, tree2
    r = random.random()
    if (r < crossover_rate):
        tree1_nodes, tree1_identifiers = get_leaf_nodes_identifier(tree1)  ## 第一颗是主树 所以我们只用获取叶子节点
        tree2_nodes, tree2_identifiers = get_branch_nodes_identifier(tree2)  ## 得到所有的分支节点

        if len(tree2_nodes) == 0:
            tree2_nodes, tree2_identifiers = get_all_nodes_identifier(tree2)

        if len(tree1) == 1:
            print("出现问题")

        tree1_split_point = random.choice(tree1_nodes)  ## 随机选择一颗子树
        tree2_split_point = random.choice(tree2_nodes)  ## 随机选择子树

        tree1_split_node = tree1_split_point
        tree2_split_node = tree2_split_point
        node = tree1.parent(tree1_split_node.identifier)
        if (node == None):
            tree1_split_node_parent = tree1_split_node.identifier
        else:
            tree1_split_node_parent = node.identifier

        if (node == None):
            tree2_split_node_parent = tree2_split_node.identifier
        else:
            tree2_split_node_parent = node.identifier

        tree2_left, tree2_right = split_tree(tree2, tree2_split_point.identifier)

        #print(tree2_left)
        tree1.paste(tree1_split_node_parent, tree2_left)

        if is_remove == True:
            tree1 = quchong(tree1)

        if tree1.depth() > max_deep:
            tree1 = quchong(tree1)
        return tree1,tree1
    else :
        if is_remove:
            tree1 = quchong(tree1)
            tree2 = quchong(tree2)
        if tree1.depth() > max_deep:
            tree1 = quchong(tree1)
            tree2 = quchong(tree2)
        return tree1, tree2


def crossover(tree1, tree2, crossover_rate, is_remove = is_remove,max_deep = 15):  ## 交叉

    if len(tree1) ==0 or  len(tree2) == 0 or len(tree1) == 1 or len(tree2) == 1:  ### 这里特判一下就好了
        return tree1,tree2


    r = random.random()
    if(r < crossover_rate):
        tree1_nodes, tree1_identifiers = get_all_nodes_identifier(tree1)  ## 得到所有节点的值
        tree2_nodes, tree2_identifiers = get_all_nodes_identifier(tree2)  ## 得到所有节点的值

        if len(tree1) == 1:
            print("出现问题")
        tree1_split_point = random.choice(tree1_nodes)             ## 随机选择一颗子树
        tree2_split_point = random.choice(tree2_nodes)            ## 随机选择子树


        tree1_split_node = tree1_split_point
        tree2_split_node = tree2_split_point
        node = tree1.parent(tree1_split_node.identifier)
        if(node == None):
            tree1_split_node_parent = tree1_split_node.identifier
        else :
            tree1_split_node_parent= node.identifier
        node = tree2.parent(tree2_split_node.identifier)
        if (node == None):
            tree2_split_node_parent = tree2_split_node.identifier
        else:
            tree2_split_node_parent = node.identifier

        tree1_left, tree1_right = split_tree(tree1, tree1_split_point.identifier)
        tree2_left, tree2_right = split_tree(tree2, tree2_split_point.identifier)
        tree1_left.paste(tree1_split_node_parent, tree2_right)
        tree2_left.paste(tree2_split_node_parent, tree1_right)
        if is_remove == True:
            tree1_left = quchong(tree1_left)
            tree2_left = quchong(tree2_left)
        if tree1_left.depth() > max_deep:
            tree1_left = quchong(tree1_left)
        if tree2_left.depth() > max_deep:
            tree2_left = quchong(tree2_left)

        return tree1_left,tree2_left
    else :
        if is_remove:
            tree1 = quchong(tree1)
            tree2 = quchong(tree2)
        if tree1.depth() > max_deep:
            tree1 = quchong(tree1)
            tree2 = quchong(tree2)
        return tree1,tree2

def mutation(tree, mutation_rate, is_remove=is_remove, max_deep = 15):
    nodes = tree.all_nodes()
    node = random.choice(nodes)
    idtag = node.tag
    r = random.random()
    if (r < mutation_rate):
        if(idtag[0] == '-'):
            mutation_view = list(range(nb_fusion_way))
            id = random.choice(mutation_view)
            idtag = '-'+ str(id)
        else:
            mutation_view = list(range(nb_view))
            id = random.choice(mutation_view)
            idtag = str(id)
        node.tag = idtag
        if is_remove:
            tree = quchong(tree)
    else:
        if is_remove:
            tree = quchong(tree)

    if(tree.depth() > max_deep):
        tree = quchong(tree)
    return tree
def mutation_new_tree_crossover(tree, mutation_rate, is_remove=is_remove, max_deep = 15,flat = 0):
    r = random.random()
    if (r < mutation_rate):
        if flat == 0:
            tree_mut = utils_tree.new_tree_1([2,4,6],[0,2,3]) ## 抽出来一颗新树 用于变异
            tree1, tree2 = crossover(tree, tree_mut, 1, is_remove, 15)  ##交叉一下  只要取第一颗就好了
        else:
            tree_mut = utils_tree.new_tree_2([0,1,3,5],[1,4])  ## 抽出来一颗新树 用于变异
            tree1, tree2 = crossover_add(tree, tree_mut, 1, is_remove, 15)  ##交叉一下  只要取第一颗就好了
        if is_remove:
            tree1 = quchong(tree1)
        if tree1.depth() > max_deep:
            tree1 = quchong(tree1)
        flat = True
        return tree1,flat
    else :
        if is_remove:
            tree = quchong(tree)
        if tree.depth() > max_deep:
            tree = quchong(tree)
        flat = False
        return tree,flat

def quchong(tree_p):
    list_tree = utils_tree.tree_to_list2(tree_p)
    quchong_tree = []
    num_views = 0
    for i in list_tree:
        if i[0] != '-':
            if i not in quchong_tree:
               quchong_tree.append(i)
               num_views +=1
        else:
            if num_views >=2:
                quchong_tree.append(i)
                num_views-=1
    quchongtree = utils_tree.list_to_tree(quchong_tree)
    return quchongtree


def add_number_to_suffix(input_list, number):
    modified_list = [item + str(number) if item.endswith('a') else item for item in input_list]
    return modified_list

def remove_number_from_suffix(input_list, number):
    modified_list = [item[:-1] if item.endswith('a' + str(number)) else item for item in input_list]
    return modified_list

def gen_offspring(P_t,indivial_set_weight,i_iter):
    shared_code_acc = utils.load_result_new()
    def select_p():
        two = random.sample(range(len(P_t)), 2)
        a1 = '+'.join([str(i) for i in P_t[two[0]]])
        a2 = '+'.join([str(i) for i in P_t[two[1]]])
        p1 = P_t[two[0]] if shared_code_acc[a1[:-2]] > shared_code_acc[a2[:-2]] else P_t[two[1]] ## 两个里面选一个精度好的返回
        return p1

    Q_t = []
    Q_tt_wight = []

    while len(Q_t) < len(P_t):
        p1 = select_p()
        p2 = select_p()
        while '+'.join(str(i) for i in p1) == '+'.join(str(i) for i in p2):
            p2 = select_p()

        p1_weight = indivial_set_weight['+'.join(str(i) for i in p1[:-1])]
        p2_weight = indivial_set_weight['+'.join(str(i) for i in p2[:-1])]


        father =  add_number_to_suffix(p1[:-1],1)
        mother =  add_number_to_suffix(p2[:-1],2)

        p1_tree = utils_tree.list_to_tree(father)
        p2_tree = utils_tree.list_to_tree(mother)
        if i_iter >= 6:
            o1_tree, o2_tree = crossover(tree1=p1_tree, tree2=p2_tree, crossover_rate=paras['crossover_rate'] / 9 )
        else:
            o1_tree, o2_tree = crossover(tree1=p1_tree, tree2=p2_tree, crossover_rate=paras['crossover_rate'])

        o1 = utils_tree.tree_to_list2(o1_tree)
        o2 = utils_tree.tree_to_list2(o2_tree)

        o1_wight = {}
        o2_wight = {}

        cnt1 = 0
        cnt2 = 0
        o_1 = []
        o_2 = []
        for num in o1:
            if num[0] != '-':
                if num[2] == '1':
                    o1_wight[num[:-1]] = p1_weight[num[:-1]]
                    o1_wight[num[:-1] + 'bn'] = p1_weight[num[:-1] + 'bn']
                    cnt1 += 1
                else:
                    o1_wight[num[:-1]] = p2_weight[num[:-1]]
                    o1_wight[num[:-1] + 'bn'] = p2_weight[num[:-1] + 'bn']
                    cnt2+=1

                o_1.append(num[:-1])
            else:
                o_1.append(num)
        if cnt2 >= cnt1:
            o1_wight['father_layer_bn'] = p2_weight['father_layer_bn']
            o1_wight['father_layer'] = p2_weight['father_layer']
        else:
            o1_wight['father_layer_bn'] = p1_weight['father_layer_bn']
            o1_wight['father_layer']    = p1_weight['father_layer']

        p_tree = utils_tree.list_to_tree(o_1)
        if i_iter >= 6:
            p1_tree, flat = mutation_new_tree_crossover(p_tree, mutation_rate=paras['mutation_rate'] * 4 , flat=1)
        else:
            p1_tree, flat = mutation_new_tree_crossover(p_tree, mutation_rate=paras['mutation_rate']  , flat=0)

        p_1 = utils_tree.tree_to_list2(p1_tree)
        if flat  == False:
            Q_tt_wight.append(o1_wight)
        else:
            p_wight = {}
            for num in p_1:
                if num[0] != '-':
                    if num in o1_wight:
                        p_wight[num] = o1_wight[num]
                        p_wight[num + 'bn'] = o1_wight[num+'bn']
                    else :
                        p_wight[num] = [0]
                        p_wight[num + 'bn'] = [0]
            Q_tt_wight.append(p_wight)
        o_1 = p_1


        cnt1 = 0
        cnt2 = 0

        if cnt2 >= cnt1:
            o2_wight['father_layer_bn'] = p2_weight['father_layer_bn']
            o2_wight['father_layer'] = p2_weight['father_layer']
        else:
            o2_wight['father_layer_bn'] = p1_weight['father_layer_bn']
            o2_wight['father_layer'] = p1_weight['father_layer']


        for num in o2:
            if num[0] != '-':
                if num[2] == '2':
                    o2_wight[num[:-1]] = p2_weight[num[:-1]]
                    o2_wight[num[:-1]+'bn'] = p2_weight[num[:-1]+'bn']
                else:
                    o2_wight[num[:-1]] = p1_weight[num[:-1]]
                    o2_wight[num[:-1] + 'bn'] = p1_weight[num[:-1] + 'bn']
                o_2.append(num[:-1])
            else:
                o_2.append(num)

        p_tree = utils_tree.list_to_tree(o_2)
        if i_iter >= 6:
            p2_tree, flat = mutation_new_tree_crossover(p_tree, mutation_rate=paras['mutation_rate'] * 4 ,flat = 1)
        else:
            p2_tree, flat = mutation_new_tree_crossover(p_tree, mutation_rate=paras['mutation_rate'],flat = 0)

        p_2 = utils_tree.tree_to_list2(p2_tree)
        if flat == False:
            Q_tt_wight.append(o2_wight)
        else:
            p_wight = {}
            for num in p_2:
                if num[0] != '-':
                    if num in o2_wight:
                        p_wight[num] = o2_wight[num]
                        p_wight[num + 'bn'] = o2_wight[num + 'bn']
                    else:
                        p_wight[num] = [0]
                        p_wight[num + 'bn'] = [0]
            Q_tt_wight.append(p_wight)

        o_2 = p_2

        o1_dis1 = tree_edit_distance(o_1,p1[:-1])
        o1_dis2 = tree_edit_distance(o_1,p2[:-1])

        o2_dis1 = tree_edit_distance(o_2, p1[:-1])
        o2_dis2 = tree_edit_distance(o_2, p2[:-1])


        fatherlen = len(p1[:-1])
        mother    = len(p2[:-1])

        o1_len = max((fatherlen - o1_dis1) / fatherlen, (mother - o1_dis2) / mother)

        o2_len = max((fatherlen - o2_dis1) / fatherlen, (mother - o2_dis2) / mother)


        if o1_len >=0.5:
            o_1.append('1')
        else:
            o_1.append('0')

        if o2_len>=0.5:
            o_2.append('1')
        else:
            o_2.append('0')


        Q_t.append(o_1)
        Q_t.append(o_2)

    return Q_t,Q_tt_wight

def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1


def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1:
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = math.inf
    return sorted_list

def selection_EVO(P_t, Q_t):
    pop_size = len(P_t) ## 种群大小
    shared_code_acc = utils.load_result_Acc()
    shared_code_par = utils.load_result_Par()
    Pt_Qt = P_t+Q_t

    function1_values2 = [shared_code_acc['+'.join([str(i) for i in Pt_Qt[i]])] for i in range(2 * len(P_t))]
    function2_values2 = [shared_code_par['+'.join([str(i) for i in Pt_Qt[i]])] for i in range(2 * len(P_t))]

    non_dominated_sorted_solution2 = NSGA_TO.fast_non_dominated_sort(function1_values2[:],function2_values2[:])

    crowding_distance_values2 = []
    for i in range(0, len(non_dominated_sorted_solution2)):
        crowding_distance_values2.append(
            NSGA_TO.crowding_distance(function1_values2[:], function2_values2[:], non_dominated_sorted_solution2[i][:]))
    new_solution = []
    for i in range(0,len(non_dominated_sorted_solution2)):
        non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j],non_dominated_sorted_solution2[i] ) for j in range(0,len(non_dominated_sorted_solution2[i]))]
        front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
        front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0,len(non_dominated_sorted_solution2[i]))]
        front.reverse()
        for value in front:
            new_solution.append(value)
            if (len(new_solution) == pop_size):
                break
        if (len(new_solution) == pop_size):
            break
    solution = [Pt_Qt[i] for i in new_solution]
    P_t1 = solution

    return P_t1


def selection(P_t, Q_t):
    shared_code_acc = utils.load_result_new()
    def select_p1(select_pool):
        two = random.sample(range(len(select_pool)), 2)
        a1 = '+'.join([str(i) for i in select_pool[two[0]]])
        a2 = '+'.join([str(i) for i in select_pool[two[1]]])
        b1 = a1[:-2]
        b2 = a2[:-2]

        p1 = select_pool[two[0]] if shared_code_acc[b1] > shared_code_acc[b2] else select_pool[two[1]]
        return p1
    P_t1 = []
    Pt_Qt = P_t+Q_t
    random.shuffle(Pt_Qt)
    while len(P_t1) < len(P_t):
        p = select_p1(Pt_Qt)
        P_t1.append(p)


    max_code = []
    max_code_str = ''
    min_code_str =''

    for k, v in shared_code_acc.items():
        if v == max(shared_code_acc.values()):
            max_code_str = k
            max_code = k.strip().split('+')

        if v == min(shared_code_acc.values()):
            min_code_str = k
    is_max = False
    for i, v in enumerate(P_t1):
        v_str = utils_tree.tree_list2str(v)
        if v_str[:-2] == max_code_str:
            is_max = True
            break
    if not is_max:
        min_i = 0
        for i, v in enumerate(P_t1):
            v_str = utils_tree.tree_list2str(v)
            if v_str[:-2] == min_code_str:
                min_i = i
                break
        max_code.append('0')
        P_t1[min_i] = max_code
    return P_t1