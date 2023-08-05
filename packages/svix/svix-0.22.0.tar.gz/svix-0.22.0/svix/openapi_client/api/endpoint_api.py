"""
    Svix API

    Welcome to the Svix API documentation!  Useful links: [Homepage](https://www.svix.com) | [Support email](mailto:support+docs@svix.com) | [Blog](https://www.svix.com/blog/) | [Slack Community](https://www.svix.com/slack/)  # Introduction  This is the reference documentation and schemas for the Svix API. For tutorials and other documentation please refer to [the documentation](https://docs.svix.com).  ## Main concepts  In Svix you have four important entities you will be interacting with:  - `messages`: these are the webhooks being sent. They can have contents and a few other properties. - `application`: this is where `messages` are sent to. Usually you want to create one application for each of your users. - `endpoint`: endpoints are the URLs messages will be sent to. Each application can have multiple `endpoints` and each message sent to that application will be sent to all of them (unless they are not subscribed to the sent event type). - `event-type`: event types are identifiers denoting the type of the message being sent. Event types are primarily used to decide which events are sent to which endpoint.   ## Authentication  Get your authentication token (`AUTH_TOKEN`) from the [Svix dashboard](https://dashboard.svix.com) and use it as part of the `Authorization` header as such: `Authorization: Bearer ${AUTH_TOKEN}`.  <SecurityDefinitions />   ## Code samples  The code samples assume you already have the respective libraries installed and you know how to use them. For the latest information on how to do that, please refer to [the documentation](https://docs.svix.com/).   ## Cross-Origin Resource Sharing  This API features Cross-Origin Resource Sharing (CORS) implemented in compliance with [W3C spec](https://www.w3.org/TR/cors/). And that allows cross-domain communication from the browser. All responses have a wildcard same-origin which makes them completely public and accessible to everyone, including any code on any site.   # noqa: E501

    The version of the OpenAPI document: 1.4
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from svix.openapi_client.api_client import ApiClient, Endpoint as _Endpoint
from svix.openapi_client.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from svix.openapi_client.model.endpoint_in import EndpointIn
from svix.openapi_client.model.endpoint_out import EndpointOut
from svix.openapi_client.model.endpoint_secret_out import EndpointSecretOut
from svix.openapi_client.model.endpoint_stats import EndpointStats
from svix.openapi_client.model.http_validation_error import HTTPValidationError
from svix.openapi_client.model.http_error_out import HttpErrorOut
from svix.openapi_client.model.list_response_endpoint_out import ListResponseEndpointOut


class EndpointApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __create_endpoint_api_v1_app_app_id_endpoint_post(
            self,
            app_id,
            endpoint_in,
            **kwargs
        ):
            """Create Endpoint  # noqa: E501

            Create a new endpoint for the application.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.create_endpoint_api_v1_app_app_id_endpoint_post(app_id, endpoint_in, async_req=True)
            >>> result = thread.get()

            Args:
                app_id (str):
                endpoint_in (EndpointIn):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                EndpointOut
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['app_id'] = \
                app_id
            kwargs['endpoint_in'] = \
                endpoint_in
            return self.call_with_http_info(**kwargs)

        self.create_endpoint_api_v1_app_app_id_endpoint_post = _Endpoint(
            settings={
                'response_type': (EndpointOut,),
                'auth': [
                    'HTTPBearer'
                ],
                'endpoint_path': '/api/v1/app/{app_id}/endpoint/',
                'operation_id': 'create_endpoint_api_v1_app_app_id_endpoint_post',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'app_id',
                    'endpoint_in',
                ],
                'required': [
                    'app_id',
                    'endpoint_in',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'app_id':
                        (str,),
                    'endpoint_in':
                        (EndpointIn,),
                },
                'attribute_map': {
                    'app_id': 'app_id',
                },
                'location_map': {
                    'app_id': 'path',
                    'endpoint_in': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client,
            callable=__create_endpoint_api_v1_app_app_id_endpoint_post
        )

        def __delete_endpoint_api_v1_app_app_id_endpoint_endpoint_id_delete(
            self,
            endpoint_id,
            app_id,
            **kwargs
        ):
            """Delete Endpoint  # noqa: E501

            Delete an endpoint.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.delete_endpoint_api_v1_app_app_id_endpoint_endpoint_id_delete(endpoint_id, app_id, async_req=True)
            >>> result = thread.get()

            Args:
                endpoint_id (str):
                app_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                None
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['endpoint_id'] = \
                endpoint_id
            kwargs['app_id'] = \
                app_id
            return self.call_with_http_info(**kwargs)

        self.delete_endpoint_api_v1_app_app_id_endpoint_endpoint_id_delete = _Endpoint(
            settings={
                'response_type': None,
                'auth': [
                    'HTTPBearer'
                ],
                'endpoint_path': '/api/v1/app/{app_id}/endpoint/{endpoint_id}/',
                'operation_id': 'delete_endpoint_api_v1_app_app_id_endpoint_endpoint_id_delete',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'endpoint_id',
                    'app_id',
                ],
                'required': [
                    'endpoint_id',
                    'app_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'endpoint_id':
                        (str,),
                    'app_id':
                        (str,),
                },
                'attribute_map': {
                    'endpoint_id': 'endpoint_id',
                    'app_id': 'app_id',
                },
                'location_map': {
                    'endpoint_id': 'path',
                    'app_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__delete_endpoint_api_v1_app_app_id_endpoint_endpoint_id_delete
        )

        def __get_endpoint_api_v1_app_app_id_endpoint_endpoint_id_get(
            self,
            endpoint_id,
            app_id,
            **kwargs
        ):
            """Get Endpoint  # noqa: E501

            Get an application.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_endpoint_api_v1_app_app_id_endpoint_endpoint_id_get(endpoint_id, app_id, async_req=True)
            >>> result = thread.get()

            Args:
                endpoint_id (str):
                app_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                EndpointOut
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['endpoint_id'] = \
                endpoint_id
            kwargs['app_id'] = \
                app_id
            return self.call_with_http_info(**kwargs)

        self.get_endpoint_api_v1_app_app_id_endpoint_endpoint_id_get = _Endpoint(
            settings={
                'response_type': (EndpointOut,),
                'auth': [
                    'HTTPBearer'
                ],
                'endpoint_path': '/api/v1/app/{app_id}/endpoint/{endpoint_id}/',
                'operation_id': 'get_endpoint_api_v1_app_app_id_endpoint_endpoint_id_get',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'endpoint_id',
                    'app_id',
                ],
                'required': [
                    'endpoint_id',
                    'app_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'endpoint_id':
                        (str,),
                    'app_id':
                        (str,),
                },
                'attribute_map': {
                    'endpoint_id': 'endpoint_id',
                    'app_id': 'app_id',
                },
                'location_map': {
                    'endpoint_id': 'path',
                    'app_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__get_endpoint_api_v1_app_app_id_endpoint_endpoint_id_get
        )

        def __get_endpoint_secret_api_v1_app_app_id_endpoint_endpoint_id_secret_get(
            self,
            endpoint_id,
            app_id,
            **kwargs
        ):
            """Get Endpoint Secret  # noqa: E501

            Get the endpoint's signing secret.  This is used to verify the authenticity of the webhook. For more information please refer to [the consuming webhooks docs](https://docs.svix.com/consuming-webhooks/).  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_endpoint_secret_api_v1_app_app_id_endpoint_endpoint_id_secret_get(endpoint_id, app_id, async_req=True)
            >>> result = thread.get()

            Args:
                endpoint_id (str):
                app_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                EndpointSecretOut
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['endpoint_id'] = \
                endpoint_id
            kwargs['app_id'] = \
                app_id
            return self.call_with_http_info(**kwargs)

        self.get_endpoint_secret_api_v1_app_app_id_endpoint_endpoint_id_secret_get = _Endpoint(
            settings={
                'response_type': (EndpointSecretOut,),
                'auth': [
                    'HTTPBearer'
                ],
                'endpoint_path': '/api/v1/app/{app_id}/endpoint/{endpoint_id}/secret/',
                'operation_id': 'get_endpoint_secret_api_v1_app_app_id_endpoint_endpoint_id_secret_get',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'endpoint_id',
                    'app_id',
                ],
                'required': [
                    'endpoint_id',
                    'app_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'endpoint_id':
                        (str,),
                    'app_id':
                        (str,),
                },
                'attribute_map': {
                    'endpoint_id': 'endpoint_id',
                    'app_id': 'app_id',
                },
                'location_map': {
                    'endpoint_id': 'path',
                    'app_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__get_endpoint_secret_api_v1_app_app_id_endpoint_endpoint_id_secret_get
        )

        def __get_endpoint_stats_api_v1_app_app_id_endpoint_endpoint_id_stats_get(
            self,
            endpoint_id,
            app_id,
            **kwargs
        ):
            """Get Endpoint Stats  # noqa: E501

            Get basic statistics for the endpoint.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_endpoint_stats_api_v1_app_app_id_endpoint_endpoint_id_stats_get(endpoint_id, app_id, async_req=True)
            >>> result = thread.get()

            Args:
                endpoint_id (str):
                app_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                EndpointStats
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['endpoint_id'] = \
                endpoint_id
            kwargs['app_id'] = \
                app_id
            return self.call_with_http_info(**kwargs)

        self.get_endpoint_stats_api_v1_app_app_id_endpoint_endpoint_id_stats_get = _Endpoint(
            settings={
                'response_type': (EndpointStats,),
                'auth': [
                    'HTTPBearer'
                ],
                'endpoint_path': '/api/v1/app/{app_id}/endpoint/{endpoint_id}/stats/',
                'operation_id': 'get_endpoint_stats_api_v1_app_app_id_endpoint_endpoint_id_stats_get',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'endpoint_id',
                    'app_id',
                ],
                'required': [
                    'endpoint_id',
                    'app_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'endpoint_id':
                        (str,),
                    'app_id':
                        (str,),
                },
                'attribute_map': {
                    'endpoint_id': 'endpoint_id',
                    'app_id': 'app_id',
                },
                'location_map': {
                    'endpoint_id': 'path',
                    'app_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__get_endpoint_stats_api_v1_app_app_id_endpoint_endpoint_id_stats_get
        )

        def __list_endpoints_api_v1_app_app_id_endpoint_get(
            self,
            app_id,
            **kwargs
        ):
            """List Endpoints  # noqa: E501

            List the application's endpoints.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.list_endpoints_api_v1_app_app_id_endpoint_get(app_id, async_req=True)
            >>> result = thread.get()

            Args:
                app_id (str):

            Keyword Args:
                iterator (str): [optional]
                limit (int): [optional] if omitted the server will use the default value of 50
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                ListResponseEndpointOut
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['app_id'] = \
                app_id
            return self.call_with_http_info(**kwargs)

        self.list_endpoints_api_v1_app_app_id_endpoint_get = _Endpoint(
            settings={
                'response_type': (ListResponseEndpointOut,),
                'auth': [
                    'HTTPBearer'
                ],
                'endpoint_path': '/api/v1/app/{app_id}/endpoint/',
                'operation_id': 'list_endpoints_api_v1_app_app_id_endpoint_get',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'app_id',
                    'iterator',
                    'limit',
                ],
                'required': [
                    'app_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'app_id':
                        (str,),
                    'iterator':
                        (str,),
                    'limit':
                        (int,),
                },
                'attribute_map': {
                    'app_id': 'app_id',
                    'iterator': 'iterator',
                    'limit': 'limit',
                },
                'location_map': {
                    'app_id': 'path',
                    'iterator': 'query',
                    'limit': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__list_endpoints_api_v1_app_app_id_endpoint_get
        )

        def __update_endpoint_api_v1_app_app_id_endpoint_endpoint_id_put(
            self,
            endpoint_id,
            app_id,
            endpoint_in,
            **kwargs
        ):
            """Update Endpoint  # noqa: E501

            Update an endpoint.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.update_endpoint_api_v1_app_app_id_endpoint_endpoint_id_put(endpoint_id, app_id, endpoint_in, async_req=True)
            >>> result = thread.get()

            Args:
                endpoint_id (str):
                app_id (str):
                endpoint_in (EndpointIn):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                EndpointOut
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['endpoint_id'] = \
                endpoint_id
            kwargs['app_id'] = \
                app_id
            kwargs['endpoint_in'] = \
                endpoint_in
            return self.call_with_http_info(**kwargs)

        self.update_endpoint_api_v1_app_app_id_endpoint_endpoint_id_put = _Endpoint(
            settings={
                'response_type': (EndpointOut,),
                'auth': [
                    'HTTPBearer'
                ],
                'endpoint_path': '/api/v1/app/{app_id}/endpoint/{endpoint_id}/',
                'operation_id': 'update_endpoint_api_v1_app_app_id_endpoint_endpoint_id_put',
                'http_method': 'PUT',
                'servers': None,
            },
            params_map={
                'all': [
                    'endpoint_id',
                    'app_id',
                    'endpoint_in',
                ],
                'required': [
                    'endpoint_id',
                    'app_id',
                    'endpoint_in',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'endpoint_id':
                        (str,),
                    'app_id':
                        (str,),
                    'endpoint_in':
                        (EndpointIn,),
                },
                'attribute_map': {
                    'endpoint_id': 'endpoint_id',
                    'app_id': 'app_id',
                },
                'location_map': {
                    'endpoint_id': 'path',
                    'app_id': 'path',
                    'endpoint_in': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client,
            callable=__update_endpoint_api_v1_app_app_id_endpoint_endpoint_id_put
        )
