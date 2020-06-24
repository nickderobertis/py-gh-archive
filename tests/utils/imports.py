import sys
from typing import Sequence


def clear_imported_modules(names: Sequence[str]):
    new_modules = {
        m_name: mod for m_name, mod in sys.modules.items() if m_name not in names
    }
    sys.modules = new_modules
