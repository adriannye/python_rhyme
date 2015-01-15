# songrhyme

## Installation

*NOTE: Requires [virtualenv](http://virtualenv.readthedocs.org/en/latest/),
[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) and
[Node.js](http://nodejs.org/).*

* `$ git clone git@github.com:adriannye/python_rhyme.git
* `$ mkvirtualenv songrhyme
* `$ pip install -r requirements.txt`
* `$ npm install -g bower`
* `$ npm install`
* `$ bower install`
* `$ python manage.py migrate`
* `$ python manage.py loadperfect`
* `$ python manage.py loadfamily`
* `$ python manage.py loadpos`
* `$ python manage.py runserver`

## Notes

The following are for Heroku deployment:
Procfile 
scripts/postInstall 
.buildpacks
