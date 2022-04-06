from colorlog import exception
import numpy as np
import os
import xlwt
from scipy.signal import savgol_filter
from statsmodels.nonparametric.kernel_regression import KernelReg
writer=xlwt.Workbook()

# writer=open('average_sentiment.xlsx','w',encoding='utf-8')
# writer.write('年份,书名,平均情感值(*100)\n')
folders=os.listdir('../output')
cnt_length=[0]*1000
for folder in folders:
    files=os.listdir('../output/'+folder)
    sheet=writer.add_sheet(folder[:-4])
    row_cnt=0
    sheet.write(row_cnt,0,'年份')
    sheet.write(row_cnt,1,'书名')
    sheet.write(row_cnt,2,'句数')
    sheet.write(row_cnt,3,'平均情感值(*100)')
    sheet.write(row_cnt,4,'波峰均值(*100)')
    sheet.write(row_cnt,5,'波谷均值(*100)')
    year_data=[]
    total_data=0
    total_top_list=[]
    total_bot_list=[]
    total_arc=0
    cnt_data=0
    print(folder)
    for file in files:
        file_path='../output/'+folder+'/'+file
        
        data=np.load(file_path)['arr_0']
        row_cnt+=1
        sheet.write(row_cnt,0,folder[:-4])
        sheet.write(row_cnt,1,file[:-4])
        sheet.write(row_cnt,2,len(data))
        sheet.write(row_cnt,3,np.average(data)*100)
        year_data.append(np.average(data))
        total_data+=np.sum(data)
        cnt_data+=len(data)
        window_length = 201 #len(data)//15*2+1
        data=savgol_filter(data,  window_length, 2)
        data=savgol_filter(data,  window_length, 2)
        # data_x= np.linspace(1,len(data),len(data))
        # kr = KernelReg(data,data_x,'c')
        # data, _ = kr.fit(data_x)
        cnt_arc=0
        top_list=[]
        bot_list=[]
        for i in range(1,len(data)-1):
            if data[i]>data[i-1] and data[i]>data[i+1]:
                top_list.append(data[i])
                total_top_list.append(data[i])
                cnt_arc+=1
            if data[i]<data[i-1] and data[i]<data[i+1]:
                bot_list.append(data[i])
                total_bot_list.append(data[i])
                cnt_arc+=1
        if cnt_arc==0:
            cnt_arc=1
            print(file_path,"has 0 arc")
        total_arc+=cnt_arc

        sheet.write(row_cnt,4,np.average(top_list)*100)
        sheet.write(row_cnt,5,np.average(bot_list)*100)
        # cnt_length[len(data)//100]+=1
            # writer.write('%s,%s,%.4f\n'%(folder[:-4],file[:-4],np.average(data)*100))
        # except Exception :
        #     print("error2 ",Exception)
    row_cnt+=1
    sheet.write(row_cnt,3,total_data/cnt_data*100)
    sheet.write(row_cnt,4,np.average(total_top_list)*100)
    sheet.write(row_cnt,5,np.average(total_bot_list)*100)
    # sheet.write(row_cnt,1,np.average(year_data)*100)

writer.save("count_arc4.xls")
# for i in range(0,1000):
#     if cnt_length[i]:
#         print("%d~%d:%d"%(i*100,(i+1)*100,cnt_length[i]))