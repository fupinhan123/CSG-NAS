
#导入所需要的模块
import math
import random

#要优化的第一个函数
def function1(x):
    value = -x**2
    return value

#要优化的第二个函数
def function2(x):
    value = -(x-2)**2
    return value

#查找列表索引的函数
def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1

#按值排序的函数
def sort_by_values(list1, values):
    sorted_list = []   ## 创建一个空列表
    while(len(sorted_list)!=len(list1)):   # 循环一直执行直到 sorted_list == list1 结束  这时候索引都被排序
        if index_of(min(values),values) in list1:
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = math.inf
    return sorted_list     ## 从小到大排序

#快速非支配排序  返回的是 非支配解的帕累托前沿
def fast_non_dominated_sort(values1, values2):
    S=[[] for i in range(0,len(values1))]
    front = [[]]
    n=[0 for i in range(0,len(values1))]
    rank = [0 for i in range(0, len(values1))]

    for p in range(0,len(values1)):
        S[p]=[]
        n[p]=0
        for q in range(0, len(values1)):
            if (values1[p] > values1[q] and values2[p] < values2[q]) or (values1[p] >= values1[q] and values2[p] < values2[q]) or (values1[p] > values1[q] and values2[p] <= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] > values1[p] and values2[q] < values2[p]) or (values1[q] >= values1[p] and values2[q] < values2[p]) or (values1[q] > values1[p] and values2[q] <= values2[p]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if( n[q]==0):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)

    del front[len(front)-1]
    return front  ## 目前来看 每一个前沿 保存的都是下标值

#计算拥挤距离


def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1,len(front)-1):
        if  max(values1) == min(values1):
           distance[k] = distance[k]+ (values1[sorted1[k+1]] - values2[sorted1[k-1]])/(max(values1) + 0.01 -min(values1))
        else:
           distance[k] = distance[k] + (values1[sorted1[k + 1]] - values2[sorted1[k - 1]]) / (max(values1) - min(values1))
    for k in range(1,len(front)-1):
        if max(values2) == min (values2):  ## 防止 最大最小是一样的 分母为0的情况
           distance[k] = distance[k]+ (values1[sorted2[k+1]] - values2[sorted2[k-1]])/((max(values2)-min(values2)) + 1)
        else:
            distance[k] = distance[k] + (values1[sorted2[k + 1]] - values2[sorted2[k - 1]]) / (max(values2) - min(values2))
    return distance   ##      解和解中间的拥挤距离

#交叉
def crossover(a,b):
    r=random.random()
    if r>0.5:
        return mutation((a+b)/2)
    else:
        return mutation((a-b)/2)

#变异
def mutation(solution):
    mutation_prob = random.random()
    if mutation_prob <1:
        solution = min_x+(max_x-min_x)*random.random()
    return solution

#Main program starts here
pop_size = 20
max_gen = 921

#Initialization
min_x=-55
max_x=55
solution=[min_x+(max_x-min_x)*random.random() for i in range(0,pop_size)]  ## 开始生成初代种群 20
gen_no=0
while(gen_no<max_gen):  ##算法迭代次数
    function1_values = [function1(solution[i])for i in range(0,pop_size)]  ## 得到优化目标1
    function2_values = [function2(solution[i])for i in range(0,pop_size)]  ## 得到优化目标2
    non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:],function2_values[:]) ## 快速非支配排序
    print("The best front for Generation number ",gen_no, " is")
    for valuez in non_dominated_sorted_solution[0]:  ## 查看第一个前沿中 每个解是什么
        print(round(solution[valuez],3),end=" ")
    print("\n")
    crowding_distance_values=[]
    for i in range(0,len(non_dominated_sorted_solution)):
        crowding_distance_values.append(crowding_distance(function1_values[:],function2_values[:],non_dominated_sorted_solution[i][:]))
    solution2 = solution[:]
    #Generating offsprings
    while(len(solution2)!=2*pop_size):
        a1 = random.randint(0,pop_size-1)
        b1 = random.randint(0,pop_size-1)
        solution2.append(crossover(solution[a1],solution[b1]))
    function1_values2 = [function1(solution2[i])for i in range(0,2*pop_size)]
    function2_values2 = [function2(solution2[i])for i in range(0,2*pop_size)]

    non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:],function2_values2[:])

    crowding_distance_values2=[]
    for i in range(0,len(non_dominated_sorted_solution2)):
        crowding_distance_values2.append(crowding_distance(function1_values2[:],function2_values2[:],non_dominated_sorted_solution2[i][:]))
    new_solution= []

    for i in range(0,len(non_dominated_sorted_solution2)):  ## 循环 用于遍历通过非支配排序得到的前沿集合

        non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j],non_dominated_sorted_solution2[i] ) for j in range(0,len(non_dominated_sorted_solution2[i]))]
        """
        在这里,对于每个前沿，首先创建一个non_dominated_sorted_solution2_1列表 其中包含每个解在其所在前沿中的索引 
        """
        front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
        """
        这一行使用sort_by_values函数对non_dominated_sorted_solution2_1进行排序，其中排序的依据是每个解的拥挤度值（crowding_distance_values2[i]）。
        这将为前沿中的解创建一个排序后的索引列表，按照拥挤度进行排序。
        """
        front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0,len(non_dominated_sorted_solution2[i]))]
        """
        在这一行，前沿中的解按照拥挤度值的排序顺序被重新排列，并存储在front列表中。这样，前沿中的解按照拥挤度从高到低的顺序排列。
        """
        front.reverse() ## 将front列表中的解反转 以便首先选择拥挤度较低的解

        for value in front:
            new_solution.append(value)
            if(len(new_solution)==pop_size):
                break
        if (len(new_solution) == pop_size):
            break
    solution = [solution2[i] for i in new_solution]
    gen_no = gen_no + 1


function1 = [i * -1 for i in function1_values]
function2 = [j * -1 for j in function2_values]



