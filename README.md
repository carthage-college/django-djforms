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

_Apps list for Migrations_

admin, admindocs, admissions, admitted, auth, bootstrapform, captcha, catering, characterquest, choral, classnotes, committee_letter, contenttypes, copyprint, core, django_countries, djtools, genomics, giving, green, honeypot, humanize, imagekit, languages, lis, memory, metamorphosis, printrequest, processors, proposal, registration, scholars, security, sites, soccer, summer_camp, taggit, userprofile, visitdays, writingcurriculum
