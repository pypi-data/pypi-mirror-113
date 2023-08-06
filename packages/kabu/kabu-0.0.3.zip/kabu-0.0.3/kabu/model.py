from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Company:
    code: str
    name: str
    market_name: str
    topix_33_code: Optional[str] = field(default=None)
    topix_33_name: Optional[str] = field(default=None)
    topix_17_code: Optional[str] = field(default=None)
    topix_17_name: Optional[str] = field(default=None)
    topix_new_index_series_code: Optional[int] = field(default=None)
    topix_new_index_series_name: Optional[str] = field(default=None)
    nikkei225: bool = field(default=False)