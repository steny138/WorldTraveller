# World Traveller
建立自己的世界之旅，從這裡開始。

## 操作說明

### PostgreSql
#### 操作指令(Mac)
* 啟動(背景)：pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
* 關閉：pg_ctl -D /usr/local/var/postgres stop -s -m fast
* 新增資料庫使用者：createuser -s -P <username>
	> -s superuser
	> -P 自訂密碼
* 移除使用者：dropuser <username>
* 新增資料庫 

### Django

* 新增專案： django-admin.py startproject world_traveller
* 修改資料庫： 使用postgresql
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': <database name>,
        'USER': <user name>,
        'PASSWORD': <password>,
        'HOST': '',
        'PORT': '',
    }
}
```
* 建立資料表： python manage.py migrate
* 啟動：python manage.py runserver
* 應用程式建立：python manage.py startapp <application name>
  * 調整 settins.py
  ``` 
  INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '<application name>',
	)
  ```

 ---
 ##### 關於映射model to database
1. 建立準備映射的檔案到migrations資料夾 
	```
	python manage.py makemigrations
	```
 	
2. 產生映射
	```
	python manage.py migrate
	```
