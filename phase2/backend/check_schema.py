from app.schemas import TodoCreate
import json

print("TodoCreate schema:")
print(TodoCreate.model_json_schema())

print("\n\nTags field info:")
tags_field = TodoCreate.model_fields.get('tags')
print(f"Tags field: {tags_field}")
print(f"Tags annotation: {tags_field.annotation if tags_field else 'N/A'}")
