# Various things to do after submissions have ended

0. Set up your shell environment properly in .bash_aliases
so that the DJ Forms settings file is use.

1. Print:

https://www.carthage.edu/forms/scholars/presentation/print/

2. Mugshots:

chown -R username:staff assets/files/scholars/mugshots/

rename files to include user's lastname, firstname:

python scholars/munge_mugshot.py

print out a list of files for tar command:

python tar_mugshots.py > mugshots.txt

cd assets/
tar czvf mugshots.tar.gz --files-from=../scholars/mugshots.txt

chown -R www-data:www-data assets/files/scholars/mugshots/

3. Posters:

chown -R username:staff assets/files/scholars/posters/

python scholars/munge_poster.py --test --year=xxxx > scholars.posters.txt

execute tar with a file as the list of files for archiving:

tar czvf posters.tar.gz  --files-from=scholars.posters.txt

