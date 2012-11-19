from djforms.alumni.classnotes.models import Contact

notes = Contact.objects.all()

for n in notes:
    #if n.name and not n.last_name:
    if n.name:
        print "%s. %s | %s" % (n.id, n.name, n.last_name)
        #n.last_name = n.name
