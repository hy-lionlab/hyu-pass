## HY-PASS

한양대학교 Keyword Based Short URL 서비스

## 📦 Requirements

- Ubuntu 18.04 LTS (GNU/Linux)
- [Python](https://docs.python.org/3/) >= 3.7
- [Pipenv](https://github.com/pypa/pipenv)
- [Gunicorn](https://gunicorn.org/)

- [Flask](https://flask.palletsprojects.com/en/1.0.x/)
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
- [Flask-Classful](http://flask-classful.teracy.org/)
- [Flask-QRCode](https://github.com/marcoagner/Flask-QRcode)
- [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/)

- [Docker](https://www.docker.com/)
- [Docker for Mac](https://docs.docker.com/docker-for-mac/)
- [MySQL](https://www.mysql.com/) 또는 [MariaDB](http://mariadb.com/) (Latest)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [GeoIP2](https://dev.maxmind.com/geoip/geoip2/downloadable/)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

- [Vue](https://kr.vuejs.org/v2/guide/index.html)
- [Webpack](https://webpack.js.org/)
- [Vue Ant Design](https://vue.ant.design/docs/vue/introduce/)

## 🔥 관리자 기능 개발 시 주의 사항

관리자 기능 개발 시 `@auth.login_required` 데코레이터를 주석 처리 해야될 수도 있습니다. (참고!) 

## 🔥🔥 Development Environment

Based on Mac OSX Mojave

```
# Installation Homebrew

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update

# Pipenv Installation
brew install python3
brew reinstall python3 #python3를 예전에 설치했거나 pip 업그레이드를 한지 시간이 지난 경우
pip3 install pip --upgrade
pip3 --version

pip3 install pipenv
pipenv --version

# Yarn Install
brew install yarn

# Pipenv Package Install & Virutal Env Activate
cd {SOURCE_PATH}
pipenv install

# docker-compose.yaml
docker-compose up -d

# .env 개발환경용 설정
# Flask Running
pipenv shell

# Flask DB
python manage.py db init
python manage.py db upgrade
python manage.py db migrate
```

## 🔥🔥 Deployment

Based on Ubuntu 18.04 LTS

```
# 필수 유틸리티 설치
sudo apt-get update
sudo apt install build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install libmysqlclient-dev

# Python PIP + Pipenv install
sudo apt install python3-pip
pip3 --version # PIP 설치 확인
pip3 install --user pipenv # PIPENV 설치
export PATH="$HOME/.local/bin:$PATH"

# Python 3.7 Install
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 python3.7-dev
sudo ln -sfn /usr/bin/python3.7 /usr/bin/python

# Nginx install
sudo apt install nginx

# Yarn install
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

sudo apt-get update
sudo apt install yarn

yarn --version # Yarn 설치 확인

# Source install
cd ~/
git clone {SOURCE_URL}
cd {$PROJECT_ROOT}

# Python + Yarn Package Install
pipenv install

cd app
yarn install
yarn build

# Supervisor Settings
sudo apt install supervisor
cd /etc/supervisor/conf.d/
sudo vi hypass.conf # config/supervisor/conf.d/hypass.conf 참조

# Nginx Settings
cd /etc/nginx/sites-available
sudo vi default # config/nginx/conf.d/hypass.conf 참조

# Supervisor Applying
sudo supervisorctl reread
sudo service supervisor restart
sudo service nginx restart

# .env 값 설정 (.env.example을 참조)

# Flask DB
python manage.py db init
python manage.py db upgrade
python manage.py db migrate

## Cerbot + Let's Encrypt
sudo apt-get install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update

sudo apt-get install certbot python-certbot-nginx

# 방화벽 443 port 오픈 필수!
sudo certbot --nginx # Certbot Setup

sudo service supervisor restart
sudo service nginx restart
```


## 📖 References

- [Homebrew](https://brew.sh/index_ko)
- [🚀 Pipenv 로 파이썬 가상환경 설정](https://velog.io/@doondoony/pipenv-101)
