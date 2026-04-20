"""
ICMS 3rd Edition Data Model — International Cost Management Standard
Full hierarchy for cross-referencing with NRM 1 codes

DESIGN: Dynamic data-driven architecture — all codes derived from data, never hardcoded in UI
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class IcmsElement:
    code: str
    description: str
    level: int  # 1=category, 2=sub-category, 3=item


ICMS_CATALOGUE: list[IcmsElement] = [
    # ─── Category 1: Site ─────────────────────────────────────────────────
    IcmsElement("1", "Site", 1),
    IcmsElement("1.1", "Facilitating Works", 2),
    IcmsElement("1.1.1", "Toxic/hazardous material removal", 3),
    IcmsElement("1.1.2", "Major demolition works", 3),
    IcmsElement("1.1.3", "Temporary support to adjacent structures", 3),
    IcmsElement("1.1.4", "Specialist ground works", 3),
    IcmsElement("1.1.5", "Temporary diversion works", 3),
    IcmsElement("1.1.6", "Extraordinary site investigation works", 3),
    IcmsElement("1.2", "Substructure", 2),
    IcmsElement("1.2.1", "Standard/specialist foundations & lowest floor", 3),
    IcmsElement("1.2.2", "Basement construction", 3),

    # ─── Category 2: Building ─────────────────────────────────────────────
    IcmsElement("2", "Building", 1),
    IcmsElement("2.1", "Structure", 2),
    IcmsElement("2.1.1", "Frame", 3),
    IcmsElement("2.1.2", "Upper floors", 3),
    IcmsElement("2.1.3", "Stairs and ramps", 3),
    IcmsElement("2.2", "Roof", 2),
    IcmsElement("2.2.1", "Roof structure", 3),
    IcmsElement("2.2.2", "Roof coverings", 3),
    IcmsElement("2.2.3", "Roof drainage", 3),
    IcmsElement("2.2.4", "Rooflights and openings", 3),
    IcmsElement("2.3", "Exterior Enclosure", 2),
    IcmsElement("2.3.1", "External walls above ground", 3),
    IcmsElement("2.3.2", "External walls below ground", 3),
    IcmsElement("2.3.3", "Cladding and screens", 3),
    IcmsElement("2.3.4", "External soffits", 3),
    IcmsElement("2.3.5", "Subsidiary walls and balustrades", 3),
    IcmsElement("2.4", "Exterior Openings", 2),
    IcmsElement("2.4.1", "External windows", 3),
    IcmsElement("2.4.2", "External doors", 3),
    IcmsElement("2.5", "Interior Construction", 2),
    IcmsElement("2.5.1", "Internal walls and partitions", 3),
    IcmsElement("2.5.2", "Internal balustrades and handrails", 3),
    IcmsElement("2.5.3", "Moveable room dividers", 3),
    IcmsElement("2.6", "Interior Openings", 2),
    IcmsElement("2.6.1", "Internal doors", 3),
    IcmsElement("2.6.2", "Hatches", 3),

    # ─── Category 3: Interior Finishes ────────────────────────────────────
    IcmsElement("3", "Interior Finishes", 1),
    IcmsElement("3.1", "Wall Finishes", 2),
    IcmsElement("3.1.1", "Finishes to walls", 3),
    IcmsElement("3.2", "Floor Finishes", 2),
    IcmsElement("3.2.1", "Finishes to floors", 3),
    IcmsElement("3.2.2", "Raised access floors", 3),
    IcmsElement("3.3", "Ceiling Finishes", 2),
    IcmsElement("3.3.1", "Finishes to ceilings", 3),
    IcmsElement("3.3.2", "False/suspended ceilings", 3),
    IcmsElement("3.3.3", "Demountable suspended ceilings", 3),

    # ─── Category 4: Fittings ─────────────────────────────────────────────
    IcmsElement("4", "Fittings, Furnishings and Equipment", 1),
    IcmsElement("4.1", "Fittings and Equipment", 2),
    IcmsElement("4.1.1", "General fittings and equipment", 3),
    IcmsElement("4.1.2", "Domestic kitchen fittings", 3),
    IcmsElement("4.1.3", "Special purpose fittings", 3),
    IcmsElement("4.1.4", "Signs and notices", 3),
    IcmsElement("4.1.5", "Works of art", 3),
    IcmsElement("4.1.6", "Non-mechanical/electrical equipment", 3),
    IcmsElement("4.1.7", "Internal planting", 3),
    IcmsElement("4.1.8", "Bird and vermin control", 3),

    # ─── Category 5: Services ─────────────────────────────────────────────
    IcmsElement("5", "Services", 1),
    IcmsElement("5.1", "Sanitary Installations", 2),
    IcmsElement("5.1.1", "Sanitary appliances and fittings", 3),
    IcmsElement("5.2", "Services Equipment", 2),
    IcmsElement("5.2.1", "Services equipment", 3),
    IcmsElement("5.3", "Disposal Installations", 2),
    IcmsElement("5.3.1", "Foul drainage above ground", 3),
    IcmsElement("5.3.2", "Chemical/toxic waste drainage", 3),
    IcmsElement("5.3.3", "Refuse disposal", 3),
    IcmsElement("5.4", "Water Installations", 2),
    IcmsElement("5.4.1", "Mains water supply", 3),
    IcmsElement("5.4.2", "Cold water distribution", 3),
    IcmsElement("5.4.3", "Hot water distribution", 3),
    IcmsElement("5.4.4", "Local hot water distribution", 3),
    IcmsElement("5.4.5", "Steam and condensate distribution", 3),
    IcmsElement("5.5", "Heating", 2),
    IcmsElement("5.5.1", "Heat source", 3),
    IcmsElement("5.6", "HVAC", 2),
    IcmsElement("5.6.1", "Central heating", 3),
    IcmsElement("5.6.2", "Local heating", 3),
    IcmsElement("5.6.3", "Central cooling", 3),
    IcmsElement("5.6.4", "Local cooling", 3),
    IcmsElement("5.6.5", "Central air conditioning", 3),
    IcmsElement("5.6.6", "Local air conditioning", 3),
    IcmsElement("5.7", "Ventilation", 2),
    IcmsElement("5.7.1", "Central ventilation", 3),
    IcmsElement("5.7.2", "Local and special ventilation", 3),
    IcmsElement("5.7.3", "Smoke extract/control", 3),
    IcmsElement("5.8", "Electrical", 2),
    IcmsElement("5.8.1", "Electrical mains and sub-mains", 3),
    IcmsElement("5.8.2", "Power installations", 3),
    IcmsElement("5.8.3", "Lighting installations", 3),
    IcmsElement("5.8.4", "Specialist lighting", 3),
    IcmsElement("5.8.5", "Local electricity generation", 3),
    IcmsElement("5.8.6", "Earthing and bonding", 3),
    IcmsElement("5.9", "Fuel", 2),
    IcmsElement("5.9.1", "Fuel storage", 3),
    IcmsElement("5.9.2", "Fuel distribution", 3),
    IcmsElement("5.10", "Vertical Transportation", 2),
    IcmsElement("5.10.1", "Lifts and hoists", 3),
    IcmsElement("5.10.2", "Escalators", 3),
    IcmsElement("5.10.3", "Moving pavements", 3),
    IcmsElement("5.11", "Fire Protection", 2),
    IcmsElement("5.11.1", "Fire fighting systems", 3),
    IcmsElement("5.11.2", "Fire suppression systems", 3),
    IcmsElement("5.11.3", "Lightning protection", 3),
    IcmsElement("5.12", "Communication and Security", 2),
    IcmsElement("5.12.1", "Telecoms and data", 3),
    IcmsElement("5.12.2", "Security systems", 3),
    IcmsElement("5.12.3", "Building management systems", 3),
    IcmsElement("5.13", "Specialist Installations", 2),
    IcmsElement("5.13.1", "Specialist piped supply", 3),
    IcmsElement("5.13.2", "Specialist refrigeration", 3),
    IcmsElement("5.13.3", "Specialist mechanical", 3),
    IcmsElement("5.13.4", "Specialist electrical/electronic", 3),
    IcmsElement("5.14", "Builder's Work in Connection", 2),
    IcmsElement("5.14.1", "Builder's work in connection with services", 3),

    # ─── Category 6: Prefabricated ────────────────────────────────────────
    IcmsElement("6", "Prefabricated Buildings and Building Units", 1),
    IcmsElement("6.1", "Prefabricated Buildings", 2),
    IcmsElement("6.1.1", "Complete buildings", 3),
    IcmsElement("6.1.2", "Building units", 3),
    IcmsElement("6.1.3", "Pods", 3),

    # ─── Category 7: Work to Existing ─────────────────────────────────────
    IcmsElement("7", "Work to Existing Buildings", 1),
    IcmsElement("7.1", "Minor demolition and alteration works", 2),
    IcmsElement("7.2", "Repairs to existing services", 2),
    IcmsElement("7.3", "Damp-proof/fungus/beetle eradication", 2),
    IcmsElement("7.4", "Facade retention", 2),
    IcmsElement("7.5", "Cleaning existing surfaces", 2),
    IcmsElement("7.6", "Renovation works", 2),

    # ─── Category 8: External Works ───────────────────────────────────────
    IcmsElement("8", "External Works", 1),
    IcmsElement("8.1", "Site Preparation", 2),
    IcmsElement("8.1.1", "Site clearance", 3),
    IcmsElement("8.1.2", "Site earthworks", 3),
    IcmsElement("8.2", "Roads and Pavings", 2),
    IcmsElement("8.2.1", "Roads and car parks", 3),
    IcmsElement("8.2.2", "Paths and pavings", 3),
    IcmsElement("8.3", "Soft Landscaping", 2),
    IcmsElement("8.3.1", "Seeding and turfing", 3),
    IcmsElement("8.3.2", "External planting", 3),
    IcmsElement("8.3.3", "Irrigation systems", 3),
    IcmsElement("8.4", "Fencing and Walls", 2),
    IcmsElement("8.4.1", "Fencing and railings", 3),
    IcmsElement("8.4.2", "Walls and screens", 3),
    IcmsElement("8.5", "External Fixtures", 2),
    IcmsElement("8.5.1", "Site furniture and equipment", 3),
    IcmsElement("8.5.2", "Ornamental features", 3),
    IcmsElement("8.6", "External Drainage", 2),
    IcmsElement("8.6.1", "Surface/foul water drainage", 3),
    IcmsElement("8.6.2", "Ancillary drainage", 3),
    IcmsElement("8.7", "External Services", 2),
    IcmsElement("8.7.1", "Water mains supply", 3),
    IcmsElement("8.7.2", "Electricity mains supply", 3),
    IcmsElement("8.7.3", "Gas mains supply", 3),
    IcmsElement("8.7.4", "Telecoms and other services", 3),
    IcmsElement("8.8", "Minor Building Works", 2),
    IcmsElement("8.8.1", "Ancillary buildings", 3),
    IcmsElement("8.8.2", "Minor building works", 3),

    # ─── Categories 9-15: Non-building costs ──────────────────────────────
    IcmsElement("9", "Preliminaries", 1),
    IcmsElement("9.1", "Main contractor's preliminaries", 2),
    IcmsElement("10", "Overheads and Profit", 1),
    IcmsElement("10.1", "Main contractor's overheads", 2),
    IcmsElement("10.2", "Main contractor's profit", 2),
    IcmsElement("11", "Project/Design Team Fees", 1),
    IcmsElement("11.1", "Consultants' fees", 2),
    IcmsElement("11.2", "Pre-construction fees", 2),
    IcmsElement("11.3", "Design fees", 2),
    IcmsElement("12", "Other Development Costs", 1),
    IcmsElement("12.1", "Land acquisition costs", 2),
    IcmsElement("12.2", "Other development costs", 2),
    IcmsElement("13", "Risks", 1),
    IcmsElement("13.1", "Design development risks", 2),
    IcmsElement("13.2", "Construction risks", 2),
    IcmsElement("13.3", "Employer change risks", 2),
    IcmsElement("13.4", "Employer other risks", 2),
    IcmsElement("14", "Inflation", 1),
    IcmsElement("14.1", "Tender inflation", 2),
    IcmsElement("14.2", "Construction inflation", 2),
    IcmsElement("15", "VAT", 1),
    IcmsElement("15.1", "VAT assessment", 2),
]

# Build lookup indices
_icms_by_code: dict[str, IcmsElement] = {e.code: e for e in ICMS_CATALOGUE}


def get_icms_by_code(code: str) -> Optional[IcmsElement]:
    """Get ICMS element by code."""
    return _icms_by_code.get(code)


def get_icms_for_nrm(nrm_code: str) -> Optional[IcmsElement]:
    """Get the ICMS element mapped from an NRM code.
    
    Uses the NRM catalogue's icms_mapping field to find the ICMS entry.
    Falls back to parent NRM code if exact match not found.
    """
    from data.nrm_data import get_nrm_by_code
    nrm = get_nrm_by_code(nrm_code)
    if not nrm:
        return None
    
    icms = _icms_by_code.get(nrm.icms_mapping)
    if icms:
        return icms
    
    # Try parent ICMS code
    parts = nrm.icms_mapping.split(".")
    while len(parts) > 1:
        parts.pop()
        parent_code = ".".join(parts)
        parent = _icms_by_code.get(parent_code)
        if parent:
            return parent
    
    return None


def search_icms(query: str) -> list[IcmsElement]:
    """Search ICMS catalogue by description or code."""
    q = query.lower()
    return [e for e in ICMS_CATALOGUE if q in e.code.lower() or q in e.description.lower()]
