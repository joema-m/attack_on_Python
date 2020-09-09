# -*- coding: utf-8 -*-
import argparse

# 创建一个解析器-- 一个ArgumentParser对象
parser = argparse.ArgumentParser(description='argparse test')

# 添加参数
parser.add_argument("-i", "--input", help="Your input file.")
parser.add_argument("-o", "--output", help="Your destination output file.")
parser.add_argument("-n", "--number", type=int, help="A number.")
parser.add_argument("-v", "--verbose", dest='verbose', action='store_true', help="Verbose mode.")
# 返回值是 Namespace
# 不用设置 -h --help，会自动生成
args = parser.parse_args()
print(args)
"""
>>> python parse.py -i 'in.txt' -o 'out.txt' -n 1200 -v
Namespace(input="'in.txt'", number=1200, output="'out.txt'", verbose=True)
"""


# 不能使用下面这样的循环来显示参数
# for i in args:
#     print(i)

# 可以使用下面的方法获取参数
# 但是不能使用短参数
print(args.input, args.output, args.number, args.verbose)
# 'in.txt' 'out.txt' 1200 True


