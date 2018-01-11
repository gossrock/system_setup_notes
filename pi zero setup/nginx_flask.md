initially from:

 https://iotbytes.wordpress.com/python-flask-web-application-on-raspberry-pi-with-nginx-and-uwsgi/

and

 http://vladikk.com/2013/09/12/serving-flask-with-nginx-on-ubuntu/

and

https://askubuntu.com/questions/927881/running-a-flask-app-on-startup-with-systemd#928829


update system:
```
sudo apt update
sudo apt upgrade -y
```
install nginx:

```
sudo apt install -y nginx
```

start nginx:
```
sudo service nginx start
```

if not already done, install requirements for venv:

```
sudo apt install -y python3-pip
sudo apt install -y python3-venv
```

create and activate venv for project:
```
mkdir ~/project_name
cd project_name
python3 -m venv .venv3
source .venv/bin/activate
```

install flask
(with venv still active)
```
python -m pip install flask
```

install uwsgi:

(with venv still active)
```
python -m pip install uwsgi
```


create simple app:

```
mkdir ~/project_name/app
nano ~/project_name/app/app.py

```

in app.py
```
from flask import Flask
first_app = Flask(__name__)

@first_app.route("/")
def first_function():
 return "<html><body><h1 style='color:red'>I am hosted on Raspberry Pi !!!</h1></body></html>"

if __name__ == "__main__":
 first_app.run(host='0.0.0.0')
 ```

test with python:
```
python ~/project_name/app/app.py
```

browse to ip_of_server:5000


test with uwsgi:

```
cd ~/project_name/app
uwsgi --socket 0.0.0.0:8000 --protocol=http -w app:first_app
```



```
nano uwsgi_config.ini
```

in uwsgi_config.ini put the following:
```

```
