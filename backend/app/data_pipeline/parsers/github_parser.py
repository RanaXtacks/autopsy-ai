from .base_parser import BaseParser
from ..validators.schema_validator import GitHubSchema, validate_schema

class GitHubParser(BaseParser):
    def clean(self):
        if self.df is None:
            return
            
        self.df.dropna(subset=['Repository', 'Action', 'Timestamp'], inplace=True)
        self.df.drop_duplicates(inplace=True)
        
    def parse(self) -> list:
        if self.df is None or self.df.empty:
            return []
            
        raw_data = self.df.to_dict('records')
        schema = GitHubSchema()
        valid_data = validate_schema(raw_data, schema)
        
        return valid_data
