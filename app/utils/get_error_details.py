from fastapi.exceptions import RequestValidationError
from app.schemas.response import ErrorDetail

def get_error_details(exc: RequestValidationError) -> list[dict]:
    """Extracts field and message details from validation errors."""
    error_details = []
    for error in exc.errors():
        # Memastikan bahwa loc ada
        field_name = str(error["loc"][-1]) if error["loc"] else "unknown"  # Mengonversi ke string
        
        # Mengambil pesan dengan aman
        message = "Validation error"  # Default message
        if "ctx" in error and "error" in error["ctx"]:
            error_instance = error["ctx"]["error"]
            if hasattr(error_instance, 'args') and error_instance.args:
                message = error_instance.args[0]
            else:
                # Menggunakan error di ctx jika tidak ada args
                message = error["ctx"]["error"]
        elif "msg" in error:
            message = error["msg"]

        # Menangani kesalahan JSON decode
        if error.get("type") == "json_invalid":
            message = "Invalid JSON format. " + message

        error_details.append(ErrorDetail(field=field_name, message=message).model_dump())
        
    return error_details
