# Guinicor startup shell script
gunicorn --chdir app wsgi:app -w 2 --threads 2 -b 0.0.0.0:80