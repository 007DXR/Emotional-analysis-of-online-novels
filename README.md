# [由“虐”到“甜”：数字人文视角下的女频网文情感转向](https://github.com/007DXR/Emotional-analysis-of-online-novels/blob/main/由“虐”到“甜”：数字人文视角下的女频网文情感转向.pdf)
## 北京大学第三十届“挑战杯”跨学科学生课外学术科技作品竞赛

# 摘要：
本文以数字人文的视角切入，结合传统文学研究当中的社会历史分析、脉
络梳理、文本细读等方法对前人已有的定性研究结论做出量化的证明与阐释。通
过绘制历年代表性文本的情感弧，证明了女频网文由“虐”到“甜”的情感转向
以及伴随其出现的叙事节奏拉平、高潮分散化的现象。借助数字人文辅助，聚焦
“虐”这一概念从情感模式向情节元素的解离，在“虐”的从“文”到“梗”的
文本变化中，发现女性读者情感结构与消费模式的后现代转向。

# 关键词：
数字人文 网络文学 情感弧 甜文 虐文

# 网文数据来源
番茄小说APP
晋江小说城

## 移动端APP爬取文本及评论方法
### 1、uiautomator2
uiautomator2是一个自动化测试开源工具，仅支持Android平台的原生应用测试。python-uiautomator2封装了谷歌自带的uiautomator测试框架，提供便利的python接口，用它可以很便捷的编写python脚本来实现app的自动化测试。

python端：运行脚本，往移动端发送HTTP请求
移动端：安装atx-agent，然后atx-agent启动uiautomator2服务进行监听，并识别python脚本，转换为uiautomator2的代码。
移动设备通过WIFI(同一网段)或USB接收到PC上发来的HTTP请求，执行制定的操作。

### 2、前提环境
Python

Android SDK

uiautomator2：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --pre -U uiautomator2`

设备上安装atx-agent：`python -m uiautomator2 init`

### 3、uiautomator2连接移动设备的三种方法
参考[link](https://www.cnblogs.com/qingchengzi/articles/14642737.html)

`import uiautomator2 as u2`

### U2控制移动设备

 连接手机的USB进行连接(安卓模拟器和真机都可以）必须开启USB调试模式
 CSQBL5000123456为手机序列号，`adb devices`查看
`d = u2.connect_usb("CSQBL5000123456")`
`print(d.info)`


