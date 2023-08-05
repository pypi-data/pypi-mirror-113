# coding: utf-8

"""
    Cythereal Dashboard API

     The API used exclusively by the MAGIC Dashboard for populating charts, graphs, tables, etc... on the dashboard.  # API Conventions  **All responses** MUST be of type `APIResponse` and contain the following fields:  * `api_version` |  The current api version * `success` | Boolean value indicating if the operation succeeded. * `code` | Status code. Typically corresponds to the HTTP status code.  * `message` | A human readable message providing more details about the operation. Can be null or empty.  **Successful operations** MUST return a `SuccessResponse`, which extends `APIResponse` by adding:  * `data` | Properties containing the response object. * `success` | MUST equal True  When returning objects from a successful response, the `data` object SHOULD contain a property named after the requested object type. For example, the `/alerts` endpoint should return a response object with `data.alerts`. This property SHOULD  contain a list of the returned objects. For the `/alerts` endpoint, the `data.alerts` property contains a list of MagicAlerts objects. See the `/alerts` endpoint documentation for an example.  **Failed Operations** MUST return an `ErrorResponse`, which extends `APIResponse` by adding:  * `success` | MUST equal False.   # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: support@cythereal.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ProcedureReportResponseData(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'hard_hash': 'str',
        'is_library': 'bool',
        'status': 'str',
        'limit': 'int',
        'page': 'int',
        'warnings': 'str',
        'binaries': 'ProcedureInfoList'
    }

    attribute_map = {
        'hard_hash': 'hard_hash',
        'is_library': 'is_library',
        'status': 'status',
        'limit': 'limit',
        'page': 'page',
        'warnings': 'warnings',
        'binaries': 'binaries'
    }

    def __init__(self, hard_hash=None, is_library=None, status=None, limit=None, page=None, warnings=None, binaries=None):  # noqa: E501
        """ProcedureReportResponseData - a model defined in Swagger"""  # noqa: E501

        self._hard_hash = None
        self._is_library = None
        self._status = None
        self._limit = None
        self._page = None
        self._warnings = None
        self._binaries = None
        self.discriminator = None

        if hard_hash is not None:
            self.hard_hash = hard_hash
        if is_library is not None:
            self.is_library = is_library
        if status is not None:
            self.status = status
        if limit is not None:
            self.limit = limit
        if page is not None:
            self.page = page
        if warnings is not None:
            self.warnings = warnings
        if binaries is not None:
            self.binaries = binaries

    @property
    def hard_hash(self):
        """Gets the hard_hash of this ProcedureReportResponseData.  # noqa: E501


        :return: The hard_hash of this ProcedureReportResponseData.  # noqa: E501
        :rtype: str
        """
        return self._hard_hash

    @hard_hash.setter
    def hard_hash(self, hard_hash):
        """Sets the hard_hash of this ProcedureReportResponseData.


        :param hard_hash: The hard_hash of this ProcedureReportResponseData.  # noqa: E501
        :type: str
        """

        self._hard_hash = hard_hash

    @property
    def is_library(self):
        """Gets the is_library of this ProcedureReportResponseData.  # noqa: E501


        :return: The is_library of this ProcedureReportResponseData.  # noqa: E501
        :rtype: bool
        """
        return self._is_library

    @is_library.setter
    def is_library(self, is_library):
        """Sets the is_library of this ProcedureReportResponseData.


        :param is_library: The is_library of this ProcedureReportResponseData.  # noqa: E501
        :type: bool
        """

        self._is_library = is_library

    @property
    def status(self):
        """Gets the status of this ProcedureReportResponseData.  # noqa: E501


        :return: The status of this ProcedureReportResponseData.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ProcedureReportResponseData.


        :param status: The status of this ProcedureReportResponseData.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def limit(self):
        """Gets the limit of this ProcedureReportResponseData.  # noqa: E501


        :return: The limit of this ProcedureReportResponseData.  # noqa: E501
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ProcedureReportResponseData.


        :param limit: The limit of this ProcedureReportResponseData.  # noqa: E501
        :type: int
        """

        self._limit = limit

    @property
    def page(self):
        """Gets the page of this ProcedureReportResponseData.  # noqa: E501


        :return: The page of this ProcedureReportResponseData.  # noqa: E501
        :rtype: int
        """
        return self._page

    @page.setter
    def page(self, page):
        """Sets the page of this ProcedureReportResponseData.


        :param page: The page of this ProcedureReportResponseData.  # noqa: E501
        :type: int
        """

        self._page = page

    @property
    def warnings(self):
        """Gets the warnings of this ProcedureReportResponseData.  # noqa: E501


        :return: The warnings of this ProcedureReportResponseData.  # noqa: E501
        :rtype: str
        """
        return self._warnings

    @warnings.setter
    def warnings(self, warnings):
        """Sets the warnings of this ProcedureReportResponseData.


        :param warnings: The warnings of this ProcedureReportResponseData.  # noqa: E501
        :type: str
        """

        self._warnings = warnings

    @property
    def binaries(self):
        """Gets the binaries of this ProcedureReportResponseData.  # noqa: E501


        :return: The binaries of this ProcedureReportResponseData.  # noqa: E501
        :rtype: ProcedureInfoList
        """
        return self._binaries

    @binaries.setter
    def binaries(self, binaries):
        """Sets the binaries of this ProcedureReportResponseData.


        :param binaries: The binaries of this ProcedureReportResponseData.  # noqa: E501
        :type: ProcedureInfoList
        """

        self._binaries = binaries

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ProcedureReportResponseData, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ProcedureReportResponseData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
