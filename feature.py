# 这个为每个运动学片段计算对应参数
import pandas as pd
import warnings
import os

warnings.filterwarnings('ignore')

dirname = '.\\problem2_1'
f_out = pd.DataFrame([],columns=['index','Pi','Pa','Pd','Pc',
                                 'Vm','Vmr','amax','amin','am',
                                 'vsd','asd','ni','na','nd','nc','num'])
i = 1
for maindir,subdir,file_name_list in os.walk(dirname):
    for  filename in file_name_list:
        apath = os.path.join(maindir,filename)
        print(apath)
        data = pd.read_csv(apath,encoding='gbk')
        
        ser = data['工况'].value_counts()
        if 0 in ser and 1 in ser and 2 in ser and 3 in ser:
            Pi = ser[0]/data.shape[0]
            Pa = ser[1]/data.shape[0]
            Pd = ser[2]/data.shape[0]
            Pc = ser[3]/data.shape[0]
            Vm = sum(data['车速'].values)/data.shape[0]
            Vmr = sum(data['车速'].values)/(ser[1]+ser[2]+ser[3])
            amax = max(data['加速度'].values)
            amin = min(data['加速度'].values)
            am = sum(data['加速度'].values)/data.shape[0]
            
            vsd = sum([(v-Vm)**2 for v in list(data['车速'].values)])/(data.shape[0]-1)
            vsd = vsd ** 0.5

            asd = sum([a**2 for a in list(data['加速度'].values)])/(data.shape[0]-1)
            asd = asd ** 0.5

            num = filename.split('.')[0].split('_')[1]

            f_out = f_out.append([{'index':i,'Pi':Pi,'Pa':Pa,'Pd':Pd,'Pc':Pc,'Vm':Vm,'Vmr':Vmr,
                                   'amax':amax,'amin':amin,'am':am,'vsd':vsd,'asd':asd,'ni':ser[0],
                                   'na':ser[1],'nd':ser[2],'nc':ser[3],'num':num}],
                                ignore_index=True)
            i += 1

f_out.to_csv('problem2_1_feature.csv',index=0)