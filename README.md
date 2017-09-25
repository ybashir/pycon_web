# PyCon Website

This website code is based on Mezzanine which is a Python based CMS. Please read more about it here: 

http://mezzanine.jupo.org

To recreate the dev set-up:

* create a virtualenv with Python 2.7
* clone the repo
* run ```pip install -r requirements.txt```
* create a local_settings.py file similar to the one listed in mezzanine docs
* run ```python manage.py migrate```
* run ```python manage.py collectstatic```
* run ```python manage.py runserver```

You can make changes to the code and submit a PR. Ill review your changes and integrate.
