Automatic discover of LDAP services
===================================

This addon will add automatic discovery of the LDAP server to use
for django-ldap-auth. It requires version 1.1.6+ of django-ldap-auth
and dnspython.

If your company/organization is publishing the LDAP servers via DNS
SRV records you just need to add the following to you django settings.py:
```
import ldap_auto_discover

AUTH_LDAP_AUTODISCOVER_DOMAIN = "yourcompanydomain.com"
AUTH_LDAP_SERVER_URI = discover_ldap_servers
```

Troubleshooting
---------------

You can check what records are published via:
```
$ nslookup -type=SRV _ldap._tcp.your.domain.com
```

and compare to:
```
$ python ldap_auto_discover.py your.domain.com
```


Tests
-----

Run the tests via
```
$ PYTHONPATH=. python tests/test_discover.py
```