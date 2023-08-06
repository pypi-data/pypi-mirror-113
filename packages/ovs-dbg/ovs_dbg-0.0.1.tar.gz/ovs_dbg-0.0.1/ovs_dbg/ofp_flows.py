""" Defines the parsers needed to parse ofproto flows
"""

from flows import CSLParser


def kv_time(_, value):
    """time key-value parser

    Used for fields such as:
        duration=1234.123s
    """
    time_str = value.rstrip("s")
    return float(time_str)


def kv_int(_, value):
    """integer parser

    Used for fields such as:
        n_bytes=34
    """
    return int(value)
