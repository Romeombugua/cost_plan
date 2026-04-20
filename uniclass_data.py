"""
Uniclass 2015 Data Model — UK Unified Classification System
Tables: EF (Elements/Functions), Ss (Systems), Pr (Products)
With NRM 1 cross-reference mappings

DESIGN: Dynamic data-driven architecture — all codes derived from data, never hardcoded in UI
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class UniclassEntry:
    code: str
    description: str
    table: str  # "EF", "Ss", or "Pr"
    level: int  # hierarchy depth
    parent_code: Optional[str]
    nrm_mapping: Optional[str]  # NRM 1 cross-reference


UNICLASS_CATALOGUE: list[UniclassEntry] = [
    # ─── EF: Elements/Functions ───────────────────────────────────────────
    UniclassEntry("EF_20", "Structural elements", "EF", 1, None, None),
    UniclassEntry("EF_20_05", "Substructure", "EF", 2, "EF_20", "1.1"),
    UniclassEntry("EF_20_05_30", "Foundations", "EF", 3, "EF_20_05", "1.1.1"),
    UniclassEntry("EF_20_05_65", "Pile foundations", "EF", 3, "EF_20_05", "1.1.2"),
    UniclassEntry("EF_20_05_50", "Lowest floor construction", "EF", 3, "EF_20_05", "1.1.3"),
    UniclassEntry("EF_20_10", "Frames", "EF", 2, "EF_20", "2.1"),
    UniclassEntry("EF_20_10_75", "Steel frames", "EF", 3, "EF_20_10", "2.1.1"),
    UniclassEntry("EF_20_10_20", "Concrete frames", "EF", 3, "EF_20_10", "2.1.2"),
    UniclassEntry("EF_20_10_85", "Timber frames", "EF", 3, "EF_20_10", "2.1.3"),
    UniclassEntry("EF_20_15", "Floors and galleries", "EF", 2, "EF_20", "2.2"),
    UniclassEntry("EF_20_15_30", "Floor structures", "EF", 3, "EF_20_15", "2.2.1"),
    UniclassEntry("EF_20_20", "Roofs", "EF", 2, "EF_20", "2.3"),
    UniclassEntry("EF_20_20_70", "Roof structures", "EF", 3, "EF_20_20", "2.3.1"),
    UniclassEntry("EF_20_20_75", "Roof coverings", "EF", 3, "EF_20_20", "2.3.2"),
    UniclassEntry("EF_20_20_25", "Roof drainage", "EF", 3, "EF_20_20", "2.3.3"),
    UniclassEntry("EF_20_20_70_50", "Rooflights", "EF", 4, "EF_20_20_70", "2.3.4"),
    UniclassEntry("EF_20_30", "Stairs and ramps", "EF", 2, "EF_20", "2.4"),
    UniclassEntry("EF_20_30_75", "Stair structures", "EF", 3, "EF_20_30", "2.4.1"),

    UniclassEntry("EF_25", "Wall and barrier elements", "EF", 1, None, None),
    UniclassEntry("EF_25_10", "External walls", "EF", 2, "EF_25", "2.5"),
    UniclassEntry("EF_25_10_30", "External wall structures", "EF", 3, "EF_25_10", "2.5.1"),
    UniclassEntry("EF_25_10_15", "Curtain walling", "EF", 3, "EF_25_10", "2.5.3"),
    UniclassEntry("EF_25_20", "Internal walls", "EF", 2, "EF_25", "2.7"),
    UniclassEntry("EF_25_20_45", "Internal wall structures", "EF", 3, "EF_25_20", "2.7.1"),
    UniclassEntry("EF_25_20_55", "Moveable partitions", "EF", 3, "EF_25_20", "2.7.3"),
    UniclassEntry("EF_25_30", "Windows", "EF", 2, "EF_25", "2.6"),
    UniclassEntry("EF_25_30_30", "External windows", "EF", 3, "EF_25_30", "2.6.1"),
    UniclassEntry("EF_25_40", "Doors and access", "EF", 2, "EF_25", "2.6"),
    UniclassEntry("EF_25_40_25", "External doors", "EF", 3, "EF_25_40", "2.6.2"),
    UniclassEntry("EF_25_40_45", "Internal doors", "EF", 3, "EF_25_40", "2.8.1"),

    UniclassEntry("EF_30", "Finish elements", "EF", 1, None, None),
    UniclassEntry("EF_30_10", "Wall finishes", "EF", 2, "EF_30", "3.1"),
    UniclassEntry("EF_30_10_90", "Wall finish systems", "EF", 3, "EF_30_10", "3.1.1"),
    UniclassEntry("EF_30_20", "Floor finishes", "EF", 2, "EF_30", "3.2"),
    UniclassEntry("EF_30_20_35", "Floor finish systems", "EF", 3, "EF_30_20", "3.2.1"),
    UniclassEntry("EF_30_20_70", "Raised access floors", "EF", 3, "EF_30_20", "3.2.2"),
    UniclassEntry("EF_30_30", "Ceiling finishes", "EF", 2, "EF_30", "3.3"),
    UniclassEntry("EF_30_30_15", "Ceiling finish systems", "EF", 3, "EF_30_30", "3.3.1"),
    UniclassEntry("EF_30_30_80", "Suspended ceilings", "EF", 3, "EF_30_30", "3.3.2"),

    UniclassEntry("EF_35", "Fitting elements", "EF", 1, None, None),
    UniclassEntry("EF_35_10", "General fittings", "EF", 2, "EF_35", "4.1"),
    UniclassEntry("EF_35_10_40", "Kitchen fittings", "EF", 3, "EF_35_10", "4.1.2"),
    UniclassEntry("EF_35_10_72", "Signage", "EF", 3, "EF_35_10", "4.1.4"),
    UniclassEntry("EF_35_40", "Sanitary fittings", "EF", 2, "EF_35", "5.1"),
    UniclassEntry("EF_35_40_70", "Sanitary appliances", "EF", 3, "EF_35_40", "5.1.1"),

    UniclassEntry("EF_40", "Piped supply elements", "EF", 1, None, None),
    UniclassEntry("EF_40_10", "Cold water supply", "EF", 2, "EF_40", "5.4"),
    UniclassEntry("EF_40_10_15", "Cold water distribution", "EF", 3, "EF_40_10", "5.4.2"),
    UniclassEntry("EF_40_20", "Hot water supply", "EF", 2, "EF_40", "5.4"),
    UniclassEntry("EF_40_20_40", "Hot water distribution", "EF", 3, "EF_40_20", "5.4.3"),
    UniclassEntry("EF_40_30", "Heating", "EF", 2, "EF_40", "5.5"),
    UniclassEntry("EF_40_30_40", "Heat source", "EF", 3, "EF_40_30", "5.5.1"),

    UniclassEntry("EF_50", "Waste disposal elements", "EF", 1, None, None),
    UniclassEntry("EF_50_10", "Foul drainage", "EF", 2, "EF_50", "5.3"),
    UniclassEntry("EF_50_10_30", "Foul drainage above ground", "EF", 3, "EF_50_10", "5.3.1"),
    UniclassEntry("EF_50_20", "Refuse disposal", "EF", 2, "EF_50", "5.3"),
    UniclassEntry("EF_50_20_70", "Refuse disposal systems", "EF", 3, "EF_50_20", "5.3.3"),

    UniclassEntry("EF_55", "Space conditioning elements", "EF", 1, None, None),
    UniclassEntry("EF_55_10", "Heating systems", "EF", 2, "EF_55", "5.6"),
    UniclassEntry("EF_55_10_15", "Central heating", "EF", 3, "EF_55_10", "5.6.1"),
    UniclassEntry("EF_55_10_50", "Local heating", "EF", 3, "EF_55_10", "5.6.2"),
    UniclassEntry("EF_55_20", "Cooling systems", "EF", 2, "EF_55", "5.6"),
    UniclassEntry("EF_55_20_15", "Central cooling", "EF", 3, "EF_55_20", "5.6.3"),
    UniclassEntry("EF_55_30", "Ventilation", "EF", 2, "EF_55", "5.7"),
    UniclassEntry("EF_55_30_15", "Central ventilation", "EF", 3, "EF_55_30", "5.7.1"),
    UniclassEntry("EF_55_30_50", "Local ventilation", "EF", 3, "EF_55_30", "5.7.2"),
    UniclassEntry("EF_55_30_73", "Smoke extract", "EF", 3, "EF_55_30", "5.7.3"),

    UniclassEntry("EF_60", "Electrical elements", "EF", 1, None, None),
    UniclassEntry("EF_60_10", "Electrical supply", "EF", 2, "EF_60", "5.8"),
    UniclassEntry("EF_60_10_25", "Electrical distribution", "EF", 3, "EF_60_10", "5.8.1"),
    UniclassEntry("EF_60_10_65", "Power installations", "EF", 3, "EF_60_10", "5.8.2"),
    UniclassEntry("EF_60_30", "Lighting", "EF", 2, "EF_60", "5.8"),
    UniclassEntry("EF_60_30_45", "Lighting installations", "EF", 3, "EF_60_30", "5.8.3"),
    UniclassEntry("EF_60_40", "Communications", "EF", 2, "EF_60", "5.12"),
    UniclassEntry("EF_60_40_80", "Telecoms and data", "EF", 3, "EF_60_40", "5.12.1"),
    UniclassEntry("EF_60_50", "Security", "EF", 2, "EF_60", "5.12"),
    UniclassEntry("EF_60_50_72", "Security systems", "EF", 3, "EF_60_50", "5.12.2"),
    UniclassEntry("EF_60_60", "BMS", "EF", 2, "EF_60", "5.12"),
    UniclassEntry("EF_60_60_10", "Building management systems", "EF", 3, "EF_60_60", "5.12.3"),

    UniclassEntry("EF_65", "Transport elements", "EF", 1, None, None),
    UniclassEntry("EF_65_10", "Lifts", "EF", 2, "EF_65", "5.10"),
    UniclassEntry("EF_65_10_50", "Passenger lifts", "EF", 3, "EF_65_10", "5.10.1"),
    UniclassEntry("EF_65_20", "Escalators", "EF", 2, "EF_65", "5.10"),
    UniclassEntry("EF_65_20_30", "Escalator systems", "EF", 3, "EF_65_20", "5.10.2"),

    UniclassEntry("EF_70", "Protection elements", "EF", 1, None, None),
    UniclassEntry("EF_70_10", "Fire protection", "EF", 2, "EF_70", "5.11"),
    UniclassEntry("EF_70_10_32", "Fire fighting systems", "EF", 3, "EF_70_10", "5.11.1"),
    UniclassEntry("EF_70_10_33", "Fire suppression", "EF", 3, "EF_70_10", "5.11.2"),
    UniclassEntry("EF_70_20", "Lightning protection", "EF", 2, "EF_70", "5.11"),
    UniclassEntry("EF_70_20_50", "Lightning protection systems", "EF", 3, "EF_70_20", "5.11.3"),

    UniclassEntry("EF_75", "Site elements", "EF", 1, None, None),
    UniclassEntry("EF_75_10", "Site preparation", "EF", 2, "EF_75", "8.1"),
    UniclassEntry("EF_75_10_72", "Site clearance", "EF", 3, "EF_75_10", "8.1.1"),
    UniclassEntry("EF_75_20", "Roads and pavings", "EF", 2, "EF_75", "8.2"),
    UniclassEntry("EF_75_20_70", "Roads and car parks", "EF", 3, "EF_75_20", "8.2.1"),
    UniclassEntry("EF_75_20_60", "Paths and pavings", "EF", 3, "EF_75_20", "8.2.2"),
    UniclassEntry("EF_75_30", "Soft landscaping", "EF", 2, "EF_75", "8.3"),
    UniclassEntry("EF_75_30_72", "Seeding and turfing", "EF", 3, "EF_75_30", "8.3.1"),
    UniclassEntry("EF_75_30_65", "Planting", "EF", 3, "EF_75_30", "8.3.2"),
    UniclassEntry("EF_75_40", "Fencing and barriers", "EF", 2, "EF_75", "8.4"),
    UniclassEntry("EF_75_40_30", "Fencing and railings", "EF", 3, "EF_75_40", "8.4.1"),
    UniclassEntry("EF_75_50", "External drainage", "EF", 2, "EF_75", "8.6"),
    UniclassEntry("EF_75_50_80", "Surface water drainage", "EF", 3, "EF_75_50", "8.6.1"),
    UniclassEntry("EF_75_60", "External services", "EF", 2, "EF_75", "8.7"),

    # ─── Ss: Systems ──────────────────────────────────────────────────────
    UniclassEntry("Ss_20", "Structural systems", "Ss", 1, None, None),
    UniclassEntry("Ss_20_05", "Foundation systems", "Ss", 2, "Ss_20", "1.1"),
    UniclassEntry("Ss_20_05_30", "Strip foundations", "Ss", 3, "Ss_20_05", "1.1.1"),
    UniclassEntry("Ss_20_05_65", "Piled foundations", "Ss", 3, "Ss_20_05", "1.1.2"),
    UniclassEntry("Ss_20_05_70", "Raft foundations", "Ss", 3, "Ss_20_05", "1.1.1"),
    UniclassEntry("Ss_20_10", "Frame systems", "Ss", 2, "Ss_20", "2.1"),
    UniclassEntry("Ss_20_10_75", "Steel frame systems", "Ss", 3, "Ss_20_10", "2.1.1"),
    UniclassEntry("Ss_20_10_20", "Concrete frame systems", "Ss", 3, "Ss_20_10", "2.1.2"),
    UniclassEntry("Ss_20_15", "Floor systems", "Ss", 2, "Ss_20", "2.2"),
    UniclassEntry("Ss_20_15_20", "Concrete floor systems", "Ss", 3, "Ss_20_15", "2.2.1"),
    UniclassEntry("Ss_20_20", "Roof systems", "Ss", 2, "Ss_20", "2.3"),
    UniclassEntry("Ss_20_20_30", "Flat roof systems", "Ss", 3, "Ss_20_20", "2.3.2"),
    UniclassEntry("Ss_20_20_65", "Pitched roof systems", "Ss", 3, "Ss_20_20", "2.3.2"),
    UniclassEntry("Ss_20_30", "Stair systems", "Ss", 2, "Ss_20", "2.4"),

    UniclassEntry("Ss_25", "Wall and barrier systems", "Ss", 1, None, None),
    UniclassEntry("Ss_25_10", "External wall systems", "Ss", 2, "Ss_25", "2.5"),
    UniclassEntry("Ss_25_10_10", "Brick/block wall systems", "Ss", 3, "Ss_25_10", "2.5.1"),
    UniclassEntry("Ss_25_10_15", "Curtain wall systems", "Ss", 3, "Ss_25_10", "2.5.3"),
    UniclassEntry("Ss_25_10_30", "Cladding systems", "Ss", 3, "Ss_25_10", "2.5.3"),
    UniclassEntry("Ss_25_20", "Internal wall systems", "Ss", 2, "Ss_25", "2.7"),
    UniclassEntry("Ss_25_20_25", "Drylining systems", "Ss", 3, "Ss_25_20", "2.7.1"),
    UniclassEntry("Ss_25_20_55", "Partition systems", "Ss", 3, "Ss_25_20", "2.7.1"),
    UniclassEntry("Ss_25_30", "Window systems", "Ss", 2, "Ss_25", "2.6"),
    UniclassEntry("Ss_25_30_02", "Aluminium window systems", "Ss", 3, "Ss_25_30", "2.6.1"),
    UniclassEntry("Ss_25_40", "Door systems", "Ss", 2, "Ss_25", "2.8"),
    UniclassEntry("Ss_25_40_45", "Internal door systems", "Ss", 3, "Ss_25_40", "2.8.1"),
    UniclassEntry("Ss_25_40_25", "External door systems", "Ss", 3, "Ss_25_40", "2.6.2"),

    UniclassEntry("Ss_30", "Finish systems", "Ss", 1, None, None),
    UniclassEntry("Ss_30_10", "Wall finish systems", "Ss", 2, "Ss_30", "3.1"),
    UniclassEntry("Ss_30_10_60", "Plastering systems", "Ss", 3, "Ss_30_10", "3.1.1"),
    UniclassEntry("Ss_30_10_80", "Tiling systems", "Ss", 3, "Ss_30_10", "3.1.1"),
    UniclassEntry("Ss_30_20", "Floor finish systems", "Ss", 2, "Ss_30", "3.2"),
    UniclassEntry("Ss_30_20_12", "Carpet systems", "Ss", 3, "Ss_30_20", "3.2.1"),
    UniclassEntry("Ss_30_20_80", "Tile flooring systems", "Ss", 3, "Ss_30_20", "3.2.1"),
    UniclassEntry("Ss_30_30", "Ceiling finish systems", "Ss", 2, "Ss_30", "3.3"),
    UniclassEntry("Ss_30_30_80", "Suspended ceiling systems", "Ss", 3, "Ss_30_30", "3.3.2"),

    UniclassEntry("Ss_35", "Fitting systems", "Ss", 1, None, None),
    UniclassEntry("Ss_35_10", "General fitting systems", "Ss", 2, "Ss_35", "4.1"),
    UniclassEntry("Ss_35_10_40", "Kitchen fitting systems", "Ss", 3, "Ss_35_10", "4.1.2"),
    UniclassEntry("Ss_35_40", "Sanitary systems", "Ss", 2, "Ss_35", "5.1"),
    UniclassEntry("Ss_35_40_70", "Sanitary appliance systems", "Ss", 3, "Ss_35_40", "5.1.1"),

    UniclassEntry("Ss_40", "Piped supply systems", "Ss", 1, None, None),
    UniclassEntry("Ss_40_10", "Water supply systems", "Ss", 2, "Ss_40", "5.4"),
    UniclassEntry("Ss_40_10_15", "Cold water systems", "Ss", 3, "Ss_40_10", "5.4.2"),
    UniclassEntry("Ss_40_10_40", "Hot water systems", "Ss", 3, "Ss_40_10", "5.4.3"),
    UniclassEntry("Ss_40_20", "Heating supply systems", "Ss", 2, "Ss_40", "5.5"),
    UniclassEntry("Ss_40_20_40", "Boiler systems", "Ss", 3, "Ss_40_20", "5.5.1"),
    UniclassEntry("Ss_40_20_41", "Heat pump systems", "Ss", 3, "Ss_40_20", "5.5.1"),

    UniclassEntry("Ss_55", "HVAC systems", "Ss", 1, None, None),
    UniclassEntry("Ss_55_10", "Heating distribution systems", "Ss", 2, "Ss_55", "5.6"),
    UniclassEntry("Ss_55_20", "Cooling distribution systems", "Ss", 2, "Ss_55", "5.6"),
    UniclassEntry("Ss_55_30", "Ventilation systems", "Ss", 2, "Ss_55", "5.7"),
    UniclassEntry("Ss_55_30_02", "Air handling units", "Ss", 3, "Ss_55_30", "5.7.1"),

    UniclassEntry("Ss_60", "Electrical systems", "Ss", 1, None, None),
    UniclassEntry("Ss_60_10", "Electrical distribution systems", "Ss", 2, "Ss_60", "5.8"),
    UniclassEntry("Ss_60_10_25", "Electrical distribution boards", "Ss", 3, "Ss_60_10", "5.8.1"),
    UniclassEntry("Ss_60_30", "Lighting systems", "Ss", 2, "Ss_60", "5.8"),
    UniclassEntry("Ss_60_30_45", "General lighting systems", "Ss", 3, "Ss_60_30", "5.8.3"),
    UniclassEntry("Ss_60_40", "Communication systems", "Ss", 2, "Ss_60", "5.12"),
    UniclassEntry("Ss_60_40_80", "Structured cabling systems", "Ss", 3, "Ss_60_40", "5.12.1"),
    UniclassEntry("Ss_60_50", "Security systems", "Ss", 2, "Ss_60", "5.12"),
    UniclassEntry("Ss_60_50_02", "Access control systems", "Ss", 3, "Ss_60_50", "5.12.2"),
    UniclassEntry("Ss_60_50_12", "CCTV systems", "Ss", 3, "Ss_60_50", "5.12.2"),

    UniclassEntry("Ss_65", "Transport systems", "Ss", 1, None, None),
    UniclassEntry("Ss_65_10", "Lift systems", "Ss", 2, "Ss_65", "5.10"),
    UniclassEntry("Ss_65_10_60", "Passenger lift systems", "Ss", 3, "Ss_65_10", "5.10.1"),
    UniclassEntry("Ss_65_10_37", "Goods lift systems", "Ss", 3, "Ss_65_10", "5.10.1"),
    UniclassEntry("Ss_65_20", "Escalator systems", "Ss", 2, "Ss_65", "5.10"),

    UniclassEntry("Ss_70", "Protection systems", "Ss", 1, None, None),
    UniclassEntry("Ss_70_10", "Fire protection systems", "Ss", 2, "Ss_70", "5.11"),
    UniclassEntry("Ss_70_10_32", "Sprinkler systems", "Ss", 3, "Ss_70_10", "5.11.2"),
    UniclassEntry("Ss_70_10_33", "Fire alarm systems", "Ss", 3, "Ss_70_10", "5.11.1"),
    UniclassEntry("Ss_70_20", "Lightning protection systems", "Ss", 2, "Ss_70", "5.11"),

    UniclassEntry("Ss_75", "Site systems", "Ss", 1, None, None),
    UniclassEntry("Ss_75_10", "Site preparation systems", "Ss", 2, "Ss_75", "8.1"),
    UniclassEntry("Ss_75_20", "Road and paving systems", "Ss", 2, "Ss_75", "8.2"),
    UniclassEntry("Ss_75_30", "Landscaping systems", "Ss", 2, "Ss_75", "8.3"),
    UniclassEntry("Ss_75_40", "Fencing systems", "Ss", 2, "Ss_75", "8.4"),
    UniclassEntry("Ss_75_50", "Drainage systems", "Ss", 2, "Ss_75", "8.6"),

    # ─── Pr: Products ─────────────────────────────────────────────────────
    UniclassEntry("Pr_20", "Structural products", "Pr", 1, None, None),
    UniclassEntry("Pr_20_05", "Foundation products", "Pr", 2, "Pr_20", "1.1"),
    UniclassEntry("Pr_20_05_19", "Concrete piles", "Pr", 3, "Pr_20_05", "1.1.2"),
    UniclassEntry("Pr_20_05_76", "Steel piles", "Pr", 3, "Pr_20_05", "1.1.2"),
    UniclassEntry("Pr_20_10", "Frame products", "Pr", 2, "Pr_20", "2.1"),
    UniclassEntry("Pr_20_10_76", "Structural steel sections", "Pr", 3, "Pr_20_10", "2.1.1"),
    UniclassEntry("Pr_20_10_67", "Precast concrete units", "Pr", 3, "Pr_20_10", "2.1.2"),
    UniclassEntry("Pr_20_15", "Floor products", "Pr", 2, "Pr_20", "2.2"),
    UniclassEntry("Pr_20_15_67", "Precast floor units", "Pr", 3, "Pr_20_15", "2.2.1"),
    UniclassEntry("Pr_20_20", "Roof products", "Pr", 2, "Pr_20", "2.3"),
    UniclassEntry("Pr_20_20_50", "Metal roof sheets", "Pr", 3, "Pr_20_20", "2.3.2"),
    UniclassEntry("Pr_20_20_80", "Roof tiles", "Pr", 3, "Pr_20_20", "2.3.2"),

    UniclassEntry("Pr_25", "Wall products", "Pr", 1, None, None),
    UniclassEntry("Pr_25_10", "External wall products", "Pr", 2, "Pr_25", "2.5"),
    UniclassEntry("Pr_25_10_10", "Bricks", "Pr", 3, "Pr_25_10", "2.5.1"),
    UniclassEntry("Pr_25_10_09", "Blocks", "Pr", 3, "Pr_25_10", "2.5.1"),
    UniclassEntry("Pr_25_10_15", "Cladding panels", "Pr", 3, "Pr_25_10", "2.5.3"),
    UniclassEntry("Pr_25_20", "Internal wall products", "Pr", 2, "Pr_25", "2.7"),
    UniclassEntry("Pr_25_20_65", "Plasterboard", "Pr", 3, "Pr_25_20", "2.7.1"),
    UniclassEntry("Pr_25_30", "Window products", "Pr", 2, "Pr_25", "2.6"),
    UniclassEntry("Pr_25_30_02", "Aluminium windows", "Pr", 3, "Pr_25_30", "2.6.1"),
    UniclassEntry("Pr_25_30_85", "Timber windows", "Pr", 3, "Pr_25_30", "2.6.1"),
    UniclassEntry("Pr_25_40", "Door products", "Pr", 2, "Pr_25", "2.8"),
    UniclassEntry("Pr_25_40_45", "Internal door sets", "Pr", 3, "Pr_25_40", "2.8.1"),
    UniclassEntry("Pr_25_40_25", "External door sets", "Pr", 3, "Pr_25_40", "2.6.2"),

    UniclassEntry("Pr_30", "Finish products", "Pr", 1, None, None),
    UniclassEntry("Pr_30_10", "Wall finish products", "Pr", 2, "Pr_30", "3.1"),
    UniclassEntry("Pr_30_10_60", "Plaster products", "Pr", 3, "Pr_30_10", "3.1.1"),
    UniclassEntry("Pr_30_10_80", "Wall tiles", "Pr", 3, "Pr_30_10", "3.1.1"),
    UniclassEntry("Pr_30_20", "Floor finish products", "Pr", 2, "Pr_30", "3.2"),
    UniclassEntry("Pr_30_20_12", "Carpet tiles", "Pr", 3, "Pr_30_20", "3.2.1"),
    UniclassEntry("Pr_30_20_88", "Vinyl flooring", "Pr", 3, "Pr_30_20", "3.2.1"),
    UniclassEntry("Pr_30_30", "Ceiling products", "Pr", 2, "Pr_30", "3.3"),
    UniclassEntry("Pr_30_30_80", "Ceiling tiles", "Pr", 3, "Pr_30_30", "3.3.2"),

    UniclassEntry("Pr_60", "Electrical products", "Pr", 1, None, None),
    UniclassEntry("Pr_60_10", "Electrical distribution products", "Pr", 2, "Pr_60", "5.8"),
    UniclassEntry("Pr_60_30", "Lighting products", "Pr", 2, "Pr_60", "5.8"),
    UniclassEntry("Pr_60_30_45", "Luminaires", "Pr", 3, "Pr_60_30", "5.8.3"),

    UniclassEntry("Pr_65", "Transport products", "Pr", 1, None, None),
    UniclassEntry("Pr_65_10", "Lift products", "Pr", 2, "Pr_65", "5.10"),
    UniclassEntry("Pr_65_10_50", "Lift cars", "Pr", 3, "Pr_65_10", "5.10.1"),

    UniclassEntry("Pr_70", "Protection products", "Pr", 1, None, None),
    UniclassEntry("Pr_70_10", "Fire protection products", "Pr", 2, "Pr_70", "5.11"),
    UniclassEntry("Pr_70_10_72", "Sprinkler heads", "Pr", 3, "Pr_70_10", "5.11.2"),
    UniclassEntry("Pr_70_10_33", "Fire detectors", "Pr", 3, "Pr_70_10", "5.11.1"),
]

# Build lookup indices
_uniclass_by_code: dict[str, UniclassEntry] = {e.code: e for e in UNICLASS_CATALOGUE}


def get_uniclass_by_code(code: str) -> Optional[UniclassEntry]:
    """Get Uniclass entry by code."""
    return _uniclass_by_code.get(code)


def get_uniclass_by_table(table: str) -> list[UniclassEntry]:
    """Get all Uniclass entries for a specific table (EF, Ss, Pr)."""
    return [e for e in UNICLASS_CATALOGUE if e.table == table]


def get_uniclass_for_nrm(nrm_code: str) -> list[UniclassEntry]:
    """Get Uniclass entries mapped to an NRM code (including parent matches)."""
    results = [e for e in UNICLASS_CATALOGUE if e.nrm_mapping == nrm_code]
    if results:
        return results
    
    # Try parent NRM code
    parts = nrm_code.split(".")
    while len(parts) > 1:
        parts.pop()
        parent_code = ".".join(parts)
        parent_results = [e for e in UNICLASS_CATALOGUE if e.nrm_mapping == parent_code]
        if parent_results:
            return parent_results
    
    return []


def derive_uniclass_table_options() -> list[dict]:
    """Derive unique Uniclass table options from data (dynamic-filters pattern)."""
    tables = sorted(set(e.table for e in UNICLASS_CATALOGUE))
    labels = {"EF": "EF — Elements/Functions", "Ss": "Ss — Systems", "Pr": "Pr — Products"}
    return [{"value": t, "label": labels.get(t, t)} for t in tables]


def build_uniclass_dropdown_options() -> list[dict]:
    """Build a flat list of Uniclass codes suitable for dropdown selection."""
    return [
        {"value": e.code, "label": f"{e.code} — {e.description}", "table": e.table, "level": e.level}
        for e in UNICLASS_CATALOGUE if e.level >= 2
    ]


def search_uniclass(query: str) -> list[UniclassEntry]:
    """Search Uniclass catalogue by description or code."""
    q = query.lower()
    return [e for e in UNICLASS_CATALOGUE if q in e.code.lower() or q in e.description.lower()]
