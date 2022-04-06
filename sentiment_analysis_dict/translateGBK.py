
import os 
from pip._vendor import chardet
from util.langconv import Converter
def Valuable(sentence):
    
    if sentence=='':
        return False
    ignore_list=['感谢投出','感谢灌溉','非常感谢','感谢在','作者有话']
    for ignore_word in ignore_list:    
                if ignore_word in sentence:
                    return False
    return True   

def readtype(path):
    types=['utf-16','utf-8','gbk','GB18030','GB2312','ISO8859-1','ISO8859-3','ISO8859-15']
    for etype in types:
        try:
            reader=open(path,'r',encoding=etype)
            code=reader.read()
            output=''
            for sentence in code.split('\n'):
                sentence=sentence.strip()
                sentence = Converter('zh-hans').convert(sentence)
                if Valuable(sentence):
                    output+=sentence+'\n'
            return output
        except:
            continue
    print("error:",path)
allFileNum = 0  
def printPath(level, path):  
    global allFileNum  
    ''''' 
    打印一个目录下的所有文件夹和文件 
    '''  
    # 所有文件夹，第一个字段是次目录的级别  
    dirList = []  
    # 所有文件  
    fileList = []  
    # 返回一个列表，其中包含在目录条目的名称(google翻译)  
    files = os.listdir(path)  
    # 先添加目录级别  
    dirList.append(str(level))  
    for f in files:  
        if(os.path.isdir(path + '/' + f)):  
            # 排除隐藏文件夹。因为隐藏文件夹过多  
            if(f[0] == '.'):  
                pass  
            else:  
                # 添加非隐藏文件夹  
                dirList.append(f)  
        if(os.path.isfile(path + '/' + f)):  
            # 添加文件  
            fileList.append(f)  
    # 当一个标志使用，文件夹列表第一个级别不打印  
    i_dl = 0  
    for dl in dirList:  
        if(i_dl == 0):  
            i_dl = i_dl + 1  
        else:  
            # 打印至控制台，不是第一个的目录  
            # print( '-' * (int(dirList[0])), dl)  
            # 打印目录下的所有文件夹和文件，目录级别+1  
            printPath((int(dirList[0]) + 1), path + '/' + dl)  
    for fl in fileList:  
        # 打印文件  
        dirPath='pack/'+path
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        
        # print ('-' * (int(dirList[0])), fl ) 
        
        writer=open(dirPath+'/' + fl,'w+',encoding='utf-8')    
        writer.write(readtype(path + '/' + fl))
        writer.close()    
        
        # 随便计算一下有多少个文件  
        allFileNum = allFileNum + 1  
  
# if __name__ == '__main__':  
printPath(1, '晋江2003~2021文包')  
print ('总文件数 =', allFileNum)