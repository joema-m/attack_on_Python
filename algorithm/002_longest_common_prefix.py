# -*- coding: utf-8 -*-

# 暴力解法
# 内存和时间都基本打不过其他人
def longestCommonPrefixOne(strs) -> str:
    if len(strs) == 0:
        return ''
    for i in range(len(strs[0])):
        c = strs[0][i]
        for j in range(1, len(strs)):
            # 如果找到最短字符串 或 找到第一个不同的字符
            if i == len(strs[j]) or strs[j][i] != c:
                return strs[0][0:i]
    return strs[0]


# 这个性能不错
# 首先按ASCII排序获取最小和最大的字符串
# 例如：abc abb abd add aqq -> abs aqq
# 只用比较这两个就行
# 排序时间复杂度
# 用时超过93% 内存超过82%
def longestCommonPrefixTwo(strs):
    if not strs:
        return ""
    s1 = min(strs)
    s2 = max(strs)
    for i, x in enumerate(s1):
        if x != s2[i]:
            return s2[:i]
    return s1

