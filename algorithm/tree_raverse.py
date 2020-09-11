# 二叉树的4种遍历
# 递归与迭代

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


node1 = TreeNode(1)
node2 = TreeNode(2)
node3 = TreeNode(3)
node4 = TreeNode(4)
node5 = TreeNode(5)
node6 = TreeNode(6)
node7 = TreeNode(7)
node8 = TreeNode(8)
node0 = TreeNode(0)

node0.left = node1
node0.right = node2
node1.left = node3
node1.right = node4
node4.right = node5
node2.right = node6
node6.left = node7
node6.right = node8

'''
前： 0 1 3 4 5 2 6 7 8
中： 3 1 4 5 0 2 7 6 8
后： 3 5 4 1 7 8 6 2 0
层： 0 1 2 3 4 6 5 7 8
'''


# 1. 前序遍历
# 递归
def pre_order_1(root: TreeNode, li):
    if root:
        li.append(root.val)
        li.append(pre_order_1(root.left, li))
        li.append(pre_order_1(root.right, li))


# 迭代，使用 stack
def pre_order_2(root: TreeNode):
    if root is None:
        return []
    stack = []
    result = []
    stack.append(root)
    while len(stack) > 0:
        node = stack.pop()
        result.append(node.val)
        # 先让右节点进栈
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


# 2.中序遍历
# 递归
def in_order_1(root: TreeNode, li):
    if root:
        in_order_1(root.left, li)
        li.append(root.val)
        in_order_1(root.right, li)
    else:
        li.append(None)


# 迭代
def in_order_2(root: TreeNode):
    if root is None:
        return []
    stack = []
    result = []
    node = root
    while node or (len(stack) > 0):
        if node:
            stack.append(node)
            node = node.left
        else:
            node = stack.pop()
            result.append(node.val)
            node = node.right
    return result


# 3.后序遍历
# 递归
def post_order_1(root: TreeNode, li):
    if root:
        post_order_1(root.left, li)
        post_order_1(root.right, li)
        li.append(root.val)
    elif root is None:
        li.append(None)


# 迭代，使用两个stack
def post_order_2(root: TreeNode):
    if root is None:
        return []
    stack1 = []
    stack2 = []
    result = []
    stack1.append(root)
    while len(stack1) > 0:
        node = stack1.pop()
        stack2.append(node)
        if node.left:
            stack1.append(node.left)
        if node.right:
            stack1.append(node.right)
    while len(stack2) > 0:
        top = stack2.pop()
        result.append(top.val)
    return result


# 层序遍历
def level_order(root: TreeNode):
    if not root:
        return []
    result = []
    queue = [root]
    while queue and root:
        result.append(queue[0].val)
        # 左边先进队
        if queue[0].left:
            queue.append(queue[0].left)
        if queue[0].right:
            queue.append(queue[0].right)
        queue.pop(0)
    return result


# resList = []
# pre_order_1(node0, resList)
# res = []
# for i in resList:
#     if i is not None:
#         res.append(i)
# print(res)

print(pre_order_2(node0))
print(in_order_2(node0))
print(post_order_2(node0))
print(level_order(node0))