"""Top-level module for regexapp.

- support TextPattern, ElementPattern, LinePattern, and PatternBuilder
- support predefine pattern reference on system_setting.yaml
- allow end-user to customize pattern on /home/.regexapp/user_settings.yaml
- allow end-user to generate on GUI application and verify it.
"""

from regexapp.collection import TextPattern
from regexapp.collection import ElementPattern
from regexapp.collection import LinePattern
from regexapp.collection import PatternBuilder
from regexapp.collection import PatternReference

__version__ = '0.0.3'
version = __version__

__all__ = [
    'TextPattern',
    'ElementPattern',
    'LinePattern',
    'PatternBuilder',
    'PatternReference',
]