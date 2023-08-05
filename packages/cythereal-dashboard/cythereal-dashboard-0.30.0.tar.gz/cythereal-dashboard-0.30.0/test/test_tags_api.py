# coding: utf-8

"""
    Cythereal Dashboard API

     The API used exclusively by the MAGIC Dashboard for populating charts, graphs, tables, etc... on the dashboard.  # API Conventions  **All responses** MUST be of type `APIResponse` and contain the following fields:  * `api_version` |  The current api version * `success` | Boolean value indicating if the operation succeeded. * `code` | Status code. Typically corresponds to the HTTP status code.  * `message` | A human readable message providing more details about the operation. Can be null or empty.  **Successful operations** MUST return a `SuccessResponse`, which extends `APIResponse` by adding:  * `data` | Properties containing the response object. * `success` | MUST equal True  When returning objects from a successful response, the `data` object SHOULD contain a property named after the requested object type. For example, the `/alerts` endpoint should return a response object with `data.alerts`. This property SHOULD  contain a list of the returned objects. For the `/alerts` endpoint, the `data.alerts` property contains a list of MagicAlerts objects. See the `/alerts` endpoint documentation for an example.  **Failed Operations** MUST return an `ErrorResponse`, which extends `APIResponse` by adding:  * `success` | MUST equal False.   # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: support@cythereal.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import cythereal_dashboard
from cythereal_dashboard.api.tags_api import TagsApi  # noqa: E501
from cythereal_dashboard.rest import ApiException


class TestTagsApi(unittest.TestCase):
    """TagsApi unit test stubs"""

    def setUp(self):
        self.api = cythereal_dashboard.api.tags_api.TagsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_tag(self):
        """Test case for add_tag

        Adds an object to the tag name  # noqa: E501
        """
        pass

    def test_create_tag(self):
        """Test case for create_tag

        Creates a new tag for the user  # noqa: E501
        """
        pass

    def test_delete_all_tags(self):
        """Test case for delete_all_tags

        Deletes all of the user's tags  # noqa: E501
        """
        pass

    def test_delete_tag(self):
        """Test case for delete_tag

        Deletes a specific tag  # noqa: E501
        """
        pass

    def test_empty_tag(self):
        """Test case for empty_tag

        Removes all objects from a tag  # noqa: E501
        """
        pass

    def test_get_tag(self):
        """Test case for get_tag

        Retrieves a specific tag for a user  # noqa: E501
        """
        pass

    def test_list_collection_tags(self):
        """Test case for list_collection_tags

        Returns all of the user's tags in a given collection  # noqa: E501
        """
        pass

    def test_list_tags(self):
        """Test case for list_tags

        Gets all the user's tags  # noqa: E501
        """
        pass

    def test_merge_tag(self):
        """Test case for merge_tag

        Merges two tag collections into a single one  # noqa: E501
        """
        pass

    def test_remove_tag(self):
        """Test case for remove_tag

        Removes an object from a tag collection  # noqa: E501
        """
        pass

    def test_rename_tag(self):
        """Test case for rename_tag

        Renames a tag and it's collection  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
