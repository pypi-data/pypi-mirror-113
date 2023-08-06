"""
A helper for interacting with the Leaseweb Domains API (v2).

This client supports the minimal subset of it needed to complete dns-01
challenges.

See https://developer.leaseweb.com/api-docs/domains_v2.html for the full API.
"""

from typing import List
from certbot_dns_leaseweb.utils import to_fqdn


import requests



LEASEWEB_DOMAIN_API_ENDPOINT="https://api.leaseweb.com/hosting/v2/domains"
# https://developer.leaseweb.com/api-docs/domains_v2.html#operation/post/domains/{domainName}/resourceRecordSets
LEASEWEB_VALID_TTLS=[
    60, 300, 1800, 3600, 14400, 28800, 43200, 86400
]


class LeasewebException(Exception):
    """ Base exception for LeasewebClient.
    """


class NotAuthorisedException(LeasewebException):
    """ Authorisation exception, indicating a 401 or 403 status code.
    """

    def __init__(
        self,
        *args
    ):
        super().__init__(
            "Missing or invalid API token",
            *args
        )


class RecordNotFoundException(LeasewebException):
    """ Domain or domain record missing exception, indicating a 404 status code.
    """

    def __init__(
        self,
        domain,
        name,
        *args
    ):
        super().__init__(
            f"No such record for domain {domain}: {name}",
            *args
        )


class ValidationFailureException(LeasewebException):
    """ Validation exception, indicating a 400 status code.

    This is typically the result of invalid/unsuitable record content data.
    """

    def __init__(
        self,
        *args
    ):
        super().__init__(
            "Invalid record.",
            *args
        )

class InvalidTTLException(LeasewebException):
    """ Exception indicating that the requested TTL is not permitted.

    Leasweb's API allows a small number of predefined TTL values, this exception
    indicates the requested TTL is not one of the allowed values.
    """

    def __init__(
        self,
        *args
    ):
        super().__init__(
            f"Valid TTL values are {','.join(LEASEWEB_VALID_TTLS)}",
            *args
        )


class LeasewebClient:
    """ A helper dealing with the parts of the Leaseweb Domains API needed to
    complete dns-01 challenges.
    """


    def __init__(
        self,
        token: str
    ):
        """
        Initialise client by providing a valid API token.

        :param token:   Leaseweb API token, can be generated from
                        https://secure.leaseweb.com/api-client-management/.
        """

        self.token = token
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self._api_endpoint = LEASEWEB_DOMAIN_API_ENDPOINT


    @property
    def headers(
        self
    ):
        """ Return headers added to all/each API request sent by this client.
        """
        return {
            "Content-Type": "application/json",
            "X-LSW-Auth": self.token,
        }


    def delete_record(
        self,
        domain_name: str,
        name: str,
        record_type: str = "TXT"
    ):
        """ Delete a DNS record given its domain, name, and type.

        :param domain_name: The name of the domain to delete the record from.
        :param name: The name of the record to delete.
        :param record_type: The type of record (TXT,A, etc) to delete. Default
                            is "TXT".

        :raises .RecordNotFoundException: The specified domain or record could
                                          not be found.
        :raises .NotAuthorisedException: API token is either invalid, or not
                                         authorised to perform the requested
                                         operation.

        """

        fqdn = to_fqdn(name)
        response = self.session.delete(
            f"{self._api_endpoint}/{domain_name}/resourceRecordSets/{fqdn}/{record_type}"
        )

        if response.status_code == 204:
            return


        if response.status_code == 404:
            raise RecordNotFoundException(domain=domain_name, name=name)

        if response.status_code in [401,403]:
            raise NotAuthorisedException()

        raise LeasewebException(response.json["error_message"])


    def add_record(
        self,
        domain_name: str,
        name: str,
        content: List[str],
        record_type: str = "TXT",
        ttl: int = 60,
    ):  # pylint: disable=too-many-arguments

        """ Create a DNS record for a domain from name, content, and type data.

        :param domain_name: The name of the domain to add the record to.
        :param name: The name of the record to add.
        :param content: A list of 1 or more strs to populate the record with.
        :param record_type: The type of record (TXT,A, etc) to add. Default
                            is "TXT".
        :param ttl: The TTL of the record in seconds. Default is 60,
                    valid values are 60, 300, 1800, 3600, 14400, 28800, 43200
                    and 86400.
        :raises .InvalidTTLException: Specified TTL is not one of the allowed
                                      values.
        :raises .ValidationFailureException: Indicates the record name or content
                                             may not be valid for its domain or
                                             type.
        :raises .NotAuthorisedException: API token is either invalid, or not
                                         authorised to perform the requested
                                         operation.
        """

        if ttl not in LEASEWEB_VALID_TTLS:
            raise InvalidTTLException()

        response = self.session.post(
            f"{self._api_endpoint}/{domain_name}/resourceRecordSets",
            json={
                "name": to_fqdn(name),
                "type": record_type,
                "ttl": ttl,
                "content": content
            }
        )

        if response.status_code == 201:
            return

        if response.status_code == 400:
            raise ValidationFailureException()

        if response.status_code in [401,403]:
            raise NotAuthorisedException()

        raise LeasewebException(response.json["error_message"])
