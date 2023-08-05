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


class LabelsInner(object):
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
        'name': 'str',
        'score': 'int',
        'label_type': 'str'
    }

    attribute_map = {
        'name': 'name',
        'score': 'score',
        'label_type': 'label_type'
    }

    def __init__(self, name=None, score=None, label_type=None):  # noqa: E501
        """LabelsInner - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._score = None
        self._label_type = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if score is not None:
            self.score = score
        if label_type is not None:
            self.label_type = label_type

    @property
    def name(self):
        """Gets the name of this LabelsInner.  # noqa: E501

        The name of the label.  # noqa: E501

        :return: The name of this LabelsInner.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LabelsInner.

        The name of the label.  # noqa: E501

        :param name: The name of this LabelsInner.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def score(self):
        """Gets the score of this LabelsInner.  # noqa: E501

        The relative stregnth of the label. Higher scores mean the label is considered stronger.  # noqa: E501

        :return: The score of this LabelsInner.  # noqa: E501
        :rtype: int
        """
        return self._score

    @score.setter
    def score(self, score):
        """Sets the score of this LabelsInner.

        The relative stregnth of the label. Higher scores mean the label is considered stronger.  # noqa: E501

        :param score: The score of this LabelsInner.  # noqa: E501
        :type: int
        """

        self._score = score

    @property
    def label_type(self):
        """Gets the label_type of this LabelsInner.  # noqa: E501

        The type of the label. Will be either 'category' or 'family'. A category is the a type of malware such as \"banking\" or \"ransomware\". A family is the name of the malware family such as \"zeus\" or \"wannacry\".        # noqa: E501

        :return: The label_type of this LabelsInner.  # noqa: E501
        :rtype: str
        """
        return self._label_type

    @label_type.setter
    def label_type(self, label_type):
        """Sets the label_type of this LabelsInner.

        The type of the label. Will be either 'category' or 'family'. A category is the a type of malware such as \"banking\" or \"ransomware\". A family is the name of the malware family such as \"zeus\" or \"wannacry\".        # noqa: E501

        :param label_type: The label_type of this LabelsInner.  # noqa: E501
        :type: str
        """

        self._label_type = label_type

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
        if issubclass(LabelsInner, dict):
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
        if not isinstance(other, LabelsInner):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
