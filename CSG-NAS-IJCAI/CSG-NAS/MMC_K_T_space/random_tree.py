from  treelib import  Tree,Node
import  random
import utils
def randomTree(viewslist,fusionslist):   ###  给初始序列 生成生成融合树
    idx = utils.idxx
    strviews = [str(i)  for i  in viewslist]  ## 转化为字符串
    #print("我的视图", strviews)
    strfusion = ['-' + str(i) for i in fusionslist] ## 转化为字符串
    #print("我的融合算子", strfusion)
    viewsize = len(strviews)
    fusionsize = len(strfusion)
    # 看一下个数
    """
    生成一个合理的融合树序列
    """
    for i in range(0, len(strfusion)):
        tree_index1 = random.randrange(viewsize)  ## 取出来我要的下标
        v1 = strviews[tree_index1]
        del strviews[tree_index1]
        viewsize -= 1
        tree_index2 = random.randrange(viewsize)
        v2 = strviews[tree_index2]
        del strviews[tree_index2]
        viewsize -= 1

        ftree_index = random.randrange(fusionsize)
        f = strfusion[ftree_index]
        del strfusion[ftree_index]
        fusionsize -= 1
        strviews.append(' ' + v1 + ' ' + v2 + ' ' + f + ' ')
        viewsize += 1
    strtrees = strviews[0].split()
    #print("融合树", strtrees)
    """
    有了一个合理的融合树序列 我们去转为一颗树
    """
    stackstree = [] ## 存放所有子树的栈
    k = 0   ## 标记树根位置
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
    utils.idxx = idx
    return treepop

if __name__ == '__main__':
    tree1 = randomTree([1,2,1,4,2],[2,1,1,4])
    tree2 = randomTree([1,3,3,4],[1,0,3])