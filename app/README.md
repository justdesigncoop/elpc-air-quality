# App installation instructions

0. Add user if necessary:

```
adduser elpcjd
usermod -aG sudo,adm elpcjd
```

1. Update and upgrade the system:

```
apt update
apt upgrade
```

2. Install the following software packages:

```
apt install git curl software-properties-common build-essential nano run-one
```

3. Install [MariaDB 10.2](https://downloads.mariadb.org/mariadb/repositories):

```
apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://nyc2.mirrors.digitalocean.com/mariadb/repo/10.2/ubuntu xenial main'
apt update
apt install mariadb-server libmysqlclient-dev
```

4. Download and [install](https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-16-04) [Miniconda2](https://conda.io/docs/user-guide/install/index.html):

```
cd /tmp
curl -O https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
sh Miniconda2-latest-Linux-x86_64.sh
```

5. Clone the repository:

```
git clone https://github.com/justdesigncoop/elpc-air-quality.git
```

5. Initialize the database:

```
cd elpc-air-quality/db
mysql -u root -p < create_db.sql
```

4. Create MariaDB user:

```
mysql -u root -p
CREATE USER 'elpcjd'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON elpc_air_quality.* TO 'elpcjd'@'localhost';
FLUSH PRIVILEGES;
exit
```

6. Create virtual environment:

```
apt install python-pip
pip install --upgrade pip
pip install virtualenv virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv elpcjd
pip install -r requirements.txt
```

Add the following to the end of ~/.bashrc:

```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME
source /usr/local/bin/virtualenvwrapper.sh
```

7. Preapre and test Django app:

```
workon elpcjd
cd app
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

10. Add the following to /etc/apache2/apache2.conf:

```
# Alias /robots.txt /path/to/mysite.com/static/robots.txt
# Alias /favicon.ico /path/to/mysite.com/static/favicon.ico

# Alias /media/ /path/to/mysite.com/media/
Alias /static/ /var/www/static/

<Directory /var/www/static>
  Require all granted
</Directory>

# <Directory /path/to/mysite.com/media>
#   Require all granted
# </Directory>

WSGIScriptAlias / /home/elpcjd/elpc-air-quality/app/elpc_air_quality/wsgi.py
WSGIPythonHome /home/elpcjd/.virtualenvs/elpcjd
WSGIPythonPath /home/elpcjd/elpc-air-quality/app

<Directory /home/elpcjd/elpc-air-quality/app/elpc_air_quality>
  <Files wsgi.py>
    Require all granted
  </Files>
</Directory>
```

8. Deploy Django app:

```
apt install apache2 libapache2-mod-wsgi phpmyadmin libspatialindex-dev
python manage.py collectstatic
python manage.py createsuperuser
/etc/init.d/apache2 restart
```

9. Change to correct time zone:

```
rm /etc/localtime
ln -s /usr/share/zoneinfo/America/Chicago /etc/localtime
w
```

10. Create a crontab entry for the database scripts (e.g. runs every morning at 2 am):

```
crontab -e
0 2 * * * run-one /home/elpcjd/elpc-air-quality/db/cron_script.sh
```

