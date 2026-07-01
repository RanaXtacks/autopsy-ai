from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
import pandas as pd
import json
import io
import traceback
import sys

from ..database import get_db
from ..models_db import BehaviorSession, Habit, ProductivityScore

router = APIRouter()

def process_json_data(data, db: Session, user_id: int):
    records_added = 0
    if isinstance(data, dict):
        data = [data]
        
    for item in data:
        # Check if it's a nested "day" object
        if "date" in item or "sessions" in item or "habits" in item:
            if "date" in item:
                score = ProductivityScore(
                    user_id=user_id,
                    date=pd.to_datetime(item["date"]).date() if item.get("date") else datetime.utcnow().date(),
                    productivity_score=float(item.get("productivity_score", 0)) if item.get("productivity_score") is not None else 0.0,
                    focus_score=float(item.get("focus_score", 0)) if item.get("focus_score") is not None else 0.0,
                    consistency_score=float(item.get("consistency_score", 0)) if item.get("consistency_score") is not None else 0.0,
                    discipline_score=float(item.get("discipline_score", 0)) if item.get("discipline_score") is not None else 0.0,
                    deep_work_score=float(item.get("deep_work_score", 0)) if item.get("deep_work_score") is not None else 0.0
                )
                db.add(score)
                records_added += 1
                
            # Parse nested sessions
            for s in item.get("sessions", []):
                session_obj = BehaviorSession(
                    user_id=user_id,
                    session_type=s.get("session_type", "Unknown"),
                    start_time=pd.to_datetime(s.get("start_time", datetime.utcnow())),
                    end_time=pd.to_datetime(s.get("end_time", datetime.utcnow())),
                    duration_minutes=float(s.get("duration_minutes", 0)) if s.get("duration_minutes") is not None else 0.0,
                    event_count=int(s.get("event_count", 0)) if s.get("event_count") is not None else 0,
                    productivity_score=float(s.get("productivity_score", 0)) if s.get("productivity_score") is not None else None
                )
                db.add(session_obj)
                records_added += 1
                
            # Parse nested habits
            for h in item.get("habits", []):
                habit_obj = Habit(
                    user_id=user_id,
                    habit_name=h.get("habit_name", "Unknown"),
                    habit_type=h.get("habit_type", "Unknown"),
                    confidence_score=float(h.get("confidence_score", 0)) if h.get("confidence_score") is not None else 0.0,
                    frequency=int(h.get("frequency", 1)) if h.get("frequency") is not None else 1,
                    first_detected=pd.to_datetime(h.get("first_detected", datetime.utcnow())),
                    last_detected=pd.to_datetime(h.get("last_detected", datetime.utcnow())),
                    description=h.get("description", "")
                )
                db.add(habit_obj)
                records_added += 1

        # Or maybe it's a flat session object
        elif "session_type" in item and "start_time" in item:
            session_obj = BehaviorSession(
                user_id=user_id,
                session_type=item.get("session_type", "Unknown"),
                start_time=pd.to_datetime(item.get("start_time", datetime.utcnow())),
                end_time=pd.to_datetime(item.get("end_time", datetime.utcnow())),
                duration_minutes=float(item.get("duration_minutes", 0)) if item.get("duration_minutes") is not None else 0.0,
                event_count=int(item.get("event_count", 0)) if item.get("event_count") is not None else 0,
                productivity_score=float(item.get("productivity_score", 0)) if item.get("productivity_score") is not None else None
            )
            db.add(session_obj)
            records_added += 1
            
        elif "habit_name" in item and "habit_type" in item:
            habit_obj = Habit(
                user_id=user_id,
                habit_name=item.get("habit_name", "Unknown"),
                habit_type=item.get("habit_type", "Unknown"),
                confidence_score=float(item.get("confidence_score", 0)) if item.get("confidence_score") is not None else 0.0,
                frequency=int(item.get("frequency", 1)) if item.get("frequency") is not None else 1,
                first_detected=pd.to_datetime(item.get("first_detected", datetime.utcnow())),
                last_detected=pd.to_datetime(item.get("last_detected", datetime.utcnow())),
                description=item.get("description", "")
            )
            db.add(habit_obj)
            records_added += 1
            
    db.commit()
    return records_added


def process_and_store_csv(df: pd.DataFrame, db: Session, user_id: int):
    columns = set(df.columns)
    records_added = 0
    if "session_type" in columns and "start_time" in columns and "end_time" in columns:
        for _, row in df.iterrows():
            session = BehaviorSession(
                user_id=user_id,
                session_type=row.get("session_type", "Unknown"),
                start_time=pd.to_datetime(row["start_time"]),
                end_time=pd.to_datetime(row["end_time"]),
                duration_minutes=float(row.get("duration_minutes", 0)) if not pd.isna(row.get("duration_minutes")) else 0.0,
                event_count=int(row.get("event_count", 0)) if not pd.isna(row.get("event_count")) else 0,
                productivity_score=float(row.get("productivity_score", 0)) if not pd.isna(row.get("productivity_score")) else None
            )
            db.add(session)
            records_added += 1
            
    elif "habit_name" in columns and "habit_type" in columns:
        for _, row in df.iterrows():
            habit = Habit(
                user_id=user_id,
                habit_name=row["habit_name"],
                habit_type=row["habit_type"],
                confidence_score=float(row.get("confidence_score", 0)) if not pd.isna(row.get("confidence_score")) else 0.0,
                frequency=int(row.get("frequency", 1)) if not pd.isna(row.get("frequency")) else 1,
                first_detected=pd.to_datetime(row.get("first_detected", datetime.utcnow())),
                last_detected=pd.to_datetime(row.get("last_detected", datetime.utcnow())),
                description=row.get("description", "")
            )
            db.add(habit)
            records_added += 1
            
    elif "date" in columns and "productivity_score" in columns:
        for _, row in df.iterrows():
            score = ProductivityScore(
                user_id=user_id,
                date=pd.to_datetime(row["date"]).date(),
                productivity_score=float(row.get("productivity_score", 0)) if not pd.isna(row.get("productivity_score")) else 0.0,
                focus_score=float(row.get("focus_score", 0)) if not pd.isna(row.get("focus_score")) else 0.0,
                consistency_score=float(row.get("consistency_score", 0)) if not pd.isna(row.get("consistency_score")) else 0.0,
                discipline_score=float(row.get("discipline_score", 0)) if not pd.isna(row.get("discipline_score")) else 0.0,
                deep_work_score=float(row.get("deep_work_score", 0)) if not pd.isna(row.get("deep_work_score")) else 0.0
            )
            db.add(score)
            records_added += 1
    else:
        raise ValueError("Unrecognized CSV format. Ensure CSV contains expected columns for Sessions, Habits, or Scores.")
        
    db.commit()
    return records_added


def update_intelligence_state(user_id: int):
    # This is a mock background task to simulate updating the intelligence state
    print(f"Running background task: updating intelligence state for user {user_id}...")

@router.post("/upload")
async def upload_data(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    USER_ID = 1 
    
    try:
        contents = await file.read()
    except Exception as e:
        print(f"Error reading file stream: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
        
    records_added = 0
    
    try:
        if file.filename.endswith(".json"):
            # Use strict python json logic for json payload
            data = json.loads(contents.decode("utf-8"))
            records_added = process_json_data(data, db, user_id=USER_ID)
            
        elif file.filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
            records_added = process_and_store_csv(df, db, user_id=USER_ID)
            
        elif file.filename.endswith(".xlsx") or file.filename.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(contents))
            records_added = process_and_store_csv(df, db, user_id=USER_ID)
        else:
            raise ValueError("Unsupported file format. Please upload .json, .csv, or .xlsx")
            
    except Exception as e:
        db.rollback()
        print("\n" + "="*50)
        print(f"DATABASE INSERTION OR PARSING FAILED FOR {file.filename}")
        print("EXACT EXCEPTION:")
        traceback.print_exc(file=sys.stdout)
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=f"Internal Server Error processing file: {str(e)}")
        
    # Trigger background tasks to update the intelligence layer
    background_tasks.add_task(update_intelligence_state, USER_ID)

    return {
        "status": "success", 
        "message": f"Successfully processed and stored {records_added} records.",
        "records_added": records_added
    }
