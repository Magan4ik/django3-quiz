from django.db import models
import json

class ListField(models.Field):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return []

        if isinstance(value, str):
            return json.loads(value)

        return value

    def get_prep_value(self, value):
        if value is None:
            return None

        if not isinstance(value, list):
            if isinstance(value, str):
                value = list(value)
            else:
                raise ValueError(f"Value must be a list ({type(value)})")


        return json.dumps(value)
