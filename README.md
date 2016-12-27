# pixi
A small web app wrapper for darknet image classification.

## Installation
- run ` sh install.sh `, or step-by-step run:
 - ` git submodule update --init `
 - ` cd darknet && make && cd ../ `
 - ` mv db.sample.sqlite3 db.sqlite3 `
 - ` mv pixi/settings.sample.py pixi/settings.py `
 - ` virtualenv env `
 - ` env/bin/pip install django `
 - ` env/bin/python manage.py migrate `

## Running the app in development
- ` env/bin/python manage.py runserver `
