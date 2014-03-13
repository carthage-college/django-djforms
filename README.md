djforms
===============

Django applications that manage data submitted by the campus community.

Logs

project requires a logs directory in the djforms directory, writeable by webserver.

cd djforms
mkdir logs
touch logs/debug.log
chmod 666 logs/debug.log

Required third party packages:

git@github.com:jezdez/django-authority.git
http://code.google.com/p/django-tagging/

_Required but woefully out of date:_

django-profile

http://code.google.com/p/django-profile/

Here's a fork of the original on github:

https://github.com/tualatrix/django-profile

Replace with?
https://github.com/stephrdev/django-userprofiles

django-imagekit

we only use this for alumni memory form. we should dump that app
or refactor it with the current imagekit project:

git@github.com:matthewwithanm/django-imagekit.git
