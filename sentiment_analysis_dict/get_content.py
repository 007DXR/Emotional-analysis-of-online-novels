
'''
使用事先保存在本地的cookies，登录网站
'''
import json
import time
from selenium import webdriver
from sympy import false
ignore_comment=['发评人','投诉删除评论','普通用户','初级vip','审核通过后显示','为营造更好的评论环境']
class Browser_Controller:
    def __init__(self) :
        options = webdriver.ChromeOptions()
        # 设置模拟的设备
        # options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'})
        # 关掉浏览器受到控制的提示
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("service_args=['–ignore-ssl-errors=true', '–ssl-protocol=TLSv1']") # 忽略错误提示
        # options.add_argument('--ignore-certificate-errors') #忽略掉证书错误
        # options.add_argument("headless") #在后台打开浏览器

        self.browser = webdriver.Chrome(options=options)

    def save_text(self,id):
        '''
        保存文本
        text_filename是文件路径，按需求修改
        '''
        text_filename = '黑月光拿稳BE剧本/第%d章.txt'%(id)
        text_file = open(text_filename, 'w',encoding='utf-8')   
        # 小说全文
        novel=self.browser.find_element_by_xpath('''//*[@id="oneboolt"]/tbody/tr[2]/td[1]/div''')
        # print(novel.text)
        text_file.write(novel.text)
        text_file.close()

    def ignore(self,text):
        for i in ignore_comment:
            if i in text:
                return True
        return False

    def save_comment(self,chapterid):
        '''
        保存评论
        '''
        comment_list=[]
        comment_filename= '黑月光拿稳BE剧本/comment第%d章.txt'%(chapterid)
        comment_file = open(comment_filename, 'w',encoding='utf-8') 
        
        for page in range(1,51):
            url='http://www.jjwxc.net/comment.php?novelid=4398312&chapterid=%d&page=%d'%(chapterid,page)
            # url='http://www.jjwxc.net/comment.php?novelid=2503818&chapterid=1&page=1'
            self.browser.get(url)

            time.sleep(0.5)
            targets=self.browser.find_elements_by_class_name('readtd')
            print(id,page,len(targets))
            if len( targets)<=1:
                break
            hidebuttons=self.browser.find_elements_by_xpath('//div[2]/span[2]/span')
            for hidebutton in hidebuttons:
                    hidebutton.click()

            for target in targets[:-1]:   
                try:  
                    comment=target.find_element_by_class_name('readbody')
                  
                    if self.ignore(comment.text):
                        continue
                    
                    comment_file.write(comment.text+'\n')
                    # reply_list=[]              
                    # replys=target.find_elements_by_class_name('replybody')
                    # for reply in replys:
  
                    #     text=''.join(reply.text.split('\n')[1:-1])
                    #     if len(text):
                    #         reply_list.append(text)
                        # if len(reply.text):
                        #     reply_list.append(reply.text)
                    # comment_list.append({'comment':comment.text,"reply":reply_list})
                except:
                    break

        # comment_file.write(json.dumps(ensure_ascii=False,obj=comment_list,indent=4))
        comment_file.close()
    def login(self,url):
        dxr.browser.get(url)
        dxr.browser.delete_all_cookies()

        # 读取之前已经储存到本地的cookie
        cookies_filename = './my_cookies.json'
        cookies_file = open(cookies_filename, 'r', encoding='utf-8')
        cookies_list = json.load(cookies_file)
        for cookie in cookies_list:  # 把cookie添加到本次连接
            dxr.browser.add_cookie({
                'domain': cookie['domain'],  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': '/',
                'expires': None        
            })
            print('add',cookie['name'])

        # 再次访问网站，由于cookie的作用，从而实现免登陆访问
        dxr.browser.get(url)
if __name__=='__main__':
    dxr=Browser_Controller()

   
    dxr.login('http://my.jjwxc.net/onebook_vip.php?novelid=4398312&chapterid=52')
    # chapterid是章节数，按小说具体情况修改
    for chapterid in range(13,140):
        # novelid是小说id，按小说具体情况修改
        # dxr.browser.get('http://my.jjwxc.net/onebook_vip.php?novelid=4398312&chapterid=%d'%chapterid)
        # dxr.save_text(chapterid)
        dxr.save_comment(chapterid)
    # for chapter_id in [1]:
    #     dxr.save_comment(chapter_id)
        
    dxr.browser.close()
