from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic.fields import FieldInfo
from typing import Type

def generate_validation_schema(model: Type[Document]):
    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [],
            "properties": {}
        }
    }

    # Add required fields
    required_fields = {field for field, info in model.model_fields.items() if info.is_required}
    schema["$jsonSchema"]["required"].extend(required_fields)

    # Process each model field
    for field_name, field_info in model.model_fields.items():
        field_properties = {}

        # Get BSON type
        bson_type = get_bson_type(field_info)
        field_properties["bsonType"] = bson_type
        field_properties["description"] = (
            f"must be a {bson_type} and is required" if field_info.is_required 
            else f"must be a {bson_type}"
        )

        # Handle string length validation
        if hasattr(field_info, "min_length") and field_info.min_length is not None:
            field_properties["minLength"] = field_info.min_length
        if hasattr(field_info, "max_length") and field_info.max_length is not None:
            field_properties["maxLength"] = field_info.max_length

        # Handle enum validation
        if field_info.annotation and hasattr(field_info.annotation, "__members__"):
            field_properties["enum"] = [e.value for e in field_info.annotation.__members__.values()]

        schema["$jsonSchema"]["properties"][field_name] = field_properties

    return schema

def get_bson_type(field_info: FieldInfo):
    field_type = field_info.annotation

    if field_type == str:
        return "string"
    elif field_type == int:
        return "int"
    elif field_type == float:
        return "double"
    elif field_type == bool:
        return "bool"
    elif field_type == PydanticObjectId or field_type == ObjectId:
        return "objectId"
    elif field_type == list:
        return "array"
    elif isinstance(field_type, type) and issubclass(field_type, Document):  # For linked documents
        return "object"
    return "object"
