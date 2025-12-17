import pint
from typing import List
from pype_schema.units import u

__all__ = [
    "units",
    "tag_types",
]

units: List[pint.Unit] = [
    u.degC,                      # Celsius
    u.degF,                      # Fahrenheit
    u.degK,                      # Kelvin
    u.Hz,                        # Hertz
    u.J,                         # Joule
    u.BTU,                       # British thermal units
    u.BTU / (u.ft ** 3),         # BTU / cubic foot
    u.kWh / u.ft**3 * u.min,     # killowatt-hour per cubic foot per minute
    u.kWh / (u.m ** 3),          # killowatt-hour per cubic meter
    u.mol,                       # mole
    u.kW,                        # Kilowatt
    u.Pa,                        # Pascal
    u.force_pound / (u.inch**2), # pounds per square inch
    u.V,                         # Volt
    u.kWh,                       # Kilowatt-hour
    u.W,                         # Watt
    u.m,                         # meter
    u.inch,                      # inch
    u.LMH,                       # liter squared per square meter per hour
    u.LMH / u.bar,               # LMH / bar
    u.W / (u.m ** 2),            # Watt per square meter
    u.m ** 3,                    # cubic meter
    u.ft ** 3,                   # cubic feet
    u.L,                         # liter
    u.gal,                       # gallon
    u.s,                         # second
    u.min,                       # minute
    u.hr,                        # hour
    u.day,                       # day
    u.MGD,                       # million gallons per day
    u.gal / u.min,               # gallons per minute
    u.gal / u.day,               # gallons per day
    u.hp,                        # horsepower
    u.ft ** 3 / u.min,           # cubic feet per minute
    u.m ** 3 / u.day,            # cubic meters per day
    u.m ** 3 / u.hr,             # cubic meters per hour
    u.mg / u.L,                  # milligram per liter
    u.g,                         # gram
    u.m / u.s,                   # meter per second
    u.dimensionless,             # dimensionless
]

tag_types: List[tag.TagType] = [
    tagType.Flow,  # flow through a connection
    tagType.Volume, 
    tagType.Level,
    tagType.Pressure,
    tagType.Temperature,
    tagType.RunTime,
    tagType.RunStatus,
    tagType.VSS,  # volatile suspended solids
    tagType.TSS,
    tagType.TDS,
    tagType.COD,
    tagType.BOD,
    tagType.pH,
    tagType.Conductivity,
    tagType.Turbidity,
    tagType.Rotation,
    tagType.Efficiency,
    tagType.StateOfCharge,
    tagType.InFlow,  # flow into a node
    tagType.OutFlow, # flow out of a node
    tagType.NetFlow,  # net flow through a node
    tagType.Speed,
    tagType.Frequency,
    tagType.Current,
    tagType.Voltage,
    tagType.Concentration,
    tagType.SetPoint,
]


