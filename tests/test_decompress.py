import sys

import pytest

from tests.base import data_file_string_is_accurate
from tests.config import DATA_FILE
from tests.utils.imports import clear_imported_modules


@pytest.mark.run(order=1)
def test_decompress_with_gzip():
    sys.modules['mgzip'] = None
    from gharchive.unzip import decompress
    with open(DATA_FILE, 'rb') as f:
        data = decompress(f.read()).decode('utf8')

    assert data_file_string_is_accurate(data)

    import gharchive.unzip
    import gzip

    assert gharchive.unzip._get_gzip_module() is gzip
    clear_imported_modules(['gzip', 'mgzip', 'gharchive.unzip', 'gharchive'])


@pytest.mark.run(order=2)
def test_decompress_with_mgzip():
    from gharchive.unzip import decompress

    with open(DATA_FILE, 'rb') as f:
        data = decompress(f.read()).decode('utf8')

    assert data_file_string_is_accurate(data)

    import gharchive.unzip
    import mgzip

    assert gharchive.unzip._get_gzip_module() is mgzip