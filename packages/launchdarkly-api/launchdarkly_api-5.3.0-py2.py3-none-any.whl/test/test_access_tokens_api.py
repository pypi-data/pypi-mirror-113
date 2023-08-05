# coding: utf-8

"""
    LaunchDarkly REST API

    Build custom integrations with the LaunchDarkly REST API  # noqa: E501

    OpenAPI spec version: 5.3.0
    Contact: support@launchdarkly.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import launchdarkly_api
from launchdarkly_api.api.access_tokens_api import AccessTokensApi  # noqa: E501
from launchdarkly_api.rest import ApiException


class TestAccessTokensApi(unittest.TestCase):
    """AccessTokensApi unit test stubs"""

    def setUp(self):
        self.api = launchdarkly_api.api.access_tokens_api.AccessTokensApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_token(self):
        """Test case for delete_token

        Delete an access token by ID.  # noqa: E501
        """
        pass

    def test_get_token(self):
        """Test case for get_token

        Get a single access token by ID.  # noqa: E501
        """
        pass

    def test_get_tokens(self):
        """Test case for get_tokens

        Returns a list of tokens in the account.  # noqa: E501
        """
        pass

    def test_patch_token(self):
        """Test case for patch_token

        Modify an access token by ID.  # noqa: E501
        """
        pass

    def test_post_token(self):
        """Test case for post_token

        Create a new token.  # noqa: E501
        """
        pass

    def test_reset_token(self):
        """Test case for reset_token

        Reset an access token's secret key with an optional expiry time for the old key.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
