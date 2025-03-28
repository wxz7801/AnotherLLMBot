import re
from typing import Tuple


@staticmethod
def extract_reasoning(content: str) -> Tuple[str, str]:
    """CoT思维链提取"""
    match = re.search(r"(?:<think>)?(.*?)</think>", content, re.DOTALL)
    content = re.sub(r"(?:<think>)?.*?</think>", "", content, flags=re.DOTALL, count=1).strip()
    
    if match:
        reasoning = match.group(1).strip()
    else:
        reasoning = ""
    
    # print("==============================\n")
    # print("reasoning:", reasoning)
    # print("========================\n")
    # print("content:", content)
    # print("==============================\n")

    return content, reasoning