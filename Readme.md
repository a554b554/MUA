#常言道：python大法好,400行写MUA#

MUA 解释器 V1.0 开发者：肖昶 3120104234
使用方法：在shell终端当前目录下输入
python mua.py [filename]
即为执行[filename]内的mua脚本
例如：python mua.py aa.mua

包含库（均为python2.7内置库，无第三方库）：
string
copy
math
time
random

几点说明：
1.说明文件内判断是否相等为eq，但示例代码给出的为equ，我以说明文件为准，将aa.mua内的equ全部改为eq
2.mua.py是驱动程序，运行时只要执行这个脚本即可。
3.lex.py为词法分析器，目的是将输入的字符串做词法分析，提取token。
4.LRParser.py为语法分析器，也是核心模块，采用LR(0)分析法对输入的token进行解析，解释器的工作全部在这里完成。
5.save所产生的文件名字以.namespace为后缀，程序内设置文件名时不需要加后缀，load的时候也不需要加后缀，只需要保证在同一文件夹即可。
6.说明文件内提到的功能均已测试可以正常工作。
