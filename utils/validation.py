import re

def validate_base64_image(input: str) -> bool:
    try:
        prefix = input.split(',')[0]
        data = input.split(',')[1]
        return "data:image/" in prefix and ";base64" in prefix\
            and re.compile("^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$").match(data) is not None
    except:
        return False
