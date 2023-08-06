class UnknownClassEncoder(Exception):
    """
    Raised when there is no defined encoding for a structure of a certain class.
    """
    pass


class UnknownClassDecoder(Exception):
    """
    Raised when there is no defined decoding method for a structure of a certain class.
    """
    pass
