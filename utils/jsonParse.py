from datetime import datetime, date
from decimal import Decimal
from fastapi.responses import JSONResponse
import json
def json_serializable(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    return str(obj)

def retorno_json(data, status=200):
    return JSONResponse(content=json.loads(json.dumps(data, default=json_serializable)), status_code=status)