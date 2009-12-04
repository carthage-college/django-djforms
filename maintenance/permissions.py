from authority import permissions, register
from djforms.maintenance.models import MaintenanceRequest


class MaintenanceRequestPermission(permissions.BasePermission):
    label = 'maintenance_permission'
    checks = ('review','update','delete',)

register(MaintenanceRequest, MaintenanceRequestPermission)
