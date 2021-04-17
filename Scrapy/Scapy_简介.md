scrapy框架

什么是框架
    就是一个集成了多个功能并且具有很强通用性的项目模板
如何学习框架
    专门学习框架中各个功能的详细用法

scrapy矿架的基本使用
    -环境安装
        windows
        pip install wheel
        下载twisted https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
        安装twisted pip install Twisted-20.3.0-cp37-cp37m-win_amd64.whl
        pip install pywin32
        pip install scrapy
        测试：在终端中输入scrapy没有报错，为安装成功
    - 创建一个工程：scrapy startproject
    cd 工程目录
    -在子目录中创建一个爬虫文件
        scrapy genspider spiderName  www.xxx.com
    
