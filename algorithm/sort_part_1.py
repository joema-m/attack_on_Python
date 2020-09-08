# -*- coding: utf-8 -*-
import random
import time


# 生成随机数组
def random_int_list(start, stop, length):
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list


# 选择排序
def selectionSort(nums):
    for i in range(len(nums) - 1):  # 遍历 len(nums)-1 次
        minIndex = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[minIndex]:  # 更新最小值索引
                minIndex = j
        nums[i], nums[minIndex] = nums[minIndex], nums[i]
    return nums


# 冒泡排序
def bubbleSort(nums):
    for i in range(len(nums) - 1):  # 遍历 len(nums)-1 次
        for j in range(len(nums) - i - 1):  # 已排好序的部分不用再次遍历
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]  # Python 交换两个数不用中间变量
    return nums


# 插入排序
def insertionSort(nums):
    for i in range(len(nums) - 1):  # 遍历 len(nums)-1 次
        curNum, preIndex = nums[i + 1], i  # curNum 保存当前待插入的数
        while preIndex >= 0 and curNum < nums[preIndex]:  # 将比 curNum 大的元素向后移动
            nums[preIndex + 1] = nums[preIndex]
            preIndex -= 1
        nums[preIndex + 1] = curNum  # 待插入的数的正确位置
    return nums


# 希尔排序
def shellSort(nums):
    lens = len(nums)
    gap = 1
    while gap < lens // 3:
        gap = gap * 3 + 1  # 动态定义间隔序列
    while gap > 0:
        for i in range(gap, lens):
            curNum, preIndex = nums[i], i - gap  # curNum 保存当前待插入的数
            while preIndex >= 0 and curNum < nums[preIndex]:
                nums[preIndex + gap] = nums[preIndex]  # 将比 curNum 大的元素向后移动
                preIndex -= gap
            nums[preIndex + gap] = curNum  # 待插入的数的正确位置
        gap //= 3  # 下一个动态间隔
    return nums


def costTime(fun, nums):
    start_time = time.time()
    sorted_num = fun(nums)
    stop_time = time.time()
    print(fun.__name__, ' costs: ', stop_time - start_time)


if __name__ == "__main__":
    random.seed(10)
    nums = random_int_list(1, 1000000, 50000)
    print(nums[:50])
    costTime(selectionSort, nums)  # 56.86020565032959s
    costTime(bubbleSort, nums)  # 105.82070279121399
    costTime(insertionSort, nums)  # 0.010009288787841797
    costTime(shellSort, nums)  # 0.08007407188415527
