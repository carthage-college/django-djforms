# Various things to do after submissions have ended

1. Print:

https://www.carthage.edu/forms/scholars/presentation/print/

2. Mugshots:

python munge_mugshot.py

will give you a list of files, which you can then use to tar:

python tar_mugshots.py

3. Posters:

python munge_poster.py --test --year=xxxx > scholars.posters.txt

execute tar with a file as the list of files for archiving:

tar cvf posters.tar  --files-from=scholars.posters.txt

4.
