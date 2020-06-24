# Set gzip module
from types import ModuleType


def decompress(b: bytes) -> bytes:
    import_mod = _get_gzip_module()
    # TODO [$5ef35e658e4f8000083fdce6]: better typing for decompress
    #
    # Not sure how to specify type annotations to say that
    # import_mod should be a module which has the function decompress.
    # Once this is determined I can remove the type ignore
    return import_mod.decompress(b)  # type: ignore


def _get_gzip_module() -> ModuleType:
    import_mod: ModuleType
    try:
        import mgzip

        import_mod = mgzip
    except ImportError:
        import gzip

        import_mod = gzip
    return import_mod
