from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from .config import GSMConfig, ConvoyScenario, CampScenario, AnalyzerConfig
from .scenario_a import analyze_convoy_mobility, analyze_convoy_fading
from .scenario_b import analyze_camp_base
from .ui_charts import (
    figure_timeslot_signal,
    figure_noise,
    figure_cluster_map,
    figure_carrier_distribution,
    figure_spectrum_from_arfcns,
    figure_doppler_coherence,
    figure_reuse_distance,
    figure_small_camera_placeholder,
)


class TitanGuiApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Protocolo Titan — Ventana de Resultados")
        self.geometry("1320x860")
        self.configure(bg="#1d2431")
        self._init_variables()
        self._init_widgets()
        self.refresh()

    def _init_variables(self) -> None:
        self.fc_mhz = tk.DoubleVar(value=900.0)
        self.timeslot_us = tk.DoubleVar(value=577.0)
        self.speed_low = tk.DoubleVar(value=50.0)
        self.speed_high = tk.DoubleVar(value=250.0)
        self.speed_profile = tk.StringVar(value="250")
        self.total_carriers = tk.IntVar(value=24)
        self.cluster_size = tk.IntVar(value=4)
        self.radius_km = tk.DoubleVar(value=1.5)
        self.nf_db = tk.DoubleVar(value=6.0)
        self.metric_doppler = tk.StringVar(value="0 Hz")
        self.metric_coherence = tk.StringVar(value="0 ms")
        self.metric_stability = tk.StringVar(value="—")

    def _label(self, parent: tk.Widget, text: str) -> ttk.Label:
        return ttk.Label(parent, text=text, background="#1d2431", foreground="#e8f4ff")

    def _init_widgets(self) -> None:
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TNotebook", background="#192032", borderwidth=0)
        style.configure("TNotebook.Tab", background="#24304a", foreground="#e8f4ff", padding=[14, 10])
        style.map("TNotebook.Tab", background=[("selected", "#325182")])
        style.configure("TFrame", background="#152037")
        style.configure("TLabel", background="#152037", foreground="#e8f4ff")
        style.configure("TButton", background="#2a4a72", foreground="#e8f4ff")
        style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"), background="#152037")

        root_frame = ttk.Frame(self)
        root_frame.pack(fill="both", expand=True, padx=10, pady=10)
        root_frame.columnconfigure(1, weight=1)
        root_frame.rowconfigure(0, weight=1)

        controls = ttk.LabelFrame(root_frame, text="Parámetros", padding=14)
        controls.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        controls.columnconfigure(1, weight=1)

        rows = [
            ("Frecuencia central (MHz)", self.fc_mhz),
            ("Timeslot GSM (µs)", self.timeslot_us),
            ("Velocidad baja (km/h)", self.speed_low),
            ("Velocidad alta (km/h)", self.speed_high),
            ("Perfil activo (km/h)", self.speed_profile),
            ("Portadoras totales", self.total_carriers),
            ("Clúster N", self.cluster_size),
            ("Radio celda (km)", self.radius_km),
            ("Figura de ruido NF (dB)", self.nf_db),
        ]

        for idx, (label_text, variable) in enumerate(rows):
            self._label(controls, label_text).grid(row=idx, column=0, sticky="w", pady=5)
            if label_text == "Perfil activo (km/h)":
                combo = ttk.Combobox(controls, textvariable=variable, values=("50", "250"), state="readonly", width=18)
                combo.grid(row=idx, column=1, sticky="ew", pady=5)
            else:
                ttk.Entry(controls, textvariable=variable, width=20).grid(row=idx, column=1, sticky="ew", pady=5)

        ttk.Button(controls, text="Actualizar resultados", command=self.refresh).grid(row=len(rows), column=0, columnspan=2, sticky="ew", pady=(16, 0))

        notebook = ttk.Notebook(root_frame)
        notebook.grid(row=0, column=1, sticky="nsew")

        self.tab_a = ttk.Frame(notebook)
        self.tab_b = ttk.Frame(notebook)
        notebook.add(self.tab_a, text="Escenario A")
        notebook.add(self.tab_b, text="Escenario B")

        self._build_tab_a()
        self._build_tab_b()

    def _build_tab_a(self) -> None:
        frame = self.tab_a
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)

        header = ttk.Label(frame, text="Convoy de alta velocidad", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(8, 14), padx=10)

        metrics = ttk.Frame(frame, padding=12)
        metrics.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)
        metrics.columnconfigure((0, 1, 2), weight=1)

        self._label(metrics, "Doppler máximo:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Label(metrics, textvariable=self.metric_doppler).grid(row=1, column=0, sticky="w")
        self._label(metrics, "Tiempo de coherencia:").grid(row=0, column=1, sticky="w", pady=4)
        ttk.Label(metrics, textvariable=self.metric_coherence).grid(row=1, column=1, sticky="w")
        self._label(metrics, "Estabilidad:").grid(row=0, column=2, sticky="w", pady=4)
        ttk.Label(metrics, textvariable=self.metric_stability).grid(row=1, column=2, sticky="w")

        self.camera_frame = ttk.Frame(frame, padding=10)
        self.camera_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.camera_frame.columnconfigure(0, weight=1)
        self.camera_frame.rowconfigure(0, weight=1)

        right = ttk.Frame(frame, padding=10)
        right.grid(row=2, column=1, sticky="nsew", padx=10, pady=5)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        self.doppler_frame = ttk.Frame(right)
        self.doppler_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        self.trace_frame = ttk.Frame(right)
        self.trace_frame.grid(row=1, column=0, sticky="nsew")

    def _build_tab_b(self) -> None:
        frame = self.tab_b
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        self.cluster_frame = ttk.Frame(frame, padding=10)
        self.cluster_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        self.reuse_frame = ttk.Frame(frame, padding=10)
        self.reuse_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        self.spectrum_frame = ttk.Frame(frame, padding=10)
        self.spectrum_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.noise_frame = ttk.Frame(frame, padding=10)
        self.noise_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

    def _draw_figure(self, fig, frame: tk.Widget) -> None:
        for child in frame.winfo_children():
            child.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh(self) -> None:
        plt.close("all")  # Libera la memoria de las figuras de la actualización anterior

        gsm = GSMConfig(carrier_frequency_hz=self.fc_mhz.get() * 1e6, timeslot_duration_s=self.timeslot_us.get() * 1e-6)
        convoy = ConvoyScenario(speeds_kmh=(self.speed_low.get(), self.speed_high.get()))
        camp = CampScenario(total_carriers=self.total_carriers.get(), cluster_size=self.cluster_size.get(), cell_radius_km=self.radius_km.get())
        analyzer = AnalyzerConfig(noise_figure_db=self.nf_db.get())

        mobility = analyze_convoy_mobility(convoy, gsm)
        fading_summary, traces = analyze_convoy_fading(convoy, gsm)
        camp_results = analyze_camp_base(camp, gsm, analyzer)

        try:
            speed = int(self.speed_profile.get())
        except ValueError:
            speed = 250
            self.speed_profile.set("250")

        if speed not in (50, 250):
            speed = 250
            self.speed_profile.set("250")

        trace_key = f"rician_{speed}_kmh"
        selected_trace = traces.get(trace_key, next(iter(traces.values())))
        selected_row = mobility[mobility["speed_kmh"] == float(speed)].iloc[0]

        self.metric_doppler.set(f"{selected_row['max_doppler_hz']:.0f} Hz")
        self.metric_coherence.set(f"{selected_row['coherence_time_ms']:.2f} ms")
        self.metric_stability.set(selected_row["stability_class"])

        self._draw_figure(figure_small_camera_placeholder(), self.camera_frame)
        self._draw_figure(figure_doppler_coherence(mobility), self.doppler_frame)
        self._draw_figure(figure_timeslot_signal(selected_trace), self.trace_frame)
        self._draw_figure(figure_cluster_map(), self.cluster_frame)
        self._draw_figure(figure_reuse_distance(camp_results["frequency_planning"]), self.reuse_frame)
        self._draw_figure(figure_spectrum_from_arfcns(camp_results["logical_channels"]), self.spectrum_frame)
        self._draw_figure(figure_noise(camp_results["rbw_noise"]), self.noise_frame)


def main() -> None:
    app = TitanGuiApp()
    app.mainloop()


if __name__ == "__main__":
    main()
