# coding: utf-8

"""
    Cythereal Dashboard API

     The API used exclusively by the MAGIC Dashboard for populating charts, graphs, tables, etc... on the dashboard.  # API Conventions  **All responses** MUST be of type `APIResponse` and contain the following fields:  * `api_version` |  The current api version * `success` | Boolean value indicating if the operation succeeded. * `code` | Status code. Typically corresponds to the HTTP status code.  * `message` | A human readable message providing more details about the operation. Can be null or empty.  **Successful operations** MUST return a `SuccessResponse`, which extends `APIResponse` by adding:  * `data` | Properties containing the response object. * `success` | MUST equal True  When returning objects from a successful response, the `data` object SHOULD contain a property named after the requested object type. For example, the `/alerts` endpoint should return a response object with `data.alerts`. This property SHOULD  contain a list of the returned objects. For the `/alerts` endpoint, the `data.alerts` property contains a list of MagicAlerts objects. See the `/alerts` endpoint documentation for an example.  **Failed Operations** MUST return an `ErrorResponse`, which extends `APIResponse` by adding:  * `success` | MUST equal False.   # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: support@cythereal.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "cythereal-dashboard"
VERSION = "0.30.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "certifi>=2017.4.17",
    "python-dateutil>=2.1",
    "six>=1.10",
    "urllib3>=1.23"
]
    

setup(
    name=NAME,
    version=VERSION,
    description="Cythereal Dashboard API",
    author_email="support@cythereal.com",
    url="",
    keywords=["Swagger", "Cythereal Dashboard API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
     The API used exclusively by the MAGIC Dashboard for populating charts, graphs, tables, etc... on the dashboard.  # API Conventions  **All responses** MUST be of type &#x60;APIResponse&#x60; and contain the following fields:  * &#x60;api_version&#x60; |  The current api version * &#x60;success&#x60; | Boolean value indicating if the operation succeeded. * &#x60;code&#x60; | Status code. Typically corresponds to the HTTP status code.  * &#x60;message&#x60; | A human readable message providing more details about the operation. Can be null or empty.  **Successful operations** MUST return a &#x60;SuccessResponse&#x60;, which extends &#x60;APIResponse&#x60; by adding:  * &#x60;data&#x60; | Properties containing the response object. * &#x60;success&#x60; | MUST equal True  When returning objects from a successful response, the &#x60;data&#x60; object SHOULD contain a property named after the requested object type. For example, the &#x60;/alerts&#x60; endpoint should return a response object with &#x60;data.alerts&#x60;. This property SHOULD  contain a list of the returned objects. For the &#x60;/alerts&#x60; endpoint, the &#x60;data.alerts&#x60; property contains a list of MagicAlerts objects. See the &#x60;/alerts&#x60; endpoint documentation for an example.  **Failed Operations** MUST return an &#x60;ErrorResponse&#x60;, which extends &#x60;APIResponse&#x60; by adding:  * &#x60;success&#x60; | MUST equal False.   # noqa: E501
    """
)
