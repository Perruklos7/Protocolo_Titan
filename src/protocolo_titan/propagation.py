import math
import numpy as np
import pandas as pd

from .config import GSMConfig


def kmh_to_ms(speed_kmh: float) -> float:
    if speed_kmh < 0:
        raise ValueError("La velocidad no puede ser negativa.")
    return speed_kmh / 3.6


def max_doppler_hz(speed_ms: float, carrier_frequency_hz: float, speed_of_light_ms: float = 3e8) -> float:
    if carrier_frequency_hz <= 0:
        raise ValueError("La frecuencia debe ser positiva.")
    if speed_of_light_ms <= 0:
        raise ValueError("La velocidad de propagación debe ser positiva.")
    return speed_ms * carrier_frequency_hz / speed_of_light_ms


def coherence_time_s(doppler_hz: float) -> float:
    if doppler_hz <= 0:
        return math.inf
    return 0.423 / doppler_hz


def classify_timeslot_stability(coherence_s: float, timeslot_s: float) -> str:
    """Clasifica la estabilidad del canal durante una ráfaga GSM."""
    ratio = coherence_s / timeslot_s

    if ratio >= 10:
        return "cuasiestatico"
    if ratio >= 3:
        return "estable_con_margen_reducido"
    if ratio >= 1:
        return "estable_pero_critico"
    return "variable_durante_timeslot"


def simulate_flat_fading(
    doppler_hz: float,
    config: GSMConfig = GSMConfig(),
    model: str = "rayleigh",
    k_factor_db: float = 6.0,
    samples: int = 512,
    seed: int = 7,
) -> pd.DataFrame:
    """Simula fading plano Rayleigh o Rician durante un timeslot GSM.

    Es una simulación docente, no un sustituto de un modelo Jakes completo.
    Permite visualizar el cambio relativo de la envolvente dentro de una ráfaga.
    """
    if samples < 32:
        raise ValueError("samples debe ser >= 32.")
    if doppler_hz < 0:
        raise ValueError("doppler_hz no puede ser negativo.")

    rng = np.random.default_rng(seed)
    t = np.linspace(0.0, config.timeslot_duration_s, samples)

    phase = 2 * np.pi * doppler_hz * t

    # Componente difusa compleja con suavizado para representar correlación temporal.
    real = rng.normal(0, 1, samples)
    imag = rng.normal(0, 1, samples)

    window_len = max(5, samples // 24)
    window = np.ones(window_len) / window_len

    real = np.convolve(real, window, mode="same")
    imag = np.convolve(imag, window, mode="same")

    diffuse = (real + 1j * imag) * np.exp(1j * phase)

    if model.lower() == "rayleigh":
        h = diffuse
    elif model.lower() == "rician":
        k = 10 ** (k_factor_db / 10)
        los = np.sqrt(k / (k + 1)) * np.exp(1j * phase)
        nlos = np.sqrt(1 / (k + 1)) * diffuse
        h = los + nlos
    else:
        raise ValueError("model debe ser 'rayleigh' o 'rician'.")

    envelope = np.abs(h)
    envelope = envelope / envelope.mean()

    return pd.DataFrame(
        {
            "time_us": t * 1e6,
            "envelope_normalized": envelope,
            "real": np.real(h),
            "imag": np.imag(h),
            "doppler_hz": doppler_hz,
            "model": model.lower(),
        }
    )


def fading_metrics(df: pd.DataFrame) -> dict:
    """Calcula métricas simples de variación de envolvente durante la ráfaga."""
    env = df["envelope_normalized"].to_numpy()
    return {
        "model": df["model"].iloc[0],
        "doppler_hz": float(df["doppler_hz"].iloc[0]),
        "envelope_min": float(env.min()),
        "envelope_max": float(env.max()),
        "envelope_std": float(env.std()),
        "relative_peak_to_peak": float(env.max() - env.min()),
    }
