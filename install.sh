# clone the submodule for darknet
git submodule update --init

# compile darknet source
cd darknet && make && cd ../

# rename the database file
mv db.sample.sqlite3 db.sqlite3

# rename the settings file
mv pixi/settings.sample.py pixi/settings.py

# create virtualenv
virtualenv env

# install dependencies in virtualenv
env/bin/pip install django

# run django migration
env/bin/python manage.py migrate