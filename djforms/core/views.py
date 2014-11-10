def not_in_group(user):
    if user:
        staff = user.groups.filter(name='carthageStaffStatus').count() == 0
        faculty = user.groups.filter(name='carthageFacultyStatus').count() == 0
        notin = False
        if staff or faculty:
            notin = True
        return notin
    return False
