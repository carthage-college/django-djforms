from djforms.alumni.classnotes.forms import ContactForm
from djforms.alumni.classnotes.models import Contact

notes = Contact.objects.all()

suffixes = ["Ph.D","Ph.D.","Ph. D","III","II","CPA","MD","M.D.","M.D","Jr.","USMC"]
salutations = "Rev.","Dr.","Col.","Ms.","Prof.","Chaplain","Colonel","Pastor"

for n in notes:
    name = n.name.split(" ")
    """
    if len(name) > 1:
        if  name[1] == "":
            del name[1]
            n.name = " ".join(name)
            n.save()
    if name[0] == "":
        del name[0]
        n.name = " ".join(name)
        n.save()
    if name[-1] == "":
        del name[-1]
        n.name = " ".join(name)
        n.save()
    if name[0] in salutations:
        n.salutation = name[0]
        del name[0]
        n.name = " ".join(name)
        n.save()
    if name[-1] in suffixes:
        n.suffix = name[-1]
        del name[-1]
        n.name = " ".join(name)
        n.save()
    if name[0] == "The":
        n.salutation = name[1]
        del name[0]
        del name[1]
        n.name = " ".join(name)
        n.save()
    if len(name) == 2:
        n.first_name = name[0]
        n.last_name = name[1]
        n.name = ''
        n.save()
    if len(name) == 3 and len(name[1].split(".")) == 2:
        #print name[0], name[1], name[2]
        n.first_name = name[0]
        n.second_name = name[1]
        n.last_name = name[2]
        n.name = ''
        n.save()
    if len(name) == 3 and len(name[1].split("(")) == 2:
        n.first_name = name[0]
        n.second_name = name[1][1:-1]
        n.last_name = name[2]
        n.name = ''
        n.save()
    if len(name) == 3:
        n.first_name = name[0]
        n.second_name = name[1]
        n.last_name = name[2]
        n.name = ''
        n.save()
    """
    if len(name) == 4:
        print "'%s' | %s" % (n.name, name)

