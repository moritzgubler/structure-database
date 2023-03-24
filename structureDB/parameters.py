
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

dbname = "structureDB.json"

@dataclass_json
@dataclass
class structureDBParameters:
    ns: int = 1
    np: int = 0
    width_cufoff: float = 4.0
    maxnatsphere: int = 50
    fpd_max: float = 1e-3
    e_thresh: float = 1e-2
    exclude: list = field(default_factory=list)
    db_name: str = 'structureDB'