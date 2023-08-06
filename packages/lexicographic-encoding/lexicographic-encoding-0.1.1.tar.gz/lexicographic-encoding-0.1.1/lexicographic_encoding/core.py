from lexicographic_encoding.utils import get_encoder, get_decoder, _write_msbint, _read_msbint


def pack_unaryint(num: int, **kwargs):
    """
    Packs an integer in unary coding.
    If it is negative the sign is inserted before and the integer is complemented bitwise.
    """
    negative = num < 0
    num = -num if negative else num
    N = num
    encoding = bytearray(1 + (num + 1) // 8)
    encoding[0] = 128 + (127 if N >= 7 else 2**7 - 2**(7 - N))
    N -= 7
    for index in range(1, 1 + (num + 1) // 8):
        encoding[index] = 255 if N >= 8 else 2**8 - 2**(8 - min(N, 8))
        N -= 8
    if negative:
        for index in range(1 + (num + 1) // 8):
            encoding[index] = 255 - encoding[index]
    return encoding, bytes()


def unpack_unaryint(bstr: bytes, **kwargs):
    "Unpacks an unary coded integer, with the first bit as sign."
    bstr = bytearray(bstr)

    def bitat(index):
        return bstr[index // 8] & (128 >> (index % 8))

    negative = bitat(0) == 0
    num, index = 0, 1
    if negative:
        bstr[index // 8] = 255 - bstr[index // 8]
    while bitat(index) != 0:
        num += 1
        index += 1
        if negative and index % 8 == 0:
            bstr[index // 8] = 255 - bstr[index // 8]
    num = -num if negative else num
    return num, bstr[1 + index // 8:]


def pack_gammaint(num: int, **kwargs):
    """
    Packs an integer into gamma encoding: the integer itself is written in binary with the most significant
    byte first, and the length of the encoding is written beforehand in unary as a sequence of ones terminated
    by a zero.
    Signs are passed to the number representing the length.
    """
    negative = num < 0
    num = -num if negative else num
    encoding, length = _write_msbint(num)
    if negative:
        for i in range(length):
            encoding[i] = 255 - encoding[i]
    length = -length if negative else length
    length_encoding = pack_unaryint(length)[0]
    return length_encoding + encoding, bytes()


def unpack_gammaint(bstr: bytes, **kwargs):
    "Unpacks a gamma-coded integer"
    bstr = bytearray(bstr)
    length, start_number = unpack_unaryint(bstr)
    negative = length < 0
    length = -length if negative else length
    if negative:
        for i in range(length):
            start_number[i] = 255 - start_number[i]
    num = _read_msbint(start_number, length)
    num = -num if negative else num
    return num, start_number[length:]


def pack_deltaint(num: int, **kwargs):
    """
    Packs an integer into delta encoding: which is the integer in binary with the most significant byte first,
    preceded by the length of this representation written in gamma encoding.
    Signs are passed to the number representing the length.
    """
    negative = num < 0
    num = -num if negative else num
    encoding, length = _write_msbint(num)
    if negative:
        for i in range(length):
            encoding[i] = 255 - encoding[i]
    length = -length if negative else length
    length_encoding = pack_gammaint(length)[0]
    return length_encoding + encoding, bytes()


def unpack_deltaint(bstr: bytes, **kwargs):
    "Unpacks a delta-encoded integer"
    bstr = bytearray(bstr)
    length, start_number = unpack_gammaint(bstr)
    negative = length < 0
    length = -length if negative else length
    if negative:
        for i in range(length):
            start_number[i] = 255 - start_number[i]
    num = _read_msbint(start_number, length)
    num = -num if negative else num
    return num, start_number[length:]


def pack_bytes(bstr: bytes, **kwargs):
    """
    Packs bytes by appending the (optional) terminating string consisting of two null bytes.
    Each occurrence of a null byte is substituted by a null byte followed by a full byte.
    """
    return bstr.replace(b"\x00", b"\x00\xff"), bytes(b"\x00\x00")


def unpack_bytes(bstr: bytes, **kwargs):
    "Unpacks an encoded bytestring"
    if b"\x00\x00" in bstr:
        firstpart = bstr.split(b"\x00\x00")[0]
        return firstpart.replace(b"\x00\xff", b"\x00"), bstr[len(firstpart)+2:]
    result = bstr.replace(b"\x00\xff", b"\x00")
    return result, bytes()


def pack_string(string: str, **kwargs):
    """
    Packs a string by encoding it and using byte packing.
    """
    return pack_bytes(string.encode('utf-8'))


def unpack_string(bstr: bytes, **kwargs):
    "Unpacks a string by decoding bytes"
    encstring, rest = unpack_bytes(bstr)
    return encstring.decode('utf-8'), rest


def pack_bool(b: bool, **kwargs):
    "Packs a bool: false=0, true=1"
    return bytes([0]) if b is False else bytes([1]), bytes([])


def unpack_bool(bstr: bytes, **kwargs):
    "Unpacks a boolean"
    return True if bstr[0] == 1 else False, bstr[1:]


def pack_sequence(sequence, mapping=None):
    """
    Packs an eterogeneous iterable progressively.
    """
    if mapping is None:
        mapping = PACK_MAPPING
    encoding = bytes()
    custom_ending = bytes([0])
    for idx, element in enumerate(sequence):
        object_packing, ending = pack_general(element, mapping=mapping)
        if idx == len(sequence) - 1:
            custom_ending = ending + custom_ending
            ending = bytes()
        encoding = encoding + bytes([167]) + object_packing + ending
    return encoding, custom_ending


def unpack_sequence(bstr: bytes, mapping=None):
    "Unpacks an eterogeneous iterable"
    if mapping is None:
        mapping = UNPACK_MAPPING
    sequence = []
    while len(bstr) > 0 and bstr[0] == 167:
        # There is a new object at the current point
        read_obj, read_len = lexunpackb(bstr[1:], mapping=mapping)
        bstr = bstr[1+read_len:]
        sequence.append(read_obj)
    if len(bstr) > 0 and bstr[0] == 0:
        # If we have the signal that the stream is over we have to remove it
        bstr = bstr[1:]
    return sequence, bstr


def pack_tuple(tup, **kwargs):
    return pack_sequence(list(tup), **kwargs)


def unpack_tuple(bstr, **kwargs):
    seq, other = unpack_sequence(bstr, **kwargs)
    return tuple(seq), other


def pack_list(lst, **kwargs):
    return pack_sequence(list(lst), **kwargs)


def unpack_list(bstr, **kwargs):
    seq, other = unpack_sequence(bstr, **kwargs)
    return list(seq), other


def pack_set(st, **kwargs):
    # We need a stable order between elements, so we first pack them, then we order them, and then pack the sequence
    elements = list(sorted(st, key=lambda el: lexpackb(el, **kwargs)))
    return pack_sequence(elements, **kwargs)


def unpack_set(bstr, **kwargs):
    seq, other = unpack_sequence(bstr, **kwargs)
    return set(seq), other


def pack_dict(dct, **kwargs):
    # We pack the list of elements pairs ordered by the key lexpack
    elements = list(sorted(dct.items(), key=lambda el: lexpackb(el[0], **kwargs)))
    return pack_sequence(elements, **kwargs)


def unpack_dict(bstr, **kwargs):
    seq, other = unpack_sequence(bstr, **kwargs)
    return {k: v for k, v in seq}, other


def pack_none(none, **kwargs):
    return bytes(), bytes()


def unpack_none(bstr, **kwargs):
    return None, bstr


def pack_general(structure, mapping, **kwargs):
    "Dispatches on the kind of structure and returns the optional ending"
    struct_encoding_num, struct_encoding_fn = get_encoder(mapping, type(structure).__name__)
    encoded_struct, optional_after = struct_encoding_fn(structure, mapping=mapping, **kwargs)
    return bytes([struct_encoding_num]) + encoded_struct, optional_after


"""
Default mapping of types to encoding functions and headers.
Can be modified and passed to `lexpackb` to change the behaviour of the encodings.
"""
PACK_MAPPING = {
    "int": (0x01, pack_deltaint),
    "bytes": (0x02, pack_bytes),
    "str": (0x03, pack_string),
    "bool": (0x04, pack_bool),
    "tuple": (0x05, pack_tuple),
    "list": (0x06, pack_list),
    "set": (0x07, pack_set),
    "dict": (0x08, pack_dict),
    "NoneType": (0x09, pack_none),
}


"""
Default mapping of header to decoding functions.
Can be modified and passed to `lexunpackb` to change the behaviour of the decodings.
"""
UNPACK_MAPPING = {
    0x01: unpack_deltaint,
    0x02: unpack_bytes,
    0x03: unpack_string,
    0x04: unpack_bool,
    0x05: unpack_tuple,
    0x06: unpack_list,
    0x07: unpack_set,
    0x08: unpack_dict,
    0x09: unpack_none,
}


def lexpackb(structure, mapping=None, **kwargs):
    """
    Main function for encoding structures of nested sequences preserving lexicographic order and prefix relations.
    If mapping is None, PACK_MAPPING is used.

    Returns the bytes corresponding to the packing of the given structure.
    """
    if mapping is None:
        mapping = PACK_MAPPING
    return pack_general(structure, mapping=mapping, **kwargs)[0]


def lexunpackb(bstr, mapping=None, **kwargs):
    """
    Main function for decoding structures of nested sequences preserving lexicographic order and prefix relations.
    If mapping is None, UNPACK_MAPPING is used.

    Returns a tuple consisting of the decoded structure in first position and the length of the used part of the
    bytes as the second one.
    This allows composability of the function in more complex setup.
    """
    if mapping is None:
        mapping = UNPACK_MAPPING
    struct_encoding_num = bstr[0]
    struct_decoding_fn = get_decoder(mapping, struct_encoding_num)
    decoded_struct, remaining_part = struct_decoding_fn(bstr[1:], mapping=mapping, **kwargs)
    return decoded_struct, len(bstr) - len(remaining_part)
