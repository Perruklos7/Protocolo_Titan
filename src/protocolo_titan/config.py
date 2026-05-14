from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class GSMConfig:
    """Parámetros de capa física GSM/EDGE empleados en el reto."""

    carrier_frequency_hz: float = 900e6
    channel_bandwidth_hz: float = 200e3
    speed_of_light_ms: float = 3e8
    timeslot_duration_s: float = 577e-6
    timeslots_per_frame: int = 8


@dataclass(frozen=True)
class ConvoyScenario:
    """Escenario A: convoy de alta velocidad en vía férrea."""

    cell_radius_km: float = 3.0
    speeds_kmh: Sequence[float] = (50.0, 250.0)


@dataclass(frozen=True)
class CampScenario:
    """Escenario B: campamento base con alta densidad operativa."""

    cell_radius_km: float = 1.5
    total_carriers: int = 24
    cluster_size: int = 4
    first_arfcn: int = 1


@dataclass(frozen=True)
class AnalyzerConfig:
    """Parámetros de instrumentación para certificación y medidas."""

    noise_figure_db: float = 6.0
    rbw_values_hz: Sequence[float] = (100e3, 10e3, 1e3)
