import pandas as pd
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('new1.csv',encoding='gbk')

# 删掉不用的数据
del data['之前时刻']

# 将两次时间差值转化成秒的形式
data['差值'] = data['差值'].apply(lambda x: int(x[7:9])*3600+int(x[10:12])*60+int(x[13:15]))
# 目前思路是把填充好的数据放到一个新的csv里面，先只保留车速和加速度（加速度后面求）
out = pd.DataFrame([],columns=['车速','加速度','发动机'])
ver = 1

# 然后判断两次的时间差值，这里用了每行遍历
for i in range(len(data['差值'])):
    item = data['差值'][i]
#   如果时间差为1，说明是正常取样，那就把这一行数据存到新的csv里面
    if item == 1:
        out = out.append([{'车速':data['GPS车速'][i],'加速度':0,'发动机':1}],ignore_index=True)
#   如果时间差大于1，判断速度差/时间差
    elif item > 1:
        print(i,item)
        delta_v = (data['GPS车速'][i]-data['GPS车速'][i-1])/(3.6*item)
#       如果加（减）速度没有超过阈值，也当过隧道处理，按照线性拟合补充速度数值
        print('  ',data['GPS车速'][i],data['GPS车速'][i-1],delta_v)
        # if -8 <= delta_v <= 3.97:
        if item < 180:
            # 对这个区间里面的所有时间，按秒计，填充数据
            j = 0
            speed = data['GPS车速'][i-1]/3.6
            while abs(data['GPS车速'][i]-speed*3.6) >= abs(delta_v*3.6) and j < item: #or speed*3.6-data['GPS车速'][i] <= delta_v*3.6:
                print('   ',abs(data['GPS车速'][i]-speed*3.6),abs(delta_v*3.6),item-j)
                out = out.append([{'车速':speed*3.6,'加速度':0,'发动机':1}],ignore_index=True)
                speed += delta_v
                j += 1
            if j > 1:
                # 最后再把这一行加上去
                out = out.append([{'车速':data['GPS车速'][i],'加速度':0,'发动机':1}],ignore_index=True)
     
#       如果加（减）速度超过阈值，说明应该是两次不同的过程
        else:
            print('  last v',data['GPS车速'][i-1])
#           前面一次的按照最大减速度将速度逐渐归0，
            speed = data['GPS车速'][i-1]/3.6
            while speed > 0:
                speed += -8
                out = out.append([{'车速':speed*3.6,'加速度':0,'发动机':1}],ignore_index=True)
            out = out.append([{'车速':0,'加速度':0,'发动机':1}],ignore_index=True)

            # 从间隔过长的地方进行分开
            out.to_csv('new1_'+str(ver)+'.csv',encoding='gbk')
            out = pd.DataFrame([],columns=['车速','加速度','发动机'])
            ver += 1
            
            # 是不还应该填一点空余的
#           后面那次的按照最大加速度将速度逐渐提升到出现的数据
            speed = data['GPS车速'][i]/3.6
            mod = speed % 3.96
            if mod > 0:
                out = out.append([{'车速':speed*3.6,'加速度':0,'发动机':1}],ignore_index=True)
            speed = mod
            while speed*3.6 < data['GPS车速'][i]:
                speed += 3.96
                out = out.append([{'车速':speed*3.6,'加速度':0,'发动机':1}],ignore_index=True)
            # 最后把这一行数据填入新表
            out = out.append([{'车速':data['GPS车速'][i],'加速度':0,'发动机':1}],ignore_index=True)

out.to_csv('new1_'+str(ver)+'.csv',encoding='gbk')