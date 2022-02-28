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

See requirements.txt

TrustCommerce python library:
https://vnvault.trustcommerce.com/downloads/tclink-4.2.0-python.tar.gz

with your python venv sources:

cd /data1/source/tclink-4.2.0-python
python setup.py install

the above directory has the patch applied. future 5.4.x might have it fixed.

_Apps list for Migrations_

admin, admindocs, admissions, admitted, auth, bootstrapform, captcha, catering, characterquest, choral, classnotes, committee_letter, conference, contenttypes, copyprint, core, django_countries, djtools, genomics, giving, green, honeypot, humanize, imagekit, languages, lis, memory, metamorphosis, printrequest, processors, proposal, registration, scholars, security, sites, soccer, summer_camp, taggit, userprofile, visitdays, writingcurriculum
