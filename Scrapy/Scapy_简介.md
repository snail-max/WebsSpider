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
        启动scrapy文件
            scrapy crawl 爬虫名称

    -scrapy数据解析
    
    -scrapy持久化存储
        基于终端命令的
            要求：只可以将parse方法的返回值存储到本地文件中
            注意:存储的格式只包括json，jsonlines，jl,csv,  
            指令：scrapy crawl xxx -o filename
        基于管道
            编码流程：
                数据解析
                在item类的定义相关的属性
                将解析的数据封装到item类型的数据中
                将item类型的对象提交给管道进行持久化存储
    
    
    

    
