import pandas as pd
import io

def process_user_data(file):
    """
    Simulates processing user data using Pandas.
    In a real scenario, this would handle CSV, JSON, etc.
    """
    try:
        # Read the file into a DataFrame
        # For simulation, we assume it's a CSV
        df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
        
        # Example processing: basic statistics
        summary = {
            "row_count": len(df),
            "columns": list(df.columns),
            "head": df.head(5).to_dict(orient='records')
        }
        
        return {
            "status": "success",
            "data": summary
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
