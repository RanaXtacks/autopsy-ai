from .base_parser import BaseParser
from ..validators.schema_validator import ChromeSchema, validate_schema

class ChromeParser(BaseParser):
    def clean(self):
        if self.df is None:
            return
            
        # Drop rows missing essential fields
        self.df.dropna(subset=['URL', 'Visit Time'], inplace=True)
        # Drop strict duplicates
        self.df.drop_duplicates(inplace=True)
        
    def parse(self) -> list:
        if self.df is None or self.df.empty:
            return []
            
        # Convert to list of dicts
        raw_data = self.df.to_dict('records')
        
        # Validate schema
        schema = ChromeSchema()
        valid_data = validate_schema(raw_data, schema)
        
        return valid_data
