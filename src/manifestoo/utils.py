from typing import List, Optional


def comma_split(s: Optional[str]) -> List[str]:
    if not s:
        return []
    s = s.strip()
    if not s:
        return []
    items = [item.strip() for item in s.split(",")]
    return [item for item in items if item]
