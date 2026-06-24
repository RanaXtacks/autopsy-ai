from marshmallow import Schema, fields, ValidationError

class ChromeSchema(Schema):
    URL = fields.String(required=True)
    Title = fields.String(required=False, allow_none=True)
    visit_time = fields.DateTime(required=True, format="%Y-%m-%d %H:%M:%S", data_key="Visit Time")

class GitHubSchema(Schema):
    Repository = fields.String(required=True)
    Action = fields.String(required=True)
    Timestamp = fields.DateTime(required=True)

class ScreenTimeSchema(Schema):
    app_name = fields.String(required=True, data_key="App Name")
    Duration = fields.Integer(required=True) # Assuming seconds or minutes
    Date = fields.DateTime(required=True)

class SpotifySchema(Schema):
    Track = fields.String(required=True)
    Artist = fields.String(required=True)
    Timestamp = fields.DateTime(required=True)

def validate_schema(data: list, schema: Schema) -> list:
    """
    Validates a list of dictionaries against a schema.
    Returns only the valid rows, skipping the corrupted ones.
    """
    valid_data = []
    for row in data:
        try:
            validated = schema.load(row)
            valid_data.append(validated)
        except ValidationError:
            # Skip invalid rows for now. In production, we might log these.
            continue
    return valid_data
