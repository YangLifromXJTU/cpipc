import pandas as pd
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

data = pd.read_excel('new1.csv')

# 删掉不用的数据
del data['之前时刻']
# 将两次时间差值转化成秒的形式
data['差值'] = data['差值'].apply(lambda x: int(x[7:9])*3600+int(x[10:12])*60+int(x[13:15]))
# 目前思路是把填充好的数据放到一个新的csv里面，先只保留车速和加速度（加速度后面求）
out = pd.DataFrame([],columns=['时间','车速','加速度','发动机转速'])

# 然后判断两次的时间差值，这里用了每行遍历
for i in range(len(data['差值'])):
    item = data['差值'][i]
#   如果时间差为1，说明是正常取样
    if item == 1:
        out.
        continue
#   如果时间差大于1，判断速度差/时间差
    if item > 1:
        delta_v = (data['GPS车速'][i]-data['GPS车速'][i-1])/(3.6*item)
#       如果加（减）速度没有超过阈值，也当过隧道处理，按照线性拟合补充速度数值
        if 0 < delta_v < 3.9686 or -8 < delta_v < -7.5:
            
#       如果加（减）速度超过阈值，说明应该是两次不同的过程
#           前面一次的按照最大减速度将速度逐渐归0，
#           后面那次的按照最大加速度将速度逐渐提升到出现的数据
      