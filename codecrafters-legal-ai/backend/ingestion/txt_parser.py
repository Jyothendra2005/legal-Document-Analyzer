def parse_txt_bytes(content: bytes) -> str:
    return content.decode("utf-8", errors="ignore")
