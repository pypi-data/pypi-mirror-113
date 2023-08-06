# Global Menu

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django)
![PyPI - Django Version](https://img.shields.io/pypi/djversions/djangorestframework)

The Global Menu is an open-source build for python-django framework. It provides an easy way to create menu base on model. 

## Get Started

To get started build menu :
1. Add `gmenu` to your `INSTALLED_APPS` setting like this :
```python
    INSTALLED_APPS = [
        ...
        'gmenu',
    ]
```

2. Include the gmenu URLconf in your project urls.py like this::
```python
    path('', include('gmenu.urls')),
```

3. On root folder (where `manage.py` reside), run `python manage.py migrate` to create the menu models.

4. On same folder as above, run `python manage.py createsuperuser` to create super user, so you have access to admin page.

5. Start the development server and visit `http://127.0.0.1:8000/admin/`
   
6. Click on `Menus` and then `add menu +`. Field you have to full field is `user` and `name`
The complete fields is :

    Field Name | Value
    ------------ | -------------
    `user` | choose username you have been create on step 4
    `parent` | parent menu, leave it blank if you want to create root menu
    `name` | menu name, appear in your project
    `link` | where to go if user click this menu
    `icon` | you can use awesome font from bootstrap
    `order menu` | order number menu
    `kind` | `frontend without login` or `frontend with login` or `backend` menu
    `is visible` | make menu visible or invisible
    `is master menu` | make menu avilable for another user
    `is statis menu` | make menu have access to statis page (the page is created by user)
