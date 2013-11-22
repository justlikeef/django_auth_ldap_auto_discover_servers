Automatic discover of LDAP services
===================================

This is a addon for the AUTH_LDAP_SERVER_URI code in
django-ldap-auth >= 1.1.6 (http://pythonhosted.org/django-auth-ldap/)

To use it, add the following to your django settings.py:
```
from ldap_auto_discover import discover_lap_servers

AUTH_LDAP_SERVER_URI = lambda: discover_ldap_servers("my.domain.com")
```
