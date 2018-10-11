## Virtualenv入门基础教程
1. pip安装virtualenv：
`pip3 install virtualenv`

2. 创建虚拟环境
`virtualenv venv`

3. 命令激活虚拟环境
(Microsoft Windows) `venv\Scripts\activate`
(mac) $ source venv/bin/activate

4. 安装flask(这里使用了豆瓣)
`pip3 install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com flask`

5. 测试是否安装了依赖包
`pip3 freeze`

6. 退出虚拟环境
`deactivate`

[参考链接：http://flask123.sinaapp.com/article/39/](http://flask123.sinaapp.com/article/39/)

## 项目开发

1. 项目目录

2. 构建蓝图

    * 定义蓝图（app/admin/__init__.py）
    from flask import Blueprint
    admin = Blueprint("admin",__name__)
    import views
    * 注册蓝图（app/__int__.py）
    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint,url_prefix="/admin")
    * 调用蓝图(app/admin/views.py)
    from .import admin
    @admin.route("/")
    
[flask使用Blueprint进行多模块应用的编写](https://blog.csdn.net/u012734441/article/details/67631564)

3. 会员及会员登录日志数据模型设计

    * 安装数据库连接依赖包 pip install flask-sqlalchemy
    `pip3 install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com flask-sqlalchemy`
    * 连接数据库
    （mac）mysql -uroot -proot 
    （windows）打开MySQL CLC 输入密码，\s，mysql> create database movie;
    mysql> create database movie;
    * 定义mysql数据库连接
    from flask_sqlalchemy import SQLAlchemy
    from falsk import Flask
    * 声明模型
    [http://www.pythondoc.com/flask-sqlalchemy/models.html](http://www.pythondoc.com/flask-sqlalchemy/models.html)
    
4. 标签、电影、上映预告数据模型设计

5. 评论及收藏电影数据模型设计

6. 权限及角色数据模型设计

7. 管理员、登录日志、操作日志数据模型设计

8. 运行数据库模型
`(venv) E:\Python\movie-website\app>python models.py`
```
// 数据库操作
    mysql> use movie;
    mysql> show tables;
    mysql> desc admin;
```
#### 注意
> 数据库中文报错
```
    role = Role(name="superAdmin",auths="")   // 没有问题，但如果name是中文：超级管理员，就会报错。
    db.session.add(role)
    db.session.commit()
```
[参考：https://blog.csdn.net/Jesszen/article/details/82056402](https://blog.csdn.net/Jesszen/article/details/82056402)
> 解决办法：`mysql> alter database movie character set utf8mb4;`
> 最后总结：字符串问题，如果mysql部署在Linux下，则可以解决；如果mysql部署在windows下，则依然会报错，只不过没啥影响，原因在pymysql的驱动存在问题。

[Flask-SQLAlchemy:https://www.cnblogs.com/carlo/p/4628971.html](https://www.cnblogs.com/carlo/p/4628971.html)

## 前台布局搭建
1. 静态文件引入： {{ url_for('static', filename = '文件路径')}}
2. 定义路由： {{ url_for('模块名.视图名', 变量 = 参数)}}
3. 定义数据块： {% block数据块名称 %} ... {% endblock %}

## 登录
@home.route("/login/")
def login():
return render_template("home/login.html")

## 退出
@home.route("/logout/")
def logout():
return redirect(url_for('home.login'))

## 注册

@home.route("/regist/")
def regist():
    return render_template("home/regist.html")
    
## 后台（管理页面）布局搭建
> app -> admin -> views.py
```python
# coding:utf8
from . import admin
from flask import render_template, redirect, url_for

@admin.route("/")
def index():
    return "<h1 style='color:red'>管理页面</h1>"

@admin.route("/login/")
def login():
    return render_template("admin/login.html")

@admin.route("/logout/")
def logout():
    return redirect(url_for("admin.login"))
```

## 管理员登录
1. app/__init__.py中创建db对象
2. app/models.py中导入db对象
3. app/admin/forms.py中定义表单验证
4. app/templates/admin/login.html中使用表单字段、信息验证、消息闪现
5. app/admin/view.py中处理登录请求、保存会话
6. app/admin/view.py定义登录装饰器、访问控制



