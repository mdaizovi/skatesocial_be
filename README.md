# Skate Social (name TBD) backend

blah blah blah

## GeoDjango specific installation issues

I expect [GeoDjango](https://docs.djangoproject.com/en/4.0/ref/contrib/gis/tutorial/) to be a PITA when deploying. Here are notes from getting it to work locally.

## GeoDjango specific installation issues

Problems with mysql, it stopped responding. Will [this](https://coderwall.com/p/os6woq/uninstall-all-those-broken-versions-of-mysql-and-re-install-it-with-brew-on-mac-mavericks) fix it?

- needed GDAL
  - `brew install gdal`

Problems with content types etc so this was the command that finally worked:

`python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission -e admin.logentry --indent 4 > db.json`

Remember you also had to start on an empty db, migrate, and then `python manage.py loaddata db.json`
