from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def save_doppler_plot(df: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(df["speed_kmh"], df["max_doppler_hz"], marker="o")
    ax.set_xlabel("Velocidad (km/h)")
    ax.set_ylabel("Doppler máximo (Hz)")
    ax.set_title("Escenario A: efecto Doppler")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def save_coherence_plot(df: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df["speed_kmh"].astype(str), df["coherence_time_ms"])
    ax.axhline(df["gsm_timeslot_ms"].iloc[0], linestyle="--", label="Timeslot GSM")
    ax.set_xlabel("Velocidad (km/h)")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_title("Tiempo de coherencia frente a timeslot GSM")
    ax.legend()
    ax.grid(True, axis="y")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def save_fading_plot(df: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["time_us"], df["envelope_normalized"])
    model = df["model"].iloc[0]
    doppler = df["doppler_hz"].iloc[0]
    ax.set_xlabel("Tiempo dentro del timeslot (µs)")
    ax.set_ylabel("Envolvente normalizada")
    ax.set_title(f"Fading {model} durante 577 µs — fD={doppler:.2f} Hz")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def save_reuse_plot(df: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    cells = df["cell"]
    distances = df["reuse_distance_km"]
    ax.bar(cells, distances)
    ax.set_xlabel("Celda del clúster")
    ax.set_ylabel("Distancia de reutilización D (km)")
    ax.set_title("Escenario B: distancia de reutilización común")
    ax.grid(True, axis="y")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def save_noise_plot(df: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(df["rbw_khz"], df["noise_floor_dbm"], marker="o")
    ax.set_xscale("log")
    ax.set_xlabel("RBW (kHz)")
    ax.set_ylabel("Suelo de ruido (dBm)")
    ax.set_title("Instrumentación: ruido integrado frente a RBW")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
