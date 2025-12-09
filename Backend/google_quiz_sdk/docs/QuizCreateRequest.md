# QuizCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**questions** | [**List[Question]**](Question.md) |  | 

## Example

```python
from openapi_client.models.quiz_create_request import QuizCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of QuizCreateRequest from a JSON string
quiz_create_request_instance = QuizCreateRequest.from_json(json)
# print the JSON string representation of the object
print(QuizCreateRequest.to_json())

# convert the object into a dict
quiz_create_request_dict = quiz_create_request_instance.to_dict()
# create an instance of QuizCreateRequest from a dict
quiz_create_request_from_dict = QuizCreateRequest.from_dict(quiz_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


