# lab # 7

## Prerequisites

You will need [Python 3.8](https://www.python.org/downloads/) or above installed.

In addition, it is required to install [mkcert](https://github.com/FiloSottile/mkcert#installation) for making locally-trusted development certificates.

## Installing

```commandline
mkcert -install
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1 ::1
```

```commandline
pip install -r requirements.txt
```

## Running

### Run migrations

```commandline
python manage.py migrate
```

### Creating an admin user

```commandline
python manage.py createsuperuser
```

### Starting development server

```commandline
python manage.py runsslserver --certificate cert.pem --key key.pem
```

Go to [https://127.0.0.1:8000/](https://127.0.0.1:8000/)
