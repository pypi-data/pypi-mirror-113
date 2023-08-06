from comlibpy.iter import map

class XTree:

    def __init__(self, node, hasRoot, children=None):
        """树结构操作类

        **Arguments**
        * node:
        * hasRoot:
        * children:
        """
        self.node = node
        self.hasRoot = hasRoot

        if children == None:
            if hasattr(node, "children"):
                self.children = lambda x : x.children
            else:
                raise Exception("Invalid children is set!")
        else:   ## 更严格来说，应该要判断是否是可调用函数
            self.children = children

    @staticmethod
    def fromArray( arr, createNode, children, level ):
        """从一个元素列表构建树/多树
        **Arguments**
        * arr: List[T] ---- 元素列表
        * createNode: (e:T,child:List[Node]|None=None)=>Node ---- 构建树节点函数
          * e: 元素列表中每个元素
          * child: 子元素列表。fromArray构建的子节点列表
          * Return: 树节点
        * children: (n:Node)=>List[Node] ---- 如何从树节点获取其子节点的列表函数
          * n: 当前节点
          * Return: 返回的子节点列表
        * level: (e:T)=>Int ---- 如何获取元素在树中的层次函数
          * e: 元素
          * Return: 在树中的层次
        * Return: 构建的新的XTree树结构
        """

        #### 内部迭代函数
        def recur(arr, ofst, result):

            while ofst < len(arr)-1:  # 至少还有2个元素

                e = arr[ofst]   # 获取迭代元素
                lvl = level(e)  # 获取元素层级关系
                nxt_lvl = level(arr[ofst+1])
                
                if lvl == nxt_lvl:   # 当前元素是一个leaf节点，下一个节点和当前节点是兄弟
                    ele = createNode( e )   # 叶子节点，无子节点
                    result.append(ele)      # 父节点加入当前节点
                    ofst = ofst + 1

                elif lvl > nxt_lvl:  # 当前元素是一个leaf节点，下一个元素是当前元素的祖辈
                    ele = createNode( e )   # 叶子节点，无子节点
                    result.append(ele)      # 父节点加入当前节点
                    return ofst+1

                else: # 当前元素还有子元素
                    sub_result = []     # 子元素集合：由子元素迭代时隙填充
                    ofst = recur( arr, ofst+1, sub_result )    # 子元素迭代
                    ele = createNode( e, sub_result )   # 子填充完sub_result后，创建元素
                    result.append(ele)  # 填充父元素的result
                    ofst = ofst + 1

            # 最后一个元素处理：必定是一个叶子节点
            if ofst == len(arr)-1:
                ele = createNode( arr[ofst] )
                result.append(ele)

            return ofst

        result = []
        multiRoot = level(arr[0])>0
        recur( arr, 0, result )
        return XTree(result if multiRoot else result[0], ~multiRoot, children)


