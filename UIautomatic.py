import uiautomator2 as u2
import time
import json
def record_comment(passages,comment_number):
    passages.click()
    
    scroll_flag=True
    temporary_list=[]
    while scroll_flag:
        d.xpath("//android.widget.TextView[@index='3']").wait(1)
        for comments in d.xpath("//android.widget.TextView[@index='3']").all():
            if comments.text in temporary_list:
                scroll_flag=False
            else:
                # comments_list[page].append(comments.text)
                temporary_list.append(comments.text)
                # print(comments.text)
        if comment_number<=4 :
            break
        time.sleep(0.5)
        # d(scrollable=True).scroll(steps=3)
        try:
            d(scrollable=True).scroll(steps=2)
        except:
            print ("can't scroll")
            break
            # return temporary_list
    
    if d(resourceId="com.dragon.read:id/x").exists:
        d.press("back")
    return temporary_list
def next_page():
    displayHeight=2304
    displayWidth=1080
    d.swipe(displayWidth/2+100, displayHeight/2, displayWidth/2-100, displayHeight/2,0.1)

d = u2.connect('182QGFZD222DZ')
print(d.info)

comments_list=[]
for page in range(3143,5000):
    
    # d(resourceId='com.dragon.read:id/bw5').click()
    # print('Page',i)
    d.xpath("//*[contains(@resource-id, 'com.dragon.read:id/bw5')]").wait(1)
    for passages in d.xpath("//*[contains(@resource-id, 'com.dragon.read:id/bw5')]").all():        
        try:
            comment_number=int(passages.text.strip())
        except:
            comment_number=100
        print('评论',comment_number)
        # record_comment(passages,comment_number)
        comments_list.append({page:record_comment(passages,comment_number)})

    for passages in d.xpath("//*[contains(@resource-id, 'com.dragon.read:id/bvl')]").all():       
        try:
            comment_number=int(passages.text.split('・')[1].strip())
        except:
            comment_number=100
        
        comments_list.append({page:record_comment(passages,comment_number)})
        # next_page()
        print('章末评论',comment_number)
        # time.sleep(6)
    if d.xpath('//*[@resource-id="com.dragon.read:id/c71"]').exists:
        print('广告')
        time.sleep(6)
    if len(comments_list) :
        writer=open('output/%d.json'%(page),'w',encoding='utf-8')
        writer.write(json.dumps(comments_list,indent=4,ensure_ascii=False))
        writer.close()
        comments_list=[]
    # else:
    #     page-=1
    next_page()
    
