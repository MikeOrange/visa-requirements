# Visa Requirements
(Project in progress)


Webpage to visualize visa requirements for all countries from info available on Wikipedia. Uses [jqvmap](https://github.com/manifestinteractive/jqvmap) to visualize the data. Includes scripts to scrap and parse content from Wikipedia using [requests](http://docs.python-requests.org/en/master/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) 

### Install and run
 - Install and activate virtualenv
 - Install backend requirements in the virtualenv depending on the environment you are at:
```sh
$ pip install -r requirements.txt # Production
$ pip install -r requirements/dev.txt # Development
```


- Install frontend requirements using: (you need to install bower previously using npm)
```sh
$ bower install
```
 - Create database and set environment variables as indicated on [environment variables](#environment-variables)
 - Create database schema using:
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```
- Fill database with data from wikipedia using (in the same order)
```sh
$ python manage.py fill_demonyms
$ python manage.py fill_requirements
```
- Run project
```sh
$ python manage.py runserver
```

### Environment variables
```sh
export VISAREQUIREMENTS_DB_NAME="Database name."
export VISAREQUIREMENTS_DB_USER="Database user."
export VISAREQUIREMENTS_DB_PASSWORD="Database password."
export VISAREQUIREMENTS_DB_HOST="Database host."
export VISAREQUIREMENTS_DB_PORT="Database port."
```

### TODO
- Manage map clicking event to show details about destination country.
- Make webpage responsive.
- Add Requirements by destination instead of origin.
- Add Curiosities found in the data.
- Add About page.

### Preview
![](docs/preview.png?raw=true)