import time
from functools import wraps
from flask import request, jsonify

# Simple in-memory rate limiter for MVP
# In production, this would use Redis
RATE_LIMIT_CACHE = {}

def rate_limit(max_requests=10, window_seconds=60):
    """
    Rate limiter decorator.
    Protects LLM/RAG endpoints from abuse.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ip = request.remote_addr
            current_time = time.time()
            
            if ip not in RATE_LIMIT_CACHE:
                RATE_LIMIT_CACHE[ip] = []
                
            # Filter out old requests outside the window
            RATE_LIMIT_CACHE[ip] = [
                req_time for req_time in RATE_LIMIT_CACHE[ip] 
                if current_time - req_time < window_seconds
            ]
            
            if len(RATE_LIMIT_CACHE[ip]) >= max_requests:
                return jsonify({
                    "error": "Rate limit exceeded", 
                    "message": f"Maximum {max_requests} requests per {window_seconds}s allowed."
                }), 429
                
            RATE_LIMIT_CACHE[ip].append(current_time)
            return f(*args, **kwargs)
        return wrapped
    return decorator
