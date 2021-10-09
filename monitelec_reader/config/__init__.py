from pathlib import Path
from dynaconf import Dynaconf

root_dir = Path('.')
home_dir = Path('~').expanduser()

settings = Dynaconf(
    envvar_prefix="MONITELEC_READER",
    settings_files=[root_dir / 'settings.toml', '.secrets.toml', home_dir / '.monitelec-reader.toml'],
)

# `envvar_prefix` = export envvars with `export MONITELEC_READER_FOO=bar`.
# `settings_files` = Load this files in the order.
