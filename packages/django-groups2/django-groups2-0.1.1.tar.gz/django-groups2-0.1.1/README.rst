==============
django-groups2
==============

Capabilities
------------

* Adds a ``Group2`` model to improve upon the django.auth.Group
* Adds a ``Group2Kind`` model to have group kinds
* Adds various needed properties to ``Group2``
* Adds a proper hierarchy using https://github.com/django-treebeard/django-treebeard (editable through django-admin)
* Has an one-to-one relationship with builtin `Group` (created automatically on save) which is used to keep user members and any needed permissions
* Allows user membership to be edited through django-admin

Requirements
------------

This works with Django 3+ and Python 3.6+. It will also install ``django-treebeard``.

Installation
------------

Run 

``pip install django-groups2``

Add  ``"groups2"`` and ``"treebeard"`` to your ``INSTALLED_APPS`` setting.

Changelog
---------

v.0.1.1
=======

- Fix bug with not including templates

v.0.1.0
=======

- Initial version


