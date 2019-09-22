import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

ans = 0
dirname = './new3_process'
for maindir,subdir,file_name_list in os.walk(dirname):
    for filename in file_name_list:
        apath = os.path.join(maindir,filename)
        data = pd.read_csv(apath,encoding='gbk')
        ans += data.shape[0]
print(ans)