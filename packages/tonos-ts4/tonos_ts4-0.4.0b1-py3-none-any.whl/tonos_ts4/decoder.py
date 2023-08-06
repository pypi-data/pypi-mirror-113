import copy

from .util      import *
from .address   import *
from .abi       import *

# TODO: This class contains decoder settings
class Decoder:
    def __init__(self,
        ints        = None,     # whether decode integers or not
        strings     = None,     # decode string or leave it as `Bytes` object
        tuples      = None,     # when getter returns tuple whether to return it as tuple or if no return as a map/dict
        skip_fields = [],       # the list of field names to be skipped in decoding stage
    ):
        self.ints        = ints
        self.strings     = strings
        self.tuples      = tuples
        self.skip_fields = skip_fields
        
    # TODO: consider adding setters and getters
        
    @staticmethod
    def defaults():
        return Decoder(ints = True, strings = True)
        
    def fill_nones(self, other):
        return Decoder(
                ints        = either_or(self.ints,        other.ints),
                strings     = either_or(self.strings,     other.strings),
                tuples      = either_or(self.tuples,      other.tuples),
                skip_fields = either_or(self.skip_fields, other.skip_fields),
            )
        

def decode_json_value(value, abi_type, decoder):
    assert isinstance(abi_type, AbiType)
    type = abi_type.type

    if abi_type.is_int():
        return decode_int(value) if decoder.ints else value

    if abi_type.is_array():
        type2 = abi_type.remove_array()
        return [decode_json_value(v, type2, decoder) for v in value]

    if type == 'bool':
        return bool(value)

    if type == 'address':
        return Address(value)

    if type == 'cell':
        return Cell(value)

    if type == 'bytes':
        return bytes2str(value) if decoder.strings else Bytes(value)

    if type == 'tuple':
        assert isinstance(value, dict)
        res = {}
        for c in abi_type.components:
            field = c.name
            if c.dont_decode or field in decoder.skip_fields:
                res[field] = value[field]
            else:
                res[field] = decode_json_value(value[field], c, decoder)
        return res

    m = re.match(r'^map\((.*),(.*)\)$', type)
    if m:
        key_type = m.group(1)
        val_type = dict(name = None, type = m.group(2))
        if 'components' in abi_type.raw_:
            val_type['components'] = abi_type.raw_['components']
        val_type = AbiType(val_type)
        res = dict()
        for k in value.keys():
            if key_type == 'address':
                key = Address(k)
            else:
                key = decode_int(k)
            res[key] = decode_json_value(value[k], val_type, decoder)
        return res

    print(type, value)
    verbose_("Unsupported type '{}'".format(type))
    return value

