import datetime
import unittest

from unittest import TestCase
from mock import (
    Mock,
    patch,
)
import dns.resolver
from ldap_auto_discover import ldap_auto_discover


class Results(list):
    expiration = 1234567


class LdapTestCase(TestCase):

    @patch.object(dns.resolver.Resolver, "query")
    def test_discover_ldap(self, mock_query):
        l = Results()
        for i in range(10):
            mock = Mock()
            mock.priority = i / 2
            mock.target.to_text.return_value = "srv%i.%i" % (i / 2, i)
            mock.port = 69
            l.append(mock)
        mock_query.return_value = l
        res = ldap_auto_discover("example.com")
        self.assertIn("ldap://srv4.8:69", res.split(" "))
        self.assertIn("ldap://srv4.9:69", res.split(" "))


if __name__ == "__main__":
    unittest.main()

