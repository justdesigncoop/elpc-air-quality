# App installation instructions

1. Update and upgrade the system:

```
apt update
apt upgrade
```

2. Install the following software packages:

```
apt install git curl software-properties-common build-essential
```

3. Install [MariaDB 10.2](https://downloads.mariadb.org/mariadb/repositories):

```
apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://nyc2.mirrors.digitalocean.com/mariadb/repo/10.2/ubuntu xenial main'
apt update
apt install mariadb-server libmysqlclient-dev phpmyadmin
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
CREATE USER 'elpcjd'@'localhost' IDENTIFIED BY 'Elpc1234';
GRANT ALL PRIVILEGES ON elpc_air_quality.* TO 'elpcjd'@'localhost';
FLUSH PRIVILEGES;
exit
```

6. Create and source conda environment:

```
cd ..
conda update -n base conda
conda env create -f environment.yml
```

7. Preapre and test Django app:

```
source activate elpcjd
cd app
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```