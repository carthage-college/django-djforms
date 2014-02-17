from djforms.alumni.classnotes.models import Contact

notes = Contact.objects.all()

# files/alumni/classnotes/photos

# 'img/alumniapps/classnotes/photos/headshot' | ['img', 'alumniapps', 'classnotes', 'photos', 'headshot']

for n in notes:
    name = str(n.picture).split("/")
    if len(name) == 5:
        #name [0] = "files"
        #name [1] = "alumni"
        #name = "/".join(name)
        #n.picture = name
        #n.save()
        print "'%s' | %s" % (n.picture, name)

