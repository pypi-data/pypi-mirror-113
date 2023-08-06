from lexicographic_encoding.exceptions import UnknownClassEncoder, UnknownClassDecoder


def get_encoder(dct, key):
    if key not in dct:
        raise UnknownClassEncoder(f"The type {key} has no known encoding methods.")
    return dct[key]


def get_decoder(dct, key):
    if key not in dct:
        raise UnknownClassDecoder(f"The class identifier {key} has no known decoding methods.")
    return dct[key]


def ilog(N, base):
    "Computes the integer logarithm of num in the specified base"
    logarithm = 0
    while N > 0:
        logarithm += 1
        N //= base
    return logarithm


def _write_msbint(num: int, base=256):
    "Packs a positive integer writing it with the most significant bit first."
    length = max(1, ilog(num, base))
    index = length
    encoding = bytearray(index)
    # Then recursively set the lower part of the byte
    while num > base - 1:
        index -= 1
        encoding[index] += num % base
        num //= base
    encoding[0] += num
    return encoding, length


def _read_msbint(bstr: bytes, length, base=256):
    "Unpacks an msb integer by considering only the lower part of its representation."
    # Then build the number from the end
    N = 0
    for value in bstr[:length]:
        N *= base
        N += value % base
    return N


def is_prefix_of(pref, big):
    """
    Checks whether the first object is a prefix of the second one.
    """
    if isinstance(pref, bytes) and isinstance(big, bytes):
        return big.startswith(pref)
    elif isinstance(pref, str) and isinstance(big, str):
        return big.startswith(pref)
    elif ((isinstance(pref, list) or isinstance(pref, tuple))
          and (isinstance(big, list) or isinstance(big, tuple))):
        # An iterable is expansion of another if they are equal for the whole range of the prefix,
        # except for the last element which can be an extension of the one in the prefix.
        for i in range(len(pref)):
            if i >= len(big):
                return False
            if pref[i] == big[i]:
                continue
            # They are different from each other
            ispref = is_prefix_of(pref[i], big[i])
            if ispref is None:
                return None
            if i == len(pref) - 1 and ispref:
                continue
            return False
        return True
    return None
