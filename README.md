# 贝壳租房爬虫(Scrapy)

---

<h3 id="Q&A">问题反馈</h3>
在使用中有任何问题，可以反馈给我，以下联系方式跟我交流

* Author: Leo
* Wechat: Leo-sunhailin 
* E-mail: 379978424@qq.com 
* Github URL: [项目链接](https://github.com/sunhailin-Leo/BeiKeZuFangSpider)

---

<h3 id="DevEnv">开发环境</h3>

* 系统版本: Windows 10 x64

* Python版本: Python 3.6.4

* 编译器: Pycharm 2018.2.3 x64

---

<h3 id="ProjectDependency">项目依赖</h3>

* Scrapy: 1.5.0

* pymongo: 3.7.1

* lxml: 4.2.4

* requests: 2.18.4


---

<h3 id="StartWays">启动方式</h3>

* EXE启动(下载release里面的exe --- 等待打包) ---> 暂时无法打包(求解决!!!!!有打包过的给个issue!)

* 命令启动(clone项目) --- 启动方法在cmdline_start_spider.py

---

<h3 id="FutureWork">未来的开发方向</h3>

1. 添加查询规则(通过配置规则进行爬取) -- 具体方案待定


---

<h3 id="OtherSomething">其他说明以及功能说明</h3>

* 如果Windows下的开发,运行Scrapy出现找不到win32api模块, 请安装libs下的exe文件(64位系统)
* 增加CSV导出功能(可以在配置文件中配置是否导出到CSV中)
    * 在判断MongoDB没有配置或者配置后首次连接无法连上, 则自动切换到CSV导出
    * 导出路径为根目录的ExportData文件夹(下个版本进行自定义修改)

---
