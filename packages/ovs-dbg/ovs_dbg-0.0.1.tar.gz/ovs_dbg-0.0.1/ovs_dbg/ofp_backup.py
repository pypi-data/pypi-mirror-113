# """ Defines the parsers needed to parse ofproto flows
# """
#
# import functools
# import re
#
# from ovs_dbg.kv import KVParser, KVDecoders, ParseError
# from ovs_dbg.list import ListParser, ListDecoders
# from ovs_dbg.decoders import (decode_int, decode_mask32, decode_default,
#                              nested_kv_decoder, kv_decoder,
#                              nested_list_decoder)
#
# class OFPFlow:
#    """OpenFlow Flow"""
#
#    def __init__(self, data, actions):
#        """Constructor"""
#        self._data = data
#        self._actions = actions
#
#    def actions(self):
#        return self._actions
#
#    def keys(self):
#        return self._data
#
#    @classmethod
#    def from_string(cls, ofp_string):
#        """Parse a ofproto flow string
#
#        :param ofp_string: a ofproto string as dumped by ovs-ofctl tool
#        :type ofp_string: str
#
#        :return: an OFPFlow with the content of the flow string
#        :rtype: OFPFlow
#        """
#        parts = ofp_string.split("actions=")
#        if len(parts) != 2:
#            raise ValueError("malformed ofproto flow: {}", ofp_string)
#
#        match_decoders = cls._match_decoders()
#        mdecoder = KVParser(match_decoders)
#        mdecoder.parse(parts[0])
#
#        act_decoders = cls._act_decoders()
#        adecoder = KVParser(act_decoders)
#        adecoder.parse(parts[1])
#
#        return cls(mdecoder.kv(), adecoder.kv())
#
#    @classmethod
#    def _match_decoders(cls):
#        """Generate the match decoders"""
#        regs = {"reg%s" % i: decode_mask32 for i in range(0, 16)}
#        matches = {
#            "priority": decode_int,
#            "metadata": decode_int,
#        }
#        return KVDecoders(decoders={**matches, **regs})
#
#    @classmethod
#    def _act_decoders(cls):
#        """Generate the actions decoders"""
#        adec = dict()
#
#        return KVDecoders(adec,
#                          default_free=decode_free_action_field)
#
#    def __str__(self):
#        string = "Matches: "
#        for match in self._data:
#            string += "    " + str(match)
#        string += "\n"
#
#        string += "Actions: "
#        for act in self._actions:
#            string += "    " + str(act)
#
#        return string
#
#
# def decode_free_action_field(value):
#    """decoder that handles free (non key-value) vields in action strings
#
#    :param: value: the free value to decode
#    :type value: str
#
#    :return: the key and the value to store
#    :rtype: (string, [int or string])
#    """
#    try:
#        return "output", int(value)
#    except ValueError:
#        return "output", value
#
#
##
##def decode_controller(value):
##    """decoder for controller action
##    """
##    if not value:
##        return True
##    else:
##        # Try controller:max_len
##        try:
##            max_len = int(value)
##            return {
##                "max_len": max_len,
##            }
##        except ValueError:
##            pass
##        # controller(key[=val], ...)
##        return nested_kv_decoder()(value)
##
##
##def decode_field_action(value):
##    """decoder for ofproto field modification actions
##
##    Example:
##        load:0x001122334455->OXM_OF_ETH_SRC[]
##        move:reg0[0..5]->reg1[26..31]
##    """
##    parts = value.split("->")
##    if len(parts) < 2:
##        raise ParseError("Invalid field action: %s" % value)
##    return {
##        "source": parts[0],
##        "destination": parts[1],
##    }
##
##
##def decode_enqueue(value):
##    """decoder that handles free (non key-value) vields in action strings
##
##    :param: value: the free value to decode
##    :type value: str
##
##    :return: the key and the value to store
##    :rtype: (string, [int or string])
##    """
##    parts = re.split(r',\:', value)
##    if len(parts) != 2:
##        raise ParseError("malformed enqueue value: %s" & value)
##    try:
##        port = int(parts[0])
##    except ValueError:
##        port = parts[0]
##
##    try:
##        queue = int(parts[1], 0)
##    except ValueError:
##        raise ParseError("malformed enqueue value: %s" & value)
##
##    return {
##        "port": port,
##        "queue": queue,
##    }
##
##def decode_free_action_field(value):
##    """decoder that handles free (non key-value) vields in action strings
##
##    :param: value: the free value to decode
##    :type value: str
##
##    :return: the key and the value to store
##    :rtype: (string, [int or string])
##    """
##    try:
##        return "output", int(value)
##    except ValueError:
##        return "output", value
##
