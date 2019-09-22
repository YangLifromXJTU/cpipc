import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

f_out = pd.DataFrame([],columns=['index','Pi','Pa','Pd','Pc',
                                 'Vm','Vmr','amax','amin','am',
                                 'vsd','asd'])

nihe = pd.read_csv('nihe_3.csv',encoding='gbk')
ser = nihe['工况'].value_counts()

Pi = ser[0]/nihe.shape[0]
Pa = ser[1]/nihe.shape[0]
Pd = ser[2]/nihe.shape[0]
Pc = ser[3]/nihe.shape[0]
Vm = sum(nihe['车速'].values)/nihe.shape[0]
Vmr = sum(nihe['车速'].values)/(ser[1]+ser[2]+ser[3])
amax = max(nihe['加速度'].values)
amin = min(nihe['加速度'].values)
am = sum(nihe['加速度'].values)/nihe.shape[0]

vsd = sum([(v-Vm)**2 for v in list(nihe['车速'].values)])/(nihe.shape[0]-1)
vsd = vsd ** 0.5

asd = sum([a**2 for a in list(nihe['加速度'].values)])/(nihe.shape[0]-1)
asd = asd ** 0.5

f_out = f_out.append([{'Pi':Pi,'Pa':Pa,'Pd':Pd,'Pc':Pc,'Vm':Vm,'Vmr':Vmr,
                       'amax':amax,'amin':amin,'am':am,'vsd':vsd,'asd':asd}],
                       ignore_index=True)

# 然后要把对应的处理完的所有数据合并，然后计算
dirname = './problem2_3'
total = pd.DataFrame()
for maindir,subdir,file_name_list in os.walk(dirname):
    for filename in file_name_list:
        apath = os.path.join(maindir,filename)
        df = pd.read_csv(apath,encoding='gbk')
        total = total.append(df,ignore_index=True)

ser = total['工况'].value_counts()

Pi = ser[0]/total.shape[0]
Pa = ser[1]/total.shape[0]
Pd = ser[2]/total.shape[0]
Pc = ser[3]/total.shape[0]
Vm = sum(total['车速'].values)/total.shape[0]
Vmr = sum(total['车速'].values)/(ser[1]+ser[2]+ser[3])
amax = max(total['加速度'].values)
amin = min(total['加速度'].values)
am = sum(total['加速度'].values)/total.shape[0]

vsd = sum([(v-Vm)**2 for v in list(total['车速'].values)])/(total.shape[0]-1)
vsd = vsd ** 0.5

asd = sum([a**2 for a in list(total['加速度'].values)])/(total.shape[0]-1)
asd = asd ** 0.5

f_out = f_out.append([{'Pi':Pi,'Pa':Pa,'Pd':Pd,'Pc':Pc,'Vm':Vm,'Vmr':Vmr,
                       'amax':amax,'amin':amin,'am':am,'vsd':vsd,'asd':asd}],
                       ignore_index=True)
f_out.to_csv('compare_3.csv',index=0,encoding='gbk')