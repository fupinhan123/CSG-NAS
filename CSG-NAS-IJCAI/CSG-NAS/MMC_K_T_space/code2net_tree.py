
import tensorflow as tf
import config
import utils_tree
import   tree_to_strlist
paras = config.get_configs()
fusion_ways = paras['fusion_ways']
fused_nb_feats = paras['fused_nb_feats']
classes = paras['classes']

idx = 0  ## 树的ID地址
def sign_sqrt(x):
    return tf.keras.backend.sign(x) * tf.keras.backend.sqrt(tf.keras.backend.abs(x) + 1e-10)

def l2_norm(x):
    return tf.keras.backend.l2_normalize(x, axis=-1)


def scaled_dot_product_attention(q, k, v):
    # 计算点积注意力分数
    attention_scores = tf.matmul(q, k, transpose_b=True)
    d_k = tf.cast(tf.shape(k)[-1], tf.float32)
    attention_scores = attention_scores / tf.sqrt(d_k)

    attention_weights = tf.nn.softmax(attention_scores, axis=-1)

    output = tf.matmul(attention_weights, v)

    return output


def fusion(x1, x2, way='add'):
    if way == fusion_ways[0]:
        fusion_x = tf.keras.layers.Add()([x1, x2])
    if way == fusion_ways[1]:
        fusion_x = tf.keras.layers.Multiply()([x1, x2])
    if way == fusion_ways[2]:
        fusion_x = tf.keras.layers.Concatenate()([x1, x2])
        fusion_x = tf.keras.layers.Dense(units=fused_nb_feats)(fusion_x)
    if way == fusion_ways[3]:
        fusion_x = tf.keras.layers.Maximum()([x1, x2])
    if way == fusion_ways[4]:
        fusion_x = tf.keras.layers.Average()([x1, x2])
    return fusion_x



def code2net_tree_KT(individual_code, nb_feats=[1024, 2048, 1028],listtree = ''):
    reuse = set()

    individual_code,nb_view= utils_tree.viewfusion(listtree)
    pop_list_id = tree_to_strlist.viewfusion_id(listtree)
    input_x = []
    x = []
    x_bn = []
    x_dp = []
    for i in range(nb_view):
        input_x.append(tf.keras.layers.Input((nb_feats[i],)))
        if pop_list_id[i] + 'bn' not in reuse:
            reuse.add(pop_list_id[i] + 'bn' )
            x_bn.append(tf.keras.layers.BatchNormalization(name=pop_list_id[i]+str('bn'))(input_x[i]))
        else:
            x_bn.append(tf.keras.layers.BatchNormalization()(input_x[i]))


        if pop_list_id[i] not in reuse:
           x.append(tf.keras.layers.Dense(units=fused_nb_feats, activation='relu', name = pop_list_id[i] )(x_bn[i]))
           reuse.add(pop_list_id[i])
        else:
           x.append(tf.keras.layers.Dense(units=fused_nb_feats, activation='relu')(x_bn[i]))

    fusion_x = None
    cnt = 0
    if nb_view == 1:
        fusion_x = x[0]
    else:
        individual_code1, vsize = listtree, nb_view
        listview = []  ## 这个就是栈了
        for index, i in enumerate(individual_code1):
            if (i[0] != '-'):
                listview.append(cnt)
                cnt += 1
            else:
                e1 = listview[-1]  ## 拿的是一个下标
                listview.pop()
                e2 = listview[-1]  ## 拿的是一个下标
                listview.pop()
                f1 = int(i[1])
                fusion_x = fusion(x1=x[e1], x2=x[e2], way=fusion_ways[f1])
                x.append(fusion_x)

                listview.append(vsize)  ## 以前是vsise
                vsize += 1
    fusion_x = tf.keras.layers.BatchNormalization(name= 'father_layer_bn')(fusion_x)
    fusion_x = tf.keras.layers.Lambda(sign_sqrt)(fusion_x)
    fusion_x = tf.keras.layers.Lambda(l2_norm)(fusion_x)
    out_x = tf.keras.layers.Dense(units=classes, activation='softmax',name= 'father_layer')(fusion_x)
    model = tf.keras.models.Model(inputs=input_x, outputs=[out_x])
    return model

def code2net_tree(individual_code, nb_feats=[1024, 2048, 1028],listtree = ''): ## 这里要多加一个变量
    individual_code,nb_view= utils_tree.viewfusion(listtree)  ## 融合视图顺序 先进去了
    input_x = []
    x = []
    x_bn = []
    x_dp = []

    for i in range(nb_view):
        input_x.append(tf.keras.layers.Input((nb_feats[i],)))
        x_bn.append(tf.keras.layers.BatchNormalization()(input_x[i]))
        x.append(tf.keras.layers.Dense(units=fused_nb_feats, activation='relu')(x_bn[i]))


    fusion_x = None
    cnt = 0
    if nb_view == 1:
        fusion_x = x[0]
    else:
        individual_code1, vsize  = listtree,nb_view

        listview = []
        for index,i in enumerate(individual_code1):
            if (i[0] != '-'):
                listview.append(cnt)
                cnt += 1
            else:
                e1 = listview[-1]
                listview.pop()
                e2 = listview[-1]
                listview.pop()
                f1 = int(i[1])
                fusion_x = fusion(x1=x[e1], x2=x[e2], way=fusion_ways[f1])
                x.append(fusion_x)
                listview.append(vsize)
                vsize += 1
    fusion_x = tf.keras.layers.BatchNormalization()(fusion_x)
    fusion_x = tf.keras.layers.Lambda(sign_sqrt)(fusion_x)
    fusion_x = tf.keras.layers.Lambda(l2_norm)(fusion_x)

    out_x = tf.keras.layers.Dense(units=classes, activation='softmax')(fusion_x)
    model = tf.keras.models.Model(inputs=input_x, outputs=[out_x])
    return model


