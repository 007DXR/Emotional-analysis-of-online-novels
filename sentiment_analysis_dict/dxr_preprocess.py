
import xlrd
reader=xlrd.open_workbook("情感词性.xlsx")
reader=reader.sheet_by_index(0)
print(reader.nrows)
positive_writer=open('positive_writer.txt','w+')
negative_writer=open('negative_writer.txt','w+')
count=0
for i in  range(1,reader.nrows):

    word=reader.row_values(i,0,1)[0]
    word_type=reader.row_values(i,6,7)[0]
    # print(word,word_type)
    try:
        if word_type==1:
            positive_writer.write(word+'\n')
        if word_type==2:
            negative_writer.write(word+'\n')
        count+=1

    except:
        print("error"+word)
        continue
print("complete",count)
# import xlwt
# writer=xlwt.Workbook("")
# sheet=writer.add_sheet("s")
# sheet.write(2,2,"")