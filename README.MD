# AI Chat Room #

# Demo
<p align="center">
<img src="docs/chat_app_demo.gif" alt="animated" />
</p>
<p align="center">
Live Demo: <a href="">AI Chat Room</a></br>
[live demo may be down due to hosting costs]
</p>

# Introduction

AI Chat Room is text based chat web application that users can converse with AI chat bots. The AI model being utilized is the "microsoft/DialoGPT-large" and the AI voices are provided by the Uberduck API. 

Tech Stack:
* Docker
* Django
* REDIS
* Celery
* microsoft/DialoGPT-large
* UberDuck API

Key Features:
* Search for specific voices
* Text based chat with AI
* AI also provides audio response


## Configuration

Create .env file and populate with the following credentials
```bash
DB_NAME=<postgres_name>
DB_USER=<postgres_username>
DB_PASS=<postgres_password>
REDIS_PASS=<redis_password>
UBERDUCKKEY=<public_key>
UBERDUCKSEC=<private_key>
```

## Installation/Deployment

1. Install Docker Compose: https://docs.docker.com/compose/install/

2. Double check to make sure updated .env is in base directory

3. Run following command

```bash
sudo docker-compose run web django-admin startproject chatt_app .
```

4. edit permissions

```bash
sudo chown -R $USER:$USER chat_app manage.py
```

5. edit settings.py and add to db section

```python
# settings.py
   
import os
   
[...]
   
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}
```

6. Run it
```bash
docker-compose up -d
```


## Contributing
Feel free to fork my work. This project is not actively maintained.

## Maintainers
Andrew Johnson

## License
[MIT](https://choosealicense.com/licenses/mit/)
