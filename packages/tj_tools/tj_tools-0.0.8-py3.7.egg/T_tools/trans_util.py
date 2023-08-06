import hashlib
import base64


def md5(inp: str) -> str:
    return hashlib.md5(inp.encode("utf-8")).hexdigest()


def base64_encode(inp: str) -> str:
    return base64.b64encode(inp.encode("utf-8")).decode("utf-8")


def base64_decode(inp: str) -> str:
    return base64.b64decode(inp).decode("utf-8")
