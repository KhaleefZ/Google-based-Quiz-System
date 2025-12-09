# QuizDB


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**title** | **str** |  | 
**status** | **str** |  | [optional] [default to 'draft']
**form_url** | **str** |  | 
**form_id** | **str** |  | 
**questions** | [**List[Question]**](Question.md) |  | 
**created_at** | **datetime** |  | [optional] 

## Example

```python
from openapi_client.models.quiz_db import QuizDB

# TODO update the JSON string below
json = "{}"
# create an instance of QuizDB from a JSON string
quiz_db_instance = QuizDB.from_json(json)
# print the JSON string representation of the object
print(QuizDB.to_json())

# convert the object into a dict
quiz_db_dict = quiz_db_instance.to_dict()
# create an instance of QuizDB from a dict
quiz_db_from_dict = QuizDB.from_dict(quiz_db_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


