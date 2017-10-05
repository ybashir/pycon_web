# PyCon Website

This website code is based on Mezzanine which is a Python based CMS. Please read more about it here: 

http://mezzanine.jupo.org

To recreate the dev set-up:

* create a virtualenv (based on Python 2.7 not 3)
* clone the repo
* run ```pip install -r requirements.txt```
* create a local_settings.py file similar to the one listed in mezzanine docs
* run ```python manage.py migrate```
* run ```python manage.py collectstatic```
* run ```python manage.py runserver```

There are a few additional things you need to do to get the homepage showing up in your local environment:

* add all of the theme images to the media gallery. For this, log on to the local admin (typically http://localhost:8000/admin) then upload the entire hierarchy from /theme/static/img to the media gallery. Because we want content authors to be able to modify the images themselves, we need to replicate them in the media library

* create a new page called Home (with slug / in meta-data). The content for this page can be obtained from the staging site (Currently pycon.arbisoft.com) by logging in as admin and copying the html source for home over to your local dev CMS.

Now your homepage should start appearing.

You can make changes to the code and submit a PR. Ill review your changes and integrate.
