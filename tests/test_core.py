import math

from protocolo_titan.propagation import kmh_to_ms, max_doppler_hz, coherence_time_s
from protocolo_titan.cellular_planning import carriers_per_cell, reuse_distance_km, reuse_ratio
from protocolo_titan.instrumentation import analyzer_noise_floor_dbm


def test_speed_conversion():
    assert math.isclose(kmh_to_ms(50), 13.8888888889)


def test_doppler_50_kmh_900mhz():
    v = kmh_to_ms(50)
    assert math.isclose(max_doppler_hz(v, 900e6), 41.6666666667)


def test_coherence_250_kmh():
    v = kmh_to_ms(250)
    fd = max_doppler_hz(v, 900e6)
    assert math.isclose(coherence_time_s(fd) * 1e3, 2.0304, rel_tol=1e-3)


def test_carriers_per_cell():
    assert carriers_per_cell(24, 4) == 6


def test_reuse_distance():
    assert math.isclose(reuse_ratio(4), math.sqrt(12))
    assert math.isclose(reuse_distance_km(1.5, 4), 5.1961524, rel_tol=1e-6)


def test_noise_floor():
    assert math.isclose(analyzer_noise_floor_dbm(100e3, 6), -118.0)
    assert math.isclose(analyzer_noise_floor_dbm(10e3, 6), -128.0)
    assert math.isclose(analyzer_noise_floor_dbm(1e3, 6), -138.0)
