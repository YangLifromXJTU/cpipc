# 程序用于按照怠速工况切割运动学片段，切割方法是两次怠速工况的开头之间为一个片段
import pandas as pd
import datetime
import time
import warnings

warnings.filterwarnings('ignore')

# 先写个data占位置
f = [i for i in range(1,80)]
ver = 1 # 用于标识是第几个文件
for n in f:
# for n in [3]:
    print(n)
    # data = pd.DataFrame()
    data = pd.read_csv('./new3_process/new3_'+str(n)+'.csv',encoding='gbk')
    print(len(data['工况']))
    del data['发动机']
    # 怠速 -> 0, 加速 -> 1, 减速 -> 2, 匀速 -> 3
    # 加速正常 -> 0, 异常 -> 1
    cut = pd.DataFrame([],columns=['时间','车速','加速度','工况','异常'])
    flag = True # 用于标识怠速工况是否是下一片段的开始
    
    i = 0
    d_count = 0 # 怠速持续时间
    # for i in range(len(data['工况'])):
    while i < len(data['工况']):
        if data['异常'][i] == 1:
            del cut
            # print('i now:',i,data['工况'][i],i<len(data['工况']))
            while i < len(data['工况']) and (data['工况'][i] != 0 or data['异常'][i] == 1):
                i += 1
                # print('i:',i)
            # print(' new slice at:',i)
            cut = pd.DataFrame([],columns=['时间','车速','加速度','工况','异常'])
            flag = True
        else:
            if data['工况'][i] == 0:
                # 如果是怠速
                d_count += 1
                if d_count < 180: # 如果连续怠速低于180就放新表，如果高于180就不放，变相等于切了
                    if i == 0 or data['工况'][i-1] == 0 or flag == True or cut.shape[0] == 0:
                        # print('i == 0')
                        # 如果是一个运动学片段的开头，就加进去
                        cut = cut.append([{'时间':data['时间'][i],
                                           '车速':data['车速'][i],
                                           '加速度':data['加速度'][i],
                                           '工况':data['工况'][i],
                                           '异常':data['异常'][i]}],ignore_index=True)
                        flag = False
                    else:
                        if 1 not in cut['异常'].values:
                            print('save it at:',i)
                            cut.to_csv('./new3_slice/new3_'+str(ver)+'.csv',encoding='gbk')
                            ver += 1
                        # else:
                            # print('not proper at:',i)
                        cut = pd.DataFrame([],columns=['时间','车速','加速度','工况','异常'])
                        flag = True
            else:
                if cut.shape[0] > 0: # 说明切片中有数据，即前面有怠速工况
                    # print('other gongkuang:',i)
                    cut = cut.append([{'时间':data['时间'][i],'车速':data['车速'][i],
                                '加速度':data['加速度'][i],'工况':data['工况'][i],
                                '异常':data['异常'][i]}],ignore_index=True)
                d_count = 0 # 怠速计数归0
            i += 1