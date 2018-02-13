Installation:
=============

```
sudo apt-get install python-pip python-dev build-essential libpq-dev nginx git virtualenv supervisor

cd /root
virtualenv -p python3 bcoreproject
cd bcoreproject && source bin/activate
git clone https://github.com/sheriefalaa/bcoreproject-backend bcoreproject-backend-src/
cd bcoreproject-backend-src/
pip install -r requirements.txt
cp bcoreproject/settings.py.example bcoreproject/settings.py
python manage.py migrate
python manage.py makemigrations bcoreproject
python manage.py migrate
python manage.py collectstatic
chown -R www-data:www-data static/
cp -ra static /var/www/.
python manage.py createsuperuser

chmod u+x /root/bcoreproject/bcoreproject-backend-src/deployment/gunicorn-start.bash
cp /root/bcoreproject/bcoreproject-backend-src/deployment/gunicorn.conf /etc/supervisor/conf.d/.
mkdir /root/bcoreproject/bcoreproject-backend-src/logs/
supervisorctl reread && supervisorctl update
rm /etc/nginx/sites-available/default
cp /root/bcoreproject/bcoreproject-backend-src/deployment/nginx.conf /etc/nginx/sites-available/bcoreproject.conf
ln -s /etc/nginx/sites-available/bcoreproject.conf /etc/nginx/sites-enabled/
systemctl restart supervisor && systemctl restart nginx
```
