import ldap
#from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

# Constants
AUTH_LDAP_SERVER = 'isaac.carthage.edu'
AUTH_LDAP_BASE_USER = "cn=webldap, o=CARTHAGE"
AUTH_LDAP_BASE_PASS = "w3Bs1t3"

class LDAPBackend:
    def authenticate(self, username=None, password=None):
        if not password:
            #raise PermissionDenied
            return None
        username = username.lower()
        base = "o=CARTHAGE"
        scope = ldap.SCOPE_SUBTREE
        filter = "(&(objectclass=person) (cn=%s))" % username
        ret = ['givenName','sn','email']

        # Authenticate the base user so we can search
        try:
            l = ldap.initialize('ldaps://isaac.carthage.edu:636')
            l.protocol_version = ldap.VERSION3
            l.simple_bind_s(AUTH_LDAP_BASE_USER,AUTH_LDAP_BASE_PASS)
        except ldap.LDAPError:
            return None

        try:
            result_id = l.search(base, scope, filter, ret)
            result_type, result_data = l.result(result_id, 0)
            # If the user does not exist in LDAP, Fail.
            if (len(result_data) != 1):
                return None

            # Attempt to bind to the user's DN - we don't need an if here. simple_bind will except if it fails, never return a value
            l.simple_bind_s(result_data[0][0],password)

            # The user existed and authenticated. Get the user record or create one with no privileges.
            # Could use get_or_create here, but I don't want to be creating random passwords constantly for no reason.

            try:
                user = User.objects.get(username__exact=username)
                if not user.last_name:
                    user.last_name = result_data[0][1]['sn'][0]
                    user.first_name = result_data[0][1]['givenName'][0]
                    user.save()
            except:
                # Theoretical backdoor could be input right here. We don't want that, so we input an unused random password here.
                # The reason this is a backdoor is because we create a User object for LDAP users so we can get permissions, however
                # we -don't- want them to be able to login without going through LDAP with this user. So we effectively disable their
                # non-LDAP login ability by setting it to a random password that is not given to them. In this way, static users
                # that don't go through ldap can still login properly, and LDAP users still have a User object.
                from random import choice
                import string
                temp_pass = ""
                for i in range(8):
                    temp_pass = temp_pass + choice(string.letters)
                user = User.objects.create_user(username,username + '@carthage.edu',temp_pass)
                #student_group = "ou=STUDENTS"
                staff_group = "ou=STAFF"
                faculty_group = "ou=FACULTY"
                # result_data returns [('cn=username,ou=GROUP,o=CARTHAGE', {})]
                group = result_data[0][0].split(',')[1]
                if group==staff_group or group==faculty_group:
                    user.is_staff = True
                else:
                    user.is_staff = False

                user.first_name = result_data[0][1]['givenName'][0]
                user.last_name = result_data[0][1]['sn'][0]
                user.save()
            # Success.
            return user

        except ldap.INVALID_CREDENTIALS:
            # Name or password were bad. Fail permanently.
            #raise PermissionDenied
            return None

    def get_user(self, user_id):
        """
        OJO: needed for django auth, don't delete
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
