from  treelib import  Tree,Node
import  utils

def tree_to_list(tree):
    listhead =list(reversed(tree.all_nodes()))
    lists = [ i.tag for i in listhead]
    return lists

def tree_to_list2(tree):
    iter_tree = tree.expand_tree()
    listhead = []
    for i in iter_tree:
        listhead.append(tree.get_node(i))
    lists = [i.tag for i in listhead]
    lists = list(reversed(lists))
    return lists
def list_to_tree(strtrees):
    idx = utils.idxx
    stackstree = []  ## 存放所有子树的栈
    idxroot = 0  ## 树根是谁
    k = 0  ## 标记树根位置
    for treenode in strtrees:
        k += 1
        node = treenode
        tree = Tree()
        if (node[0] != '-'):
            ##  里面保存的是 idx  也就是唯一的便是
            tree.create_node(tag=treenode, identifier=idx)
            stackstree.append(tree)
        else:
            if (k != len(strtrees)):
                tree.create_node(tag=treenode, identifier=idx)  ## 创造一个子树
            else:
                tree.create_node(tag=treenode, identifier=idx)
            tree.paste(idx, stackstree[-1])
            stackstree.pop()
            tree.paste(idx, stackstree[-1])
            stackstree.pop()
            stackstree.append(tree)
        idx = idx + 1

    treepop = stackstree[0]


    treepoporder = list(reversed(treepop.all_nodes()))
    utils.idxx = idx
    return treepop

def tree_list2str(list1):
    return '-'.join([str(i) for i in list1])

def viewfusion(liststr):
    views = []
    fusions = []
    viewnum = 0
    for i in liststr:
        if(i[0] != '-' and i[1] >='a' and i[1] <='z'):
            views.append(int(i[0]))
            viewnum +=1
        else:
            fusions.append(int(i[1]))
    view_fusion_code = views + fusions
    return view_fusion_code,viewnum

def viewfusion_id(liststr):
    views_id = []
    fusions = []
    viewnum = 0
    for i in liststr:
        if(i[0] != '-' and i[1] >='a' and i[1] <='z'):
            views_id.append(i)
            viewnum +=1
        else:
            fusions.append(int(i[1]))
    view_fusion_code = views_id   ### 只要id
    return view_fusion_code

def viewlist(liststr): ##  直接拿出所有视图
    views = []
    fusions = []
    viewnum = 0
    for i in liststr:
        if(i[0] != '-'):
            views.append(int(i))
            viewnum +=1
        else:
            fusions.append(int(i[1]))
    return views

def viewsize(liststr): ##  直接拿出所有视图
    viewnum = 0
    for i in liststr:
        if(i[0] == '-'):
            viewnum += 1
    return viewnum + 1