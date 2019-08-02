## 建站基础
1. 安装Django
`pip install Django`
2. 测试是否安装
* cmd > python > 交互解释器 > 输入：
```
>>> import django
>>> django.__version__
'2.2.3'
```
3. 创建项目
```
C:\Users\用户名>d:

D:\>django-admin startproject MyDjango

D:\>cd MyDjango

D:\MyDjango>code .

```
4. 目录结构
```
+-- MyDjango
|   +-- MyDjango // 文件夹
|   |   +-- __init__.py // 初始化文件
|   |   +-- settings.py // 项目配置文件
|   |   +-- urls.py     // 项目的URL设置，网站的地址信息
|   |   +-- wsgi.py     // Python服务器网关接口
|   +-- manage.py // 命令行工具
```
5. 新建项目应用
* 网站首页
`python manage.py startapp index`
* 用户中心
`python manage.py startapp user`
6. index项目目录
```
+-- MyDjango
|   +-- index // 文件夹
|   |   +-- migrations  // 用于数据库的迁移
|   |   |   +-- __init__.py // 初始化文件
|   |   +-- __init__.py // 初始化文件
|   |   +-- admin.py    // 当前APP的后台管理系统
|   |   +-- apps.py     // 当前APP的配置信息
|   |   +-- models.py   // 定义映射类关联数据库，实现数据持久化，即MTV里面的模型（Model）
|   |   +-- tests.py    // 自动化测试的模块
|   |   +-- views.py    // 逻辑处理模块，即MTV里面的视图（Views）
```
7. 运行
`python manage.py runserver 80`
## 配置信息
1. 静态资源设置
```python
# 设置根目录的静态资源文件夹public_static
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'public_static'),
# 设置APP(index) 的静态资源文件夹index_static
os.path.join(BASE_DIR, 'index/index_static')]
```
```
index >> index_static >> index_pic.png
http://localhost/static/index_pic.png
public_static >> public_pic.png
http://localhost/static/public_pic.png
```

## git 远程分支上传
```
git remote add origin https://github.com/wp360/Python.git

git checkout -b myDjango

git status

git add .

git commit -m "add file"

git push

git push --set-upstream origin myDjango
```