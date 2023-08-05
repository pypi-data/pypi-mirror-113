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


class InfoIdsResponseData(object):
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
        'binary_ids': 'list[str]',
        'campaign_ids': 'list[str]'
    }

    attribute_map = {
        'binary_ids': 'binary_ids',
        'campaign_ids': 'campaign_ids'
    }

    def __init__(self, binary_ids=None, campaign_ids=None):  # noqa: E501
        """InfoIdsResponseData - a model defined in Swagger"""  # noqa: E501

        self._binary_ids = None
        self._campaign_ids = None
        self.discriminator = None

        if binary_ids is not None:
            self.binary_ids = binary_ids
        if campaign_ids is not None:
            self.campaign_ids = campaign_ids

    @property
    def binary_ids(self):
        """Gets the binary_ids of this InfoIdsResponseData.  # noqa: E501


        :return: The binary_ids of this InfoIdsResponseData.  # noqa: E501
        :rtype: list[str]
        """
        return self._binary_ids

    @binary_ids.setter
    def binary_ids(self, binary_ids):
        """Sets the binary_ids of this InfoIdsResponseData.


        :param binary_ids: The binary_ids of this InfoIdsResponseData.  # noqa: E501
        :type: list[str]
        """

        self._binary_ids = binary_ids

    @property
    def campaign_ids(self):
        """Gets the campaign_ids of this InfoIdsResponseData.  # noqa: E501


        :return: The campaign_ids of this InfoIdsResponseData.  # noqa: E501
        :rtype: list[str]
        """
        return self._campaign_ids

    @campaign_ids.setter
    def campaign_ids(self, campaign_ids):
        """Sets the campaign_ids of this InfoIdsResponseData.


        :param campaign_ids: The campaign_ids of this InfoIdsResponseData.  # noqa: E501
        :type: list[str]
        """

        self._campaign_ids = campaign_ids

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
        if issubclass(InfoIdsResponseData, dict):
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
        if not isinstance(other, InfoIdsResponseData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
