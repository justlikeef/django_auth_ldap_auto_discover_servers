from collections import defaultdict
from datetime import datetime, timedelta
import random
import sys

import dns.resolver


class ServerDiscoverer(object):
    """
    Retrieves and caches a prioritized list of hosts from SRV records.

    SRV records are cached according to their TTL. Priority is respected, but
    weighting is not currently implemented. An instance of this class has a
    hosts() method that returns a list of (target, port) two-tuples. See RFC
    2782 for details.

    """
    def __init__(self, service, protocol, domain):
        """
        :param str service: The service name (usually IANA-assigned).
        :param str protocol: The protocol (usually 'tcp' or 'udp').
        :param str domain: The domain name.
        """
        self.service = service.lower()
        self.protocol = protocol.lower()
        self.domain = domain.lower()

        self._hosts = []
        self._expires = datetime.utcnow() - timedelta(seconds=1)

    def hosts(self):
        """ Returns a list of (target, port) two-tuples for our resource. """
        if self._is_expired():
            self._load_hosts()

        return self._hosts

    def _is_expired(self):
        return (datetime.utcnow() >= self._expires)

    def _load_hosts(self):
        resolver = dns.resolver.Resolver()
        name = '_{self.service}._{self.protocol}.{self.domain}'.format(
            self=self)

        results = resolver.query(name, 'SRV')

        servers = defaultdict(list)
        for srv in results:
            priority = int(srv.priority)
            target = srv.target.to_text().strip('.')
            port = srv.port

            servers[priority].append((target, port))

        # TODO: support weighting?
        for server_list in servers.itervalues():
            random.shuffle(server_list)

        self._hosts = [host for priority in sorted(servers.iterkeys())
                       for host in servers[priority]]
        self._expires = datetime.utcfromtimestamp(results.expiration)


discoverer = None
def ldap_auto_discover(domain):
    """
    Returns a space-separated list of LDAP servers for this domain.

    This uses SRV records to discover local LDAP servers and returns them in
    a prioritized, space-separated list for python-ldap's initialize function.
    """
    global discoverer
    if discoverer is None:
        discoverer = ServerDiscoverer("ldap", "tcp", domain)
    hosts = discoverer.hosts()

    return ' '.join('ldap://{}:{}'.format(target, port)
                    for target, port in hosts)


if __name__ == "__main__":
    print ldap_auto_discover(sys.argv[1])
