# coding: utf-8

"""
    LaunchDarkly REST API

    Build custom integrations with the LaunchDarkly REST API  # noqa: E501

    OpenAPI spec version: 5.3.0
    Contact: support@launchdarkly.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from launchdarkly_api.api_client import ApiClient


class EnvironmentsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete_environment(self, project_key, environment_key, **kwargs):  # noqa: E501
        """Delete an environment in a specific project.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_environment(project_key, environment_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param str environment_key: The environment key, used to tie together flag configuration and users under one environment so they can be managed together. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_environment_with_http_info(project_key, environment_key, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_environment_with_http_info(project_key, environment_key, **kwargs)  # noqa: E501
            return data

    def delete_environment_with_http_info(self, project_key, environment_key, **kwargs):  # noqa: E501
        """Delete an environment in a specific project.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_environment_with_http_info(project_key, environment_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param str environment_key: The environment key, used to tie together flag configuration and users under one environment so they can be managed together. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_key', 'environment_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_environment" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_key' is set
        if ('project_key' not in params or
                params['project_key'] is None):
            raise ValueError("Missing the required parameter `project_key` when calling `delete_environment`")  # noqa: E501
        # verify the required parameter 'environment_key' is set
        if ('environment_key' not in params or
                params['environment_key'] is None):
            raise ValueError("Missing the required parameter `environment_key` when calling `delete_environment`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_key' in params:
            path_params['projectKey'] = params['project_key']  # noqa: E501
        if 'environment_key' in params:
            path_params['environmentKey'] = params['environment_key']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Token']  # noqa: E501

        return self.api_client.call_api(
            '/projects/{projectKey}/environments/{environmentKey}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_environment(self, project_key, environment_key, **kwargs):  # noqa: E501
        """Get an environment given a project and key.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_environment(project_key, environment_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param str environment_key: The environment key, used to tie together flag configuration and users under one environment so they can be managed together. (required)
        :return: Environment
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_environment_with_http_info(project_key, environment_key, **kwargs)  # noqa: E501
        else:
            (data) = self.get_environment_with_http_info(project_key, environment_key, **kwargs)  # noqa: E501
            return data

    def get_environment_with_http_info(self, project_key, environment_key, **kwargs):  # noqa: E501
        """Get an environment given a project and key.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_environment_with_http_info(project_key, environment_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param str environment_key: The environment key, used to tie together flag configuration and users under one environment so they can be managed together. (required)
        :return: Environment
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_key', 'environment_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_environment" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_key' is set
        if ('project_key' not in params or
                params['project_key'] is None):
            raise ValueError("Missing the required parameter `project_key` when calling `get_environment`")  # noqa: E501
        # verify the required parameter 'environment_key' is set
        if ('environment_key' not in params or
                params['environment_key'] is None):
            raise ValueError("Missing the required parameter `environment_key` when calling `get_environment`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_key' in params:
            path_params['projectKey'] = params['project_key']  # noqa: E501
        if 'environment_key' in params:
            path_params['environmentKey'] = params['environment_key']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Token']  # noqa: E501

        return self.api_client.call_api(
            '/projects/{projectKey}/environments/{environmentKey}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Environment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def patch_environment(self, project_key, environment_key, patch_delta, **kwargs):  # noqa: E501
        """Modify an environment by ID. If you try to patch the environment by setting both required and requiredApprovalTags, it will result in an error. Users can specify either required approvals for all flags in an environment or those with specific tags, but not both. Only customers on an Enterprise plan can require approval for flag updates with either mechanism.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.patch_environment(project_key, environment_key, patch_delta, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param str environment_key: The environment key, used to tie together flag configuration and users under one environment so they can be managed together. (required)
        :param list[PatchOperation] patch_delta: Requires a JSON Patch representation of the desired changes to the project. 'http://jsonpatch.com/' (required)
        :return: Environment
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.patch_environment_with_http_info(project_key, environment_key, patch_delta, **kwargs)  # noqa: E501
        else:
            (data) = self.patch_environment_with_http_info(project_key, environment_key, patch_delta, **kwargs)  # noqa: E501
            return data

    def patch_environment_with_http_info(self, project_key, environment_key, patch_delta, **kwargs):  # noqa: E501
        """Modify an environment by ID. If you try to patch the environment by setting both required and requiredApprovalTags, it will result in an error. Users can specify either required approvals for all flags in an environment or those with specific tags, but not both. Only customers on an Enterprise plan can require approval for flag updates with either mechanism.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.patch_environment_with_http_info(project_key, environment_key, patch_delta, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param str environment_key: The environment key, used to tie together flag configuration and users under one environment so they can be managed together. (required)
        :param list[PatchOperation] patch_delta: Requires a JSON Patch representation of the desired changes to the project. 'http://jsonpatch.com/' (required)
        :return: Environment
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_key', 'environment_key', 'patch_delta']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method patch_environment" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_key' is set
        if ('project_key' not in params or
                params['project_key'] is None):
            raise ValueError("Missing the required parameter `project_key` when calling `patch_environment`")  # noqa: E501
        # verify the required parameter 'environment_key' is set
        if ('environment_key' not in params or
                params['environment_key'] is None):
            raise ValueError("Missing the required parameter `environment_key` when calling `patch_environment`")  # noqa: E501
        # verify the required parameter 'patch_delta' is set
        if ('patch_delta' not in params or
                params['patch_delta'] is None):
            raise ValueError("Missing the required parameter `patch_delta` when calling `patch_environment`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_key' in params:
            path_params['projectKey'] = params['project_key']  # noqa: E501
        if 'environment_key' in params:
            path_params['environmentKey'] = params['environment_key']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'patch_delta' in params:
            body_params = params['patch_delta']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Token']  # noqa: E501

        return self.api_client.call_api(
            '/projects/{projectKey}/environments/{environmentKey}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Environment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_environment(self, project_key, environment_body, **kwargs):  # noqa: E501
        """Create a new environment in a specified project with a given name, key, and swatch color.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_environment(project_key, environment_body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param EnvironmentPost environment_body: New environment. (required)
        :return: Environment
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.post_environment_with_http_info(project_key, environment_body, **kwargs)  # noqa: E501
        else:
            (data) = self.post_environment_with_http_info(project_key, environment_body, **kwargs)  # noqa: E501
            return data

    def post_environment_with_http_info(self, project_key, environment_body, **kwargs):  # noqa: E501
        """Create a new environment in a specified project with a given name, key, and swatch color.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_environment_with_http_info(project_key, environment_body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param EnvironmentPost environment_body: New environment. (required)
        :return: Environment
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_key', 'environment_body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_environment" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_key' is set
        if ('project_key' not in params or
                params['project_key'] is None):
            raise ValueError("Missing the required parameter `project_key` when calling `post_environment`")  # noqa: E501
        # verify the required parameter 'environment_body' is set
        if ('environment_body' not in params or
                params['environment_body'] is None):
            raise ValueError("Missing the required parameter `environment_body` when calling `post_environment`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_key' in params:
            path_params['projectKey'] = params['project_key']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'environment_body' in params:
            body_params = params['environment_body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Token']  # noqa: E501

        return self.api_client.call_api(
            '/projects/{projectKey}/environments', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Environment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def reset_environment_mobile_key(self, project_key, environment_key, **kwargs):  # noqa: E501
        """Reset an environment's mobile key. The optional expiry for the old key is deprecated for this endpoint, so the old key will always expire immediately.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reset_environment_mobile_key(project_key, environment_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param str environment_key: The environment key, used to tie together flag configuration and users under one environment so they can be managed together. (required)
        :param int expiry: The expiry parameter is deprecated for this endpoint, so the old mobile key will always expire immediately. This parameter will be removed in an upcoming major API client version.
        :return: Environment
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.reset_environment_mobile_key_with_http_info(project_key, environment_key, **kwargs)  # noqa: E501
        else:
            (data) = self.reset_environment_mobile_key_with_http_info(project_key, environment_key, **kwargs)  # noqa: E501
            return data

    def reset_environment_mobile_key_with_http_info(self, project_key, environment_key, **kwargs):  # noqa: E501
        """Reset an environment's mobile key. The optional expiry for the old key is deprecated for this endpoint, so the old key will always expire immediately.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reset_environment_mobile_key_with_http_info(project_key, environment_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param str environment_key: The environment key, used to tie together flag configuration and users under one environment so they can be managed together. (required)
        :param int expiry: The expiry parameter is deprecated for this endpoint, so the old mobile key will always expire immediately. This parameter will be removed in an upcoming major API client version.
        :return: Environment
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_key', 'environment_key', 'expiry']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method reset_environment_mobile_key" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_key' is set
        if ('project_key' not in params or
                params['project_key'] is None):
            raise ValueError("Missing the required parameter `project_key` when calling `reset_environment_mobile_key`")  # noqa: E501
        # verify the required parameter 'environment_key' is set
        if ('environment_key' not in params or
                params['environment_key'] is None):
            raise ValueError("Missing the required parameter `environment_key` when calling `reset_environment_mobile_key`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_key' in params:
            path_params['projectKey'] = params['project_key']  # noqa: E501
        if 'environment_key' in params:
            path_params['environmentKey'] = params['environment_key']  # noqa: E501

        query_params = []
        if 'expiry' in params:
            query_params.append(('expiry', params['expiry']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Token']  # noqa: E501

        return self.api_client.call_api(
            '/projects/{projectKey}/environments/{environmentKey}/mobileKey', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Environment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def reset_environment_sdk_key(self, project_key, environment_key, **kwargs):  # noqa: E501
        """Reset an environment's SDK key with an optional expiry time for the old key.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reset_environment_sdk_key(project_key, environment_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param str environment_key: The environment key, used to tie together flag configuration and users under one environment so they can be managed together. (required)
        :param int expiry: An expiration time for the old environment SDK key, expressed as a Unix epoch time in milliseconds. By default, the key will expire immediately.
        :return: Environment
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.reset_environment_sdk_key_with_http_info(project_key, environment_key, **kwargs)  # noqa: E501
        else:
            (data) = self.reset_environment_sdk_key_with_http_info(project_key, environment_key, **kwargs)  # noqa: E501
            return data

    def reset_environment_sdk_key_with_http_info(self, project_key, environment_key, **kwargs):  # noqa: E501
        """Reset an environment's SDK key with an optional expiry time for the old key.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reset_environment_sdk_key_with_http_info(project_key, environment_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_key: The project key, used to tie the flags together under one project so they can be managed together. (required)
        :param str environment_key: The environment key, used to tie together flag configuration and users under one environment so they can be managed together. (required)
        :param int expiry: An expiration time for the old environment SDK key, expressed as a Unix epoch time in milliseconds. By default, the key will expire immediately.
        :return: Environment
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_key', 'environment_key', 'expiry']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method reset_environment_sdk_key" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_key' is set
        if ('project_key' not in params or
                params['project_key'] is None):
            raise ValueError("Missing the required parameter `project_key` when calling `reset_environment_sdk_key`")  # noqa: E501
        # verify the required parameter 'environment_key' is set
        if ('environment_key' not in params or
                params['environment_key'] is None):
            raise ValueError("Missing the required parameter `environment_key` when calling `reset_environment_sdk_key`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_key' in params:
            path_params['projectKey'] = params['project_key']  # noqa: E501
        if 'environment_key' in params:
            path_params['environmentKey'] = params['environment_key']  # noqa: E501

        query_params = []
        if 'expiry' in params:
            query_params.append(('expiry', params['expiry']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Token']  # noqa: E501

        return self.api_client.call_api(
            '/projects/{projectKey}/environments/{environmentKey}/apiKey', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Environment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
