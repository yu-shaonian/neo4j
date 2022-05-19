## 使用
### 需要在环境装Django，还有医疗知识图谱的部分
### 现在用的是医疗知识图谱,使用前需要导入好图谱，文件在chat/QA_med
### 请修改chat/QA_med 中的answer_search中数据库账号密码
### 运行的话pycharm可以直接下面run点绿色三角按钮，或者在terminal中输入
```
    python manage.py runserver
    # 每次初始化需要一定时间
```


## 法律一问一答（选中网页中功能跳转中的民事问题 或者 http://127.0.0.1:8000/law_citizen）
### 需要验证部分在chat/views中的
```
    handler_crime = CrimeQA()   # 法律问答
    
    
    # 该方法的使用在crimeqa函数中
    ans = handler_crime.search_main(user_qs)
```
### CrimeQA（）的实例化方法是问答模块，这部分包没装好，不确定会有哪些路径问题。
### QA_crime是源自https://github.com/liuhuanyong/CrimeKgAssitant