""" Defines helpful decoders that can be used to decode information from the
flows

A decoder is generally a callable that accepts a string and
returns the value object
"""

import functools
import netaddr

from ovs_dbg.kv import KVParser
from ovs_dbg.list import ListParser


def decode_default(value):
    """Default decoder.

    It tries to convert into an integer value and, if it fails, just
    returns the string.
    """
    try:
        ival = int(value, 0)
        return ival
    except ValueError:
        return value


def decode_int(value):
    """integer decoder

    Both base10 and base16 integers are supported

    Used for fields such as:
        n_bytes=34
        metadata=0x4
    """
    return int(value, 0)


def decode_time(value):
    """time decoder

    Used for fields such as:
        duration=1234.123s
    """
    time_str = value.rstrip("s")
    return float(time_str)


def decode_mask(size, value):
    """value/mask decoder for values of specific size (bits)

    Used for fields such as:
        reg0=0x248/0xff
    """
    parts = value.split("/")
    if len(parts) > 1:
        value = int(parts[0], 0)
        mask = int(parts[1], 0)
    else:
        value = int(parts[0], 0)
        mask = 2 ** size - 1

    return {"value": value, "mask": mask}


decode_mask8 = functools.partial(decode_mask, 8)
decode_mask16 = functools.partial(decode_mask, 16)
decode_mask32 = functools.partial(decode_mask, 32)
decode_mask64 = functools.partial(decode_mask, 64)


def decode_ip(value):
    """IP address decoder. Supports both IPv4 and IPv6 addresses

    Used for fields such as:
        nw_src=192.168.1.1
        nw_src=192.168.1.0/24
        nw_src=192.168.1.0/255.255.255.0
        nw_dst=2001:db8::1000
        nw_dst=2001:db8::0/24
    """
    try:
        ipnet = netaddr.IPNetwork(value)
        return ipnet
    except netaddr.AddrFormatError:
        raise ValueError("value %s: is not an ipv4 or ipv6 address" % value)


def decode_mac(value):
    """MAC address decoder"""
    try:
        mac = netaddr.EUI(value)
        return mac
    except netaddr.AddrFormatError:
        raise ValueError("value %s: is not an mac address" % value)


def decode_nested_kv(decoders, value):
    """A key-value decoder that extracts nested key-value pairs and returns
    them in a dictionary

    Args:
        decoders (KVDecoders): the KVDecoders to use.
        value (str): the value string to decode.
    """
    parser = KVParser(decoders)
    parser.parse(value)
    return {kv.key: kv.value for kv in parser.kv()}


def nested_kv_decoder(decoders=None):
    """Helper function that creates a nested kv decoder with given KVDecoders"""
    return functools.partial(decode_nested_kv, decoders)


def decode_nested_list(decoders, delims, value):
    """Extracts nested list from te string and returns it in a dictionary
    them in a dictionary

    Args:
        decoders (ListDecoders): the ListDecoders to use.
        value (str): the value string to decode.
    """
    parser = ListParser(decoders, delims)
    parser.parse(value)
    return {kv.key: kv.value for kv in parser.kv()}


def nested_list_decoder(decoders=None, delims=None):
    """Helper function that creates a nested list decoder with given
    ListDecoders
    """
    return functools.partial(decode_nested_list, decoders, delims)


def kv_decoder(decoder):
    """Convert simpler value decoder into kv_decoder

    A kv_decoder is a callable that accepts a keyword and a value string
    and returns the key and value objects. In most cases, the returned keyword
    is the same as the one provided.
    This helper function converts a value decoder (that just takes the value
    string as parameter and returns an object) into a kv_decoder where the key
    is the same
    """

    def kv_decoder(key, value):
        return key, decoder(value)

    return kv_decoder
