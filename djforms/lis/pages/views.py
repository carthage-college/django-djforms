# -*- coding: utf-8 -*-
from django.shortcuts import render
from djtools.decorators.auth import group_required


@group_required('carthageFacultyStatus', 'carthageStaffStatus')
def downloads(request):
    return render(request, 'lis/downloads.html', {})
