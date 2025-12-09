# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**approve_quiz_quizzes_quiz_id_approve_post**](DefaultApi.md#approve_quiz_quizzes_quiz_id_approve_post) | **POST** /quizzes/{quiz_id}/approve | Approve Quiz
[**create_quiz_quizzes_post**](DefaultApi.md#create_quiz_quizzes_post) | **POST** /quizzes/ | Create Quiz
[**delete_quiz_quizzes_quiz_id_delete**](DefaultApi.md#delete_quiz_quizzes_quiz_id_delete) | **DELETE** /quizzes/{quiz_id} | Delete Quiz
[**get_quiz_quizzes_quiz_id_get**](DefaultApi.md#get_quiz_quizzes_quiz_id_get) | **GET** /quizzes/{quiz_id} | Get Quiz
[**health_check_health_check_get**](DefaultApi.md#health_check_health_check_get) | **GET** /__health-check__ | Health Check
[**list_quizzes_quizzes_get**](DefaultApi.md#list_quizzes_quizzes_get) | **GET** /quizzes/ | List Quizzes
[**read_root_get**](DefaultApi.md#read_root_get) | **GET** / | Read Root


# **approve_quiz_quizzes_quiz_id_approve_post**
> object approve_quiz_quizzes_quiz_id_approve_post(quiz_id, approve_request)

Approve Quiz

Transition: Draft -> Approved. Triggers email and updates DB.

### Example


```python
import openapi_client
from openapi_client.models.approve_request import ApproveRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    quiz_id = 'quiz_id_example' # str | 
    approve_request = openapi_client.ApproveRequest() # ApproveRequest | 

    try:
        # Approve Quiz
        api_response = api_instance.approve_quiz_quizzes_quiz_id_approve_post(quiz_id, approve_request)
        print("The response of DefaultApi->approve_quiz_quizzes_quiz_id_approve_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->approve_quiz_quizzes_quiz_id_approve_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **quiz_id** | **str**|  | 
 **approve_request** | [**ApproveRequest**](ApproveRequest.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_quiz_quizzes_post**
> QuizDB create_quiz_quizzes_post(quiz_create_request)

Create Quiz

Takes questions, creates a Google Form, saves to MongoDB as DRAFT.

### Example


```python
import openapi_client
from openapi_client.models.quiz_create_request import QuizCreateRequest
from openapi_client.models.quiz_db import QuizDB
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    quiz_create_request = openapi_client.QuizCreateRequest() # QuizCreateRequest | 

    try:
        # Create Quiz
        api_response = api_instance.create_quiz_quizzes_post(quiz_create_request)
        print("The response of DefaultApi->create_quiz_quizzes_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_quiz_quizzes_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **quiz_create_request** | [**QuizCreateRequest**](QuizCreateRequest.md)|  | 

### Return type

[**QuizDB**](QuizDB.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_quiz_quizzes_quiz_id_delete**
> delete_quiz_quizzes_quiz_id_delete(quiz_id)

Delete Quiz

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    quiz_id = 'quiz_id_example' # str | 

    try:
        # Delete Quiz
        api_instance.delete_quiz_quizzes_quiz_id_delete(quiz_id)
    except Exception as e:
        print("Exception when calling DefaultApi->delete_quiz_quizzes_quiz_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **quiz_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_quiz_quizzes_quiz_id_get**
> QuizDB get_quiz_quizzes_quiz_id_get(quiz_id)

Get Quiz

Get details for a specific quiz.

### Example


```python
import openapi_client
from openapi_client.models.quiz_db import QuizDB
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    quiz_id = 'quiz_id_example' # str | 

    try:
        # Get Quiz
        api_response = api_instance.get_quiz_quizzes_quiz_id_get(quiz_id)
        print("The response of DefaultApi->get_quiz_quizzes_quiz_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_quiz_quizzes_quiz_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **quiz_id** | **str**|  | 

### Return type

[**QuizDB**](QuizDB.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **health_check_health_check_get**
> object health_check_health_check_get()

Health Check

Endpoint to verify API and service account functionality.

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # Health Check
        api_response = api_instance.health_check_health_check_get()
        print("The response of DefaultApi->health_check_health_check_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->health_check_health_check_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_quizzes_quizzes_get**
> List[QuizDB] list_quizzes_quizzes_get()

List Quizzes

### Example


```python
import openapi_client
from openapi_client.models.quiz_db import QuizDB
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # List Quizzes
        api_response = api_instance.list_quizzes_quizzes_get()
        print("The response of DefaultApi->list_quizzes_quizzes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_quizzes_quizzes_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[QuizDB]**](QuizDB.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_root_get**
> object read_root_get()

Read Root

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # Read Root
        api_response = api_instance.read_root_get()
        print("The response of DefaultApi->read_root_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->read_root_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

