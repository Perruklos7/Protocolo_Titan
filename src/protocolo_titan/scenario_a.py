import pandas as pd

from .config import GSMConfig, ConvoyScenario
from .propagation import (
    kmh_to_ms,
    max_doppler_hz,
    coherence_time_s,
    classify_timeslot_stability,
    simulate_flat_fading,
    fading_metrics,
)


def analyze_convoy_mobility(
    scenario: ConvoyScenario = ConvoyScenario(),
    config: GSMConfig = GSMConfig(),
) -> pd.DataFrame:
    """Calcula Doppler, coherencia y estabilidad del canal para el convoy."""
    rows = []

    for speed_kmh in scenario.speeds_kmh:
        speed_ms = kmh_to_ms(speed_kmh)
        fd = max_doppler_hz(speed_ms, config.carrier_frequency_hz, config.speed_of_light_ms)
        tc = coherence_time_s(fd)
        ratio = tc / config.timeslot_duration_s
        stability = classify_timeslot_stability(tc, config.timeslot_duration_s)

        rows.append(
            {
                "scenario": "A_convoy_alta_velocidad",
                "cell_radius_km": scenario.cell_radius_km,
                "speed_kmh": speed_kmh,
                "speed_ms": speed_ms,
                "carrier_frequency_mhz": config.carrier_frequency_hz / 1e6,
                "max_doppler_hz": fd,
                "coherence_time_ms": tc * 1e3,
                "gsm_timeslot_ms": config.timeslot_duration_s * 1e3,
                "coherence_to_timeslot_ratio": ratio,
                "stability_class": stability,
            }
        )

    return pd.DataFrame(rows)


def analyze_convoy_fading(
    scenario: ConvoyScenario = ConvoyScenario(),
    config: GSMConfig = GSMConfig(),
    models: tuple[str, ...] = ("rayleigh", "rician"),
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    """Simula Rayleigh/Rician para cada velocidad y resume métricas."""
    mobility = analyze_convoy_mobility(scenario, config)
    metrics_rows = []
    traces = {}

    for _, row in mobility.iterrows():
        for model in models:
            trace = simulate_flat_fading(
                doppler_hz=float(row["max_doppler_hz"]),
                config=config,
                model=model,
                seed=int(row["speed_kmh"]) + (0 if model == "rayleigh" else 1000),
            )
            key = f"{model}_{int(row['speed_kmh'])}_kmh"
            traces[key] = trace

            m = fading_metrics(trace)
            m.update(
                {
                    "speed_kmh": row["speed_kmh"],
                    "coherence_time_ms": row["coherence_time_ms"],
                    "stability_class": row["stability_class"],
                }
            )
            metrics_rows.append(m)

    return pd.DataFrame(metrics_rows), traces
