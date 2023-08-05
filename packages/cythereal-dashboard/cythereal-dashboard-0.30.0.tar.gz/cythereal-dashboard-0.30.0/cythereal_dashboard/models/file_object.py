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


class FileObject(object):
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
        'sha1': 'Sha1',
        'sha256': 'Sha256',
        'sha512': 'Sha512',
        'md5': 'Md5',
        'object_class': 'ObjectClass',
        'unix_filetype': 'Filetype',
        'upload_date': 'Timestamp',
        'children': 'list[FileObject]',
        'filenames': 'Filenames',
        'is_public': 'IsPublic',
        'is_owned': 'IsOwned',
        'tags': 'Tags',
        'status': 'Status',
        'analysis': 'Analysis',
        'num_matches': 'int',
        'num_scans': 'int',
        'num_detections': 'int',
        'scan_date': 'Timestamp',
        'evasiveness': 'Evasiveness',
        'categories': 'Categories',
        'families': 'Families',
        'tokens': 'Tokens',
        'av_names': 'AvNames',
        'labels': 'OldCategories',
        'category': 'Category',
        'family': 'Family'
    }

    attribute_map = {
        'sha1': 'sha1',
        'sha256': 'sha256',
        'sha512': 'sha512',
        'md5': 'md5',
        'object_class': 'object_class',
        'unix_filetype': 'unix_filetype',
        'upload_date': 'upload_date',
        'children': 'children',
        'filenames': 'filenames',
        'is_public': 'is_public',
        'is_owned': 'is_owned',
        'tags': 'tags',
        'status': 'status',
        'analysis': 'analysis',
        'num_matches': 'num_matches',
        'num_scans': 'num_scans',
        'num_detections': 'num_detections',
        'scan_date': 'scan_date',
        'evasiveness': 'evasiveness',
        'categories': 'categories',
        'families': 'families',
        'tokens': 'tokens',
        'av_names': 'av_names',
        'labels': 'labels',
        'category': 'category',
        'family': 'family'
    }

    def __init__(self, sha1=None, sha256=None, sha512=None, md5=None, object_class=None, unix_filetype=None, upload_date=None, children=None, filenames=None, is_public=None, is_owned=None, tags=None, status=None, analysis=None, num_matches=None, num_scans=None, num_detections=None, scan_date=None, evasiveness=None, categories=None, families=None, tokens=None, av_names=None, labels=None, category=None, family=None):  # noqa: E501
        """FileObject - a model defined in Swagger"""  # noqa: E501

        self._sha1 = None
        self._sha256 = None
        self._sha512 = None
        self._md5 = None
        self._object_class = None
        self._unix_filetype = None
        self._upload_date = None
        self._children = None
        self._filenames = None
        self._is_public = None
        self._is_owned = None
        self._tags = None
        self._status = None
        self._analysis = None
        self._num_matches = None
        self._num_scans = None
        self._num_detections = None
        self._scan_date = None
        self._evasiveness = None
        self._categories = None
        self._families = None
        self._tokens = None
        self._av_names = None
        self._labels = None
        self._category = None
        self._family = None
        self.discriminator = None

        if sha1 is not None:
            self.sha1 = sha1
        if sha256 is not None:
            self.sha256 = sha256
        if sha512 is not None:
            self.sha512 = sha512
        if md5 is not None:
            self.md5 = md5
        if object_class is not None:
            self.object_class = object_class
        if unix_filetype is not None:
            self.unix_filetype = unix_filetype
        if upload_date is not None:
            self.upload_date = upload_date
        if children is not None:
            self.children = children
        if filenames is not None:
            self.filenames = filenames
        if is_public is not None:
            self.is_public = is_public
        if is_owned is not None:
            self.is_owned = is_owned
        if tags is not None:
            self.tags = tags
        if status is not None:
            self.status = status
        if analysis is not None:
            self.analysis = analysis
        if num_matches is not None:
            self.num_matches = num_matches
        if num_scans is not None:
            self.num_scans = num_scans
        if num_detections is not None:
            self.num_detections = num_detections
        if scan_date is not None:
            self.scan_date = scan_date
        if evasiveness is not None:
            self.evasiveness = evasiveness
        if categories is not None:
            self.categories = categories
        if families is not None:
            self.families = families
        if tokens is not None:
            self.tokens = tokens
        if av_names is not None:
            self.av_names = av_names
        if labels is not None:
            self.labels = labels
        if category is not None:
            self.category = category
        if family is not None:
            self.family = family

    @property
    def sha1(self):
        """Gets the sha1 of this FileObject.  # noqa: E501


        :return: The sha1 of this FileObject.  # noqa: E501
        :rtype: Sha1
        """
        return self._sha1

    @sha1.setter
    def sha1(self, sha1):
        """Sets the sha1 of this FileObject.


        :param sha1: The sha1 of this FileObject.  # noqa: E501
        :type: Sha1
        """

        self._sha1 = sha1

    @property
    def sha256(self):
        """Gets the sha256 of this FileObject.  # noqa: E501


        :return: The sha256 of this FileObject.  # noqa: E501
        :rtype: Sha256
        """
        return self._sha256

    @sha256.setter
    def sha256(self, sha256):
        """Sets the sha256 of this FileObject.


        :param sha256: The sha256 of this FileObject.  # noqa: E501
        :type: Sha256
        """

        self._sha256 = sha256

    @property
    def sha512(self):
        """Gets the sha512 of this FileObject.  # noqa: E501


        :return: The sha512 of this FileObject.  # noqa: E501
        :rtype: Sha512
        """
        return self._sha512

    @sha512.setter
    def sha512(self, sha512):
        """Sets the sha512 of this FileObject.


        :param sha512: The sha512 of this FileObject.  # noqa: E501
        :type: Sha512
        """

        self._sha512 = sha512

    @property
    def md5(self):
        """Gets the md5 of this FileObject.  # noqa: E501


        :return: The md5 of this FileObject.  # noqa: E501
        :rtype: Md5
        """
        return self._md5

    @md5.setter
    def md5(self, md5):
        """Sets the md5 of this FileObject.


        :param md5: The md5 of this FileObject.  # noqa: E501
        :type: Md5
        """

        self._md5 = md5

    @property
    def object_class(self):
        """Gets the object_class of this FileObject.  # noqa: E501


        :return: The object_class of this FileObject.  # noqa: E501
        :rtype: ObjectClass
        """
        return self._object_class

    @object_class.setter
    def object_class(self, object_class):
        """Sets the object_class of this FileObject.


        :param object_class: The object_class of this FileObject.  # noqa: E501
        :type: ObjectClass
        """

        self._object_class = object_class

    @property
    def unix_filetype(self):
        """Gets the unix_filetype of this FileObject.  # noqa: E501


        :return: The unix_filetype of this FileObject.  # noqa: E501
        :rtype: Filetype
        """
        return self._unix_filetype

    @unix_filetype.setter
    def unix_filetype(self, unix_filetype):
        """Sets the unix_filetype of this FileObject.


        :param unix_filetype: The unix_filetype of this FileObject.  # noqa: E501
        :type: Filetype
        """

        self._unix_filetype = unix_filetype

    @property
    def upload_date(self):
        """Gets the upload_date of this FileObject.  # noqa: E501


        :return: The upload_date of this FileObject.  # noqa: E501
        :rtype: Timestamp
        """
        return self._upload_date

    @upload_date.setter
    def upload_date(self, upload_date):
        """Sets the upload_date of this FileObject.


        :param upload_date: The upload_date of this FileObject.  # noqa: E501
        :type: Timestamp
        """

        self._upload_date = upload_date

    @property
    def children(self):
        """Gets the children of this FileObject.  # noqa: E501


        :return: The children of this FileObject.  # noqa: E501
        :rtype: list[FileObject]
        """
        return self._children

    @children.setter
    def children(self, children):
        """Sets the children of this FileObject.


        :param children: The children of this FileObject.  # noqa: E501
        :type: list[FileObject]
        """

        self._children = children

    @property
    def filenames(self):
        """Gets the filenames of this FileObject.  # noqa: E501


        :return: The filenames of this FileObject.  # noqa: E501
        :rtype: Filenames
        """
        return self._filenames

    @filenames.setter
    def filenames(self, filenames):
        """Sets the filenames of this FileObject.


        :param filenames: The filenames of this FileObject.  # noqa: E501
        :type: Filenames
        """

        self._filenames = filenames

    @property
    def is_public(self):
        """Gets the is_public of this FileObject.  # noqa: E501


        :return: The is_public of this FileObject.  # noqa: E501
        :rtype: IsPublic
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this FileObject.


        :param is_public: The is_public of this FileObject.  # noqa: E501
        :type: IsPublic
        """

        self._is_public = is_public

    @property
    def is_owned(self):
        """Gets the is_owned of this FileObject.  # noqa: E501


        :return: The is_owned of this FileObject.  # noqa: E501
        :rtype: IsOwned
        """
        return self._is_owned

    @is_owned.setter
    def is_owned(self, is_owned):
        """Sets the is_owned of this FileObject.


        :param is_owned: The is_owned of this FileObject.  # noqa: E501
        :type: IsOwned
        """

        self._is_owned = is_owned

    @property
    def tags(self):
        """Gets the tags of this FileObject.  # noqa: E501


        :return: The tags of this FileObject.  # noqa: E501
        :rtype: Tags
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this FileObject.


        :param tags: The tags of this FileObject.  # noqa: E501
        :type: Tags
        """

        self._tags = tags

    @property
    def status(self):
        """Gets the status of this FileObject.  # noqa: E501


        :return: The status of this FileObject.  # noqa: E501
        :rtype: Status
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this FileObject.


        :param status: The status of this FileObject.  # noqa: E501
        :type: Status
        """

        self._status = status

    @property
    def analysis(self):
        """Gets the analysis of this FileObject.  # noqa: E501


        :return: The analysis of this FileObject.  # noqa: E501
        :rtype: Analysis
        """
        return self._analysis

    @analysis.setter
    def analysis(self, analysis):
        """Sets the analysis of this FileObject.


        :param analysis: The analysis of this FileObject.  # noqa: E501
        :type: Analysis
        """

        self._analysis = analysis

    @property
    def num_matches(self):
        """Gets the num_matches of this FileObject.  # noqa: E501

        The number of similar files to this one.  # noqa: E501

        :return: The num_matches of this FileObject.  # noqa: E501
        :rtype: int
        """
        return self._num_matches

    @num_matches.setter
    def num_matches(self, num_matches):
        """Sets the num_matches of this FileObject.

        The number of similar files to this one.  # noqa: E501

        :param num_matches: The num_matches of this FileObject.  # noqa: E501
        :type: int
        """

        self._num_matches = num_matches

    @property
    def num_scans(self):
        """Gets the num_scans of this FileObject.  # noqa: E501

        The number of virus vendors that scanned this file similar payload  # noqa: E501

        :return: The num_scans of this FileObject.  # noqa: E501
        :rtype: int
        """
        return self._num_scans

    @num_scans.setter
    def num_scans(self, num_scans):
        """Sets the num_scans of this FileObject.

        The number of virus vendors that scanned this file similar payload  # noqa: E501

        :param num_scans: The num_scans of this FileObject.  # noqa: E501
        :type: int
        """

        self._num_scans = num_scans

    @property
    def num_detections(self):
        """Gets the num_detections of this FileObject.  # noqa: E501

        The number of virus vendors that detected this file as malicious  # noqa: E501

        :return: The num_detections of this FileObject.  # noqa: E501
        :rtype: int
        """
        return self._num_detections

    @num_detections.setter
    def num_detections(self, num_detections):
        """Sets the num_detections of this FileObject.

        The number of virus vendors that detected this file as malicious  # noqa: E501

        :param num_detections: The num_detections of this FileObject.  # noqa: E501
        :type: int
        """

        self._num_detections = num_detections

    @property
    def scan_date(self):
        """Gets the scan_date of this FileObject.  # noqa: E501


        :return: The scan_date of this FileObject.  # noqa: E501
        :rtype: Timestamp
        """
        return self._scan_date

    @scan_date.setter
    def scan_date(self, scan_date):
        """Sets the scan_date of this FileObject.


        :param scan_date: The scan_date of this FileObject.  # noqa: E501
        :type: Timestamp
        """

        self._scan_date = scan_date

    @property
    def evasiveness(self):
        """Gets the evasiveness of this FileObject.  # noqa: E501


        :return: The evasiveness of this FileObject.  # noqa: E501
        :rtype: Evasiveness
        """
        return self._evasiveness

    @evasiveness.setter
    def evasiveness(self, evasiveness):
        """Sets the evasiveness of this FileObject.


        :param evasiveness: The evasiveness of this FileObject.  # noqa: E501
        :type: Evasiveness
        """

        self._evasiveness = evasiveness

    @property
    def categories(self):
        """Gets the categories of this FileObject.  # noqa: E501


        :return: The categories of this FileObject.  # noqa: E501
        :rtype: Categories
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this FileObject.


        :param categories: The categories of this FileObject.  # noqa: E501
        :type: Categories
        """

        self._categories = categories

    @property
    def families(self):
        """Gets the families of this FileObject.  # noqa: E501


        :return: The families of this FileObject.  # noqa: E501
        :rtype: Families
        """
        return self._families

    @families.setter
    def families(self, families):
        """Sets the families of this FileObject.


        :param families: The families of this FileObject.  # noqa: E501
        :type: Families
        """

        self._families = families

    @property
    def tokens(self):
        """Gets the tokens of this FileObject.  # noqa: E501


        :return: The tokens of this FileObject.  # noqa: E501
        :rtype: Tokens
        """
        return self._tokens

    @tokens.setter
    def tokens(self, tokens):
        """Sets the tokens of this FileObject.


        :param tokens: The tokens of this FileObject.  # noqa: E501
        :type: Tokens
        """

        self._tokens = tokens

    @property
    def av_names(self):
        """Gets the av_names of this FileObject.  # noqa: E501


        :return: The av_names of this FileObject.  # noqa: E501
        :rtype: AvNames
        """
        return self._av_names

    @av_names.setter
    def av_names(self, av_names):
        """Sets the av_names of this FileObject.


        :param av_names: The av_names of this FileObject.  # noqa: E501
        :type: AvNames
        """

        self._av_names = av_names

    @property
    def labels(self):
        """Gets the labels of this FileObject.  # noqa: E501


        :return: The labels of this FileObject.  # noqa: E501
        :rtype: OldCategories
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this FileObject.


        :param labels: The labels of this FileObject.  # noqa: E501
        :type: OldCategories
        """

        self._labels = labels

    @property
    def category(self):
        """Gets the category of this FileObject.  # noqa: E501


        :return: The category of this FileObject.  # noqa: E501
        :rtype: Category
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this FileObject.


        :param category: The category of this FileObject.  # noqa: E501
        :type: Category
        """

        self._category = category

    @property
    def family(self):
        """Gets the family of this FileObject.  # noqa: E501


        :return: The family of this FileObject.  # noqa: E501
        :rtype: Family
        """
        return self._family

    @family.setter
    def family(self, family):
        """Sets the family of this FileObject.


        :param family: The family of this FileObject.  # noqa: E501
        :type: Family
        """

        self._family = family

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
        if issubclass(FileObject, dict):
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
        if not isinstance(other, FileObject):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
