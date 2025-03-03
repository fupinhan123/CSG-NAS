

best_fivess = set()


### 四个种群 
A1_best_fivess = {}
A2_best_fivess = {}
A3_best_fivess = {}
A4_best_fivess = {}

Archive1 = []     ## 这个是全部训练数据存储的 最优个体

Archive2 = []     ## 这个是抽样训练数据存储的 最优个体

## 存储历史最佳的知识库也就是父代的

Archive1_weights = {}     ## 这个是全部训练数据存储的 最优个体权重
Archive2_weights = {}     ## 这个是抽样训练数据存储的 最优个体权重


GPU_lists = [0,2,3,4,5,6,7]  ## 自己维护一个


All_best_fivess = {}
Archive_All_best = []