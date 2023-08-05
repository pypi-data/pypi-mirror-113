# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class DeploymentList(ListResource):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, service_sid, environment_sid):
        """
        Initialize the DeploymentList

        :param Version version: Version that contains the resource
        :param service_sid: The SID of the Service that the Deployment resource is associated with
        :param environment_sid: The SID of the Environment for the Deployment

        :returns: twilio.rest.serverless.v1.service.environment.deployment.DeploymentList
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentList
        """
        super(DeploymentList, self).__init__(version)

        # Path Solution
        self._solution = {'service_sid': service_sid, 'environment_sid': environment_sid, }
        self._uri = '/Services/{service_sid}/Environments/{environment_sid}/Deployments'.format(**self._solution)

    def stream(self, limit=None, page_size=None):
        """
        Streams DeploymentInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.serverless.v1.service.environment.deployment.DeploymentInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(page_size=limits['page_size'], )

        return self._version.stream(page, limits['limit'])

    def list(self, limit=None, page_size=None):
        """
        Lists DeploymentInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.serverless.v1.service.environment.deployment.DeploymentInstance]
        """
        return list(self.stream(limit=limit, page_size=page_size, ))

    def page(self, page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of DeploymentInstance records from the API.
        Request is executed immediately

        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of DeploymentInstance
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentPage
        """
        data = values.of({'PageToken': page_token, 'Page': page_number, 'PageSize': page_size, })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return DeploymentPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of DeploymentInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of DeploymentInstance
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return DeploymentPage(self._version, response, self._solution)

    def create(self, build_sid=values.unset):
        """
        Create the DeploymentInstance

        :param unicode build_sid: The SID of the Build for the Deployment

        :returns: The created DeploymentInstance
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentInstance
        """
        data = values.of({'BuildSid': build_sid, })

        payload = self._version.create(method='POST', uri=self._uri, data=data, )

        return DeploymentInstance(
            self._version,
            payload,
            service_sid=self._solution['service_sid'],
            environment_sid=self._solution['environment_sid'],
        )

    def get(self, sid):
        """
        Constructs a DeploymentContext

        :param sid: The SID that identifies the Deployment resource to fetch

        :returns: twilio.rest.serverless.v1.service.environment.deployment.DeploymentContext
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentContext
        """
        return DeploymentContext(
            self._version,
            service_sid=self._solution['service_sid'],
            environment_sid=self._solution['environment_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a DeploymentContext

        :param sid: The SID that identifies the Deployment resource to fetch

        :returns: twilio.rest.serverless.v1.service.environment.deployment.DeploymentContext
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentContext
        """
        return DeploymentContext(
            self._version,
            service_sid=self._solution['service_sid'],
            environment_sid=self._solution['environment_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Serverless.V1.DeploymentList>'


class DeploymentPage(Page):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, response, solution):
        """
        Initialize the DeploymentPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param service_sid: The SID of the Service that the Deployment resource is associated with
        :param environment_sid: The SID of the Environment for the Deployment

        :returns: twilio.rest.serverless.v1.service.environment.deployment.DeploymentPage
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentPage
        """
        super(DeploymentPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of DeploymentInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.serverless.v1.service.environment.deployment.DeploymentInstance
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentInstance
        """
        return DeploymentInstance(
            self._version,
            payload,
            service_sid=self._solution['service_sid'],
            environment_sid=self._solution['environment_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Serverless.V1.DeploymentPage>'


class DeploymentContext(InstanceContext):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, service_sid, environment_sid, sid):
        """
        Initialize the DeploymentContext

        :param Version version: Version that contains the resource
        :param service_sid: The SID of the Service to fetch the Deployment resource from
        :param environment_sid: The SID of the Environment used by the Deployment to fetch
        :param sid: The SID that identifies the Deployment resource to fetch

        :returns: twilio.rest.serverless.v1.service.environment.deployment.DeploymentContext
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentContext
        """
        super(DeploymentContext, self).__init__(version)

        # Path Solution
        self._solution = {'service_sid': service_sid, 'environment_sid': environment_sid, 'sid': sid, }
        self._uri = '/Services/{service_sid}/Environments/{environment_sid}/Deployments/{sid}'.format(**self._solution)

    def fetch(self):
        """
        Fetch the DeploymentInstance

        :returns: The fetched DeploymentInstance
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return DeploymentInstance(
            self._version,
            payload,
            service_sid=self._solution['service_sid'],
            environment_sid=self._solution['environment_sid'],
            sid=self._solution['sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Serverless.V1.DeploymentContext {}>'.format(context)


class DeploymentInstance(InstanceResource):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, payload, service_sid, environment_sid, sid=None):
        """
        Initialize the DeploymentInstance

        :returns: twilio.rest.serverless.v1.service.environment.deployment.DeploymentInstance
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentInstance
        """
        super(DeploymentInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'sid': payload.get('sid'),
            'account_sid': payload.get('account_sid'),
            'service_sid': payload.get('service_sid'),
            'environment_sid': payload.get('environment_sid'),
            'build_sid': payload.get('build_sid'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'url': payload.get('url'),
        }

        # Context
        self._context = None
        self._solution = {
            'service_sid': service_sid,
            'environment_sid': environment_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: DeploymentContext for this DeploymentInstance
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentContext
        """
        if self._context is None:
            self._context = DeploymentContext(
                self._version,
                service_sid=self._solution['service_sid'],
                environment_sid=self._solution['environment_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def sid(self):
        """
        :returns: The unique string that identifies the Deployment resource
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def account_sid(self):
        """
        :returns: The SID of the Account that created the Deployment resource
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def service_sid(self):
        """
        :returns: The SID of the Service that the Deployment resource is associated with
        :rtype: unicode
        """
        return self._properties['service_sid']

    @property
    def environment_sid(self):
        """
        :returns: The SID of the Environment for the Deployment
        :rtype: unicode
        """
        return self._properties['environment_sid']

    @property
    def build_sid(self):
        """
        :returns: The SID of the Build for the deployment
        :rtype: unicode
        """
        return self._properties['build_sid']

    @property
    def date_created(self):
        """
        :returns: The ISO 8601 date and time in GMT when the Deployment resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The ISO 8601 date and time in GMT when the Deployment resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def url(self):
        """
        :returns: The absolute URL of the Deployment resource
        :rtype: unicode
        """
        return self._properties['url']

    def fetch(self):
        """
        Fetch the DeploymentInstance

        :returns: The fetched DeploymentInstance
        :rtype: twilio.rest.serverless.v1.service.environment.deployment.DeploymentInstance
        """
        return self._proxy.fetch()

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Serverless.V1.DeploymentInstance {}>'.format(context)
