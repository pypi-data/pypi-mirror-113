# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base.domain import Domain
from twilio.rest.proxy.v1 import V1


class Proxy(Domain):

    def __init__(self, twilio):
        """
        Initialize the Proxy Domain

        :returns: Domain for Proxy
        :rtype: twilio.rest.proxy.Proxy
        """
        super(Proxy, self).__init__(twilio)

        self.base_url = 'https://proxy.twilio.com'

        # Versions
        self._v1 = None

    @property
    def v1(self):
        """
        :returns: Version v1 of proxy
        :rtype: twilio.rest.proxy.v1.V1
        """
        if self._v1 is None:
            self._v1 = V1(self)
        return self._v1

    @property
    def services(self):
        """
        :rtype: twilio.rest.proxy.v1.service.ServiceList
        """
        return self.v1.services

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Proxy>'
