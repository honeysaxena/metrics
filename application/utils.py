import json
from pydantic import BaseModel, error_wrappers


def valid_schema_data_or_error(raw_data: dict, SchemaModel: BaseModel):
    data = {}
    errors = []
    err_str = None
    try:
        cleaned_data = SchemaModel(**raw_data)
        data = cleaned_data.dict()
    except error_wrappers.ValidationError as e: 
            err_str = e.json()
    if err_str is not None:        
        try:
            errors = json.loads(err_str)
        except Exception as e:
                errors = [{"loc": "non_field_error", "msg": "Unknown error"}]
    return data, errors        