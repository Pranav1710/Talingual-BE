# utils/logging.py

def log_error(source: str, err: Exception):
    print(f"[ERROR] [{source}] {str(err)}")
