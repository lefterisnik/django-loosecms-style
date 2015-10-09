========================
Django Loose CMS - Style
========================

A style admin plugin for Django Loose CMS that extends HtmlPageAdmin.

Requirements
------------

Loose CMS Style plugin requires:

* Django version 1.8
* Python 2.6 or 2.7
* loosecms
* tinycss
* beautifulsoup4

Quick Start
-----------

1. Instalation via pip::

    pip install https://github.com/lefterisnik/django-loosecms-style/archive/master.zip

2. Add "loosecms_style" to your INSTALLED_APPS setting after "loosecms" like this::

    INSTALLED_APPS = (
        ...
        'loosecms_style',
        'loosecms',
        ...
    )
 Must be before other Loose CMS plugins.
    
3. Run `python manage.py migrate` to create the loosecms_style models.

4. Run development server `python manage.py runserver` and visit http://127.0.0.1:8000/ to start
   playing with the cms.