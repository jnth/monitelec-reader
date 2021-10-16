import dataclasses
import datetime
import json


@dataclasses.dataclass
class Record:
    """Single record with indexes from teleinfo flow."""

    dt_utc: datetime.datetime
    adco: str
    optarif: str
    isousc: int
    hc: int
    hp: int
    ptec: str
    iinst: int
    imax: int
    papp: int
    hhphc: str
    motdetat: str

    def __post_init__(self):
        for field in dataclasses.fields(self):
            # Convert integer fields
            if field.type is int:
                setattr(self, field.name, int(getattr(self, field.name)))
            # Truncate `ptec` field
            if field.name == 'ptec':
                setattr(self, field.name, getattr(self, field.name)[0:2])

    def __str__(self):
        return ", ".join(f"{key} = {getattr(self, key)}"
                         for key in ('ptec', 'hc', 'hp', 'iinst', 'papp'))

    def as_json(self):
        """Information as JSON string (most compact JSON representation)."""
        return json.dumps({"dt_utc": self.dt_utc.strftime("%Y-%m-%d %H:%M:%S"), "ptec": self.ptec,
                           "hc": self.hc, "hp": self.hp, "isousc": self.isousc, "iinst": self.iinst, "papp": self.papp},
                          separators=(',', ':'))
