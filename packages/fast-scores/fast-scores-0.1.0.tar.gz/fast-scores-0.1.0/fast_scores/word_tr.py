"""Translate a word via mdx_dict."""
# from typing import List, Union

from pathlib import Path
import msgpack
from string import punctuation

_ = Path(__file__).parent
_ = Path(_, "msbing_c_e.msgpk")
mdx_dict = msgpack.load(open(_, "rb"))


def word_tr(word: str, strip: bool = True) -> str:
    """Translate a word via mdx_dict.

    Args:
        word: text (str) to translate
        strip: when True, word.strip(string.punctuation)

    Returns:
        "".join(mdx_dict.get(
            word.strip(punctuation), {}
        ).values())
    """
    if strip:
        return "".join(mdx_dict.get(word.strip(punctuation), {}).values())

    return "".join(mdx_dict.get(word, {}).values())
