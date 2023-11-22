def response(code: int, message: str, data: dict, error = ""):
    return {"code": code, "message": message, "data": data, "error": error}
