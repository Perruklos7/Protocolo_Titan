from __future__ import annotations

import sys
from pathlib import Path

import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Allow running the module directly as a script from the repository root.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from protocolo_titan.config import GSMConfig, ConvoyScenario, CampScenario, AnalyzerConfig
from protocolo_titan.scenario_a import analyze_convoy_mobility, analyze_convoy_fading
from protocolo_titan.scenario_b import analyze_camp_base
from protocolo_titan.ui_charts import (
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
        self.after(100, self.refresh)

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
        self.zoom_factor = tk.DoubleVar(value=1.0)
        self.metric_doppler = tk.StringVar(value="0 Hz")
        self.metric_coherence = tk.StringVar(value="0 ms")
        self.metric_stability = tk.StringVar(value="—")
        self.frequency_value = tk.StringVar(value="900.000 MHz")
        self.bandwidth_value = tk.StringVar(value="200 kHz")
        self.velocity_main = tk.StringVar(value="250 km/h")
        self.velocity_sub = tk.StringVar(value="50 km/h")
        self.doppler_value = tk.StringVar(value="0 Hz")
        self.coherence_value = tk.StringVar(value="0 ms")

    def _label(self, parent: tk.Widget, text: str) -> ttk.Label:
        return ttk.Label(parent, text=text, background="#1d2431", foreground="#e8f4ff")

    def _init_widgets(self) -> None:
        self.configure(bg="#08111F")
        self.sidebar_bg = "#091827"
        self.panel_bg = "#0D1724"
        self.card_bg = "#11223B"
        self.card_alt_bg = "#152844"
        self.text_fg = "#E8F5FF"
        self.subtext_fg = "#8FA4BF"
        self.accent = "#6BC4FF"

        root_frame = tk.Frame(self, bg=self.sidebar_bg)
        root_frame.pack(fill="both", expand=True)
        root_frame.columnconfigure(1, weight=1)
        root_frame.rowconfigure(0, weight=1)

        sidebar = tk.Frame(root_frame, bg=self.sidebar_bg, width=280)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        self._build_sidebar(sidebar)

        content_container = tk.Frame(root_frame, bg=self.panel_bg)
        content_container.grid(row=0, column=1, sticky="nsew")
        content_container.columnconfigure(0, weight=1)
        content_container.rowconfigure(0, weight=1)

        self.content_canvas = tk.Canvas(content_container, bg=self.panel_bg, highlightthickness=0)
        self.content_canvas.grid(row=0, column=0, sticky="nsew")

        self.content_scrollbar = ttk.Scrollbar(content_container, orient="vertical", command=self.content_canvas.yview)
        self.content_scrollbar.grid(row=0, column=1, sticky="ns")
        self.content_canvas.configure(yscrollcommand=self.content_scrollbar.set)

        self.content_frame = tk.Frame(self.content_canvas, bg=self.panel_bg)
        self.content_window = self.content_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", self._on_content_configure)
        self.content_canvas.bind("<Configure>", self._on_canvas_configure)
        self.content_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.content_canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.content_canvas.bind_all("<Button-5>", self._on_mousewheel)

        self._build_header(self.content_frame)
        self._build_main_tabs(self.content_frame)

    def _build_header(self, parent: tk.Widget) -> None:
        header = tk.Frame(parent, bg=self.card_bg)
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 12))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)

        title_block = tk.Frame(header, bg=self.card_bg)
        title_block.grid(row=0, column=0, sticky="nsew")
        tk.Label(title_block, text="Scenario Alpha: High-Speed Convoy", bg=self.card_bg, fg="#F8FBFF", font=("Segoe UI", 22, "bold"), anchor="w").pack(fill="x")
        tk.Label(title_block, text="Análisis de coherencia y espectro para comunicaciones GSM en convoy de alta velocidad.", bg=self.card_bg, fg=self.subtext_fg, font=("Segoe UI", 10), anchor="w", pady=6).pack(fill="x")

        badge_block = tk.Frame(header, bg=self.card_bg)
        badge_block.grid(row=0, column=1, sticky="e", padx=(12, 0))
        tk.Label(badge_block, text="GSM-900", bg="#0F1A2C", fg=self.accent, font=("Segoe UI", 10, "bold"), padx=10, pady=8).pack(anchor="e", pady=(0, 6))
        tk.Label(badge_block, text="900.000 MHz | 200 kHz", bg="#0F1A2C", fg=self.text_fg, font=("Segoe UI", 9), padx=10, pady=8).pack(anchor="e")

    def _build_main_tabs(self, parent: tk.Widget) -> None:
        notebook = ttk.Notebook(parent)
        notebook.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        notebook.columnconfigure(0, weight=1)
        notebook.rowconfigure(0, weight=1)

        self.input_tab = tk.Frame(notebook, bg=self.panel_bg)
        self.results_tab = tk.Frame(notebook, bg=self.panel_bg)
        notebook.add(self.input_tab, text="Parámetros")
        notebook.add(self.results_tab, text="Resultados")

        self._build_input_tab(self.input_tab)
        self._build_results_tab(self.results_tab)
        self.notebook = notebook

    def _build_section_card(self, parent: tk.Widget, title: str, subtitle: str = "") -> tk.Frame:
        section = tk.Frame(parent, bg=self.card_alt_bg, bd=0, padx=16, pady=16)
        section.pack(fill="x", pady=(0, 14))
        tk.Label(section, text=title, bg=self.card_alt_bg, fg=self.text_fg, font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x")
        if subtitle:
            tk.Label(section, text=subtitle, bg=self.card_alt_bg, fg=self.subtext_fg, font=("Segoe UI", 8), anchor="w", pady=6).pack(fill="x")
        return section

    def _build_input_row(self, parent: tk.Widget, label_text: str, variable: tk.Variable, min_value: float, max_value: float, increment: float, digits: int | None = None, unit: str = "") -> tk.Spinbox:
        row = tk.Frame(parent, bg=self.card_alt_bg)
        row.pack(fill="x", pady=6)
        tk.Label(row, text=label_text, bg=self.card_alt_bg, fg=self.subtext_fg, font=("Segoe UI", 9)).pack(anchor="w")
        input_frame = tk.Frame(row, bg=self.card_alt_bg)
        input_frame.pack(anchor="w", pady=6)
        spin = tk.Spinbox(
            input_frame,
            textvariable=variable,
            from_=min_value,
            to=max_value,
            increment=increment,
            width=12,
            font=("Segoe UI", 10),
            bd=0,
            relief="flat",
            justify="center",
        )
        if digits is not None:
            spin.config(format=f"%.{digits}f")
        spin.pack(side="left")
        if unit:
            tk.Label(input_frame, text=unit, bg=self.card_alt_bg, fg=self.accent, font=("Segoe UI", 10, "bold"), padx=8).pack(side="left")
        return spin

    def _select_tab(self, tab_name: str) -> None:
        if not hasattr(self, "notebook"):
            return
        for index in range(self.notebook.index("end")):
            if self.notebook.tab(index, "text") == tab_name:
                self.notebook.select(index)
                return

    def _build_input_tab(self, parent: tk.Widget) -> None:
        parent.columnconfigure((0, 1), weight=1)
        parent.rowconfigure(0, weight=1)

        left_panel = tk.Frame(parent, bg=self.panel_bg)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=8)
        right_panel = tk.Frame(parent, bg=self.panel_bg)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=8)

        left_panel.columnconfigure(0, weight=1)
        right_panel.columnconfigure(0, weight=1)

        global_section = self._build_section_card(left_panel, "Parámetros globales", "Configuración de onda y tiempos GSM")
        self._build_input_row(global_section, "Frecuencia central", self.fc_mhz, 100.0, 2000.0, 10.0, 1, "MHz")
        self._build_input_row(global_section, "Timeslot GSM", self.timeslot_us, 100.0, 1000.0, 1.0, 0, "µs")

        alpha_section = self._build_section_card(left_panel, "Escenario Alpha", "Movilidad del convoy y perfil de velocidad")
        self._build_input_row(alpha_section, "Velocidad baja", self.speed_low, 0.0, 150.0, 10.0, 0, "km/h")
        self._build_input_row(alpha_section, "Velocidad alta", self.speed_high, 150.0, 350.0, 10.0, 0, "km/h")
        profile_frame = tk.Frame(alpha_section, bg=self.card_alt_bg)
        profile_frame.pack(fill="x", pady=6)
        tk.Label(profile_frame, text="Perfil de velocidad", bg=self.card_alt_bg, fg=self.subtext_fg, font=("Segoe UI", 9)).pack(anchor="w")
        radio_frame = tk.Frame(profile_frame, bg=self.card_alt_bg)
        radio_frame.pack(anchor="w", pady=6)
        for value, label in [(50, "50 km/h"), (250, "250 km/h")]:
            tk.Radiobutton(
                radio_frame,
                text=label,
                variable=self.speed_profile,
                value=str(value),
                bg=self.card_alt_bg,
                fg=self.text_fg,
                selectcolor="#0D1724",
                activebackground=self.card_alt_bg,
                activeforeground=self.text_fg,
                font=("Segoe UI", 9),
                indicatoron=0,
                width=10,
                bd=0,
                relief="ridge",
                pady=6,
            ).pack(side="left", padx=(0, 8))

        beta_section = self._build_section_card(left_panel, "Escenario Beta", "Parámetros de planificación de portadoras y celda")
        self._build_input_row(beta_section, "Portadoras totales", self.total_carriers, 1, 100, 1, 0, "ch")
        self._build_input_row(beta_section, "Clúster N", self.cluster_size, 1, 16, 1, 0, "")
        self._build_input_row(beta_section, "Radio de celda", self.radius_km, 0.1, 10.0, 0.1, 1, "km")

        instrumentation_section = self._build_section_card(left_panel, "Instrumentación", "Control de ruido y condiciones de análisis")
        self._build_input_row(instrumentation_section, "Figura de ruido (NF)", self.nf_db, 0.0, 20.0, 0.5, 1, "dB")

        summary_card = tk.Frame(right_panel, bg=self.card_alt_bg, bd=0, padx=16, pady=16)
        summary_card.pack(fill="x")
        tk.Label(summary_card, text="Resumen actual", bg=self.card_alt_bg, fg=self.text_fg, font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x")
        tk.Label(summary_card, text="Valores cargados para el cálculo actual.", bg=self.card_alt_bg, fg=self.subtext_fg, font=("Segoe UI", 9), anchor="w", pady=6).pack(fill="x")

        for label, variable, unit in [
            ("Frecuencia", self.fc_mhz, "MHz"),
            ("Timeslot", self.timeslot_us, "µs"),
            ("Velocidad conv.", self.velocity_main, ""),
            ("Perfil", self.speed_profile, ""),
            ("Portadoras", self.total_carriers, ""),
            ("Clúster", self.cluster_size, ""),
            ("Radio", self.radius_km, "km"),
            ("NF", self.nf_db, "dB"),
        ]:
            row = tk.Frame(summary_card, bg=self.card_alt_bg)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"{label}:", bg=self.card_alt_bg, fg=self.subtext_fg, font=("Segoe UI", 9)).pack(side="left")
            tk.Label(row, textvariable=variable, bg=self.card_alt_bg, fg=self.text_fg, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(6, 0))
            if unit:
                tk.Label(row, text=unit, bg=self.card_alt_bg, fg=self.accent, font=("Segoe UI", 9)).pack(side="left", padx=(4, 0))

        tk.Button(
            right_panel,
            text="RECALCULAR RESULTADOS",
            command=lambda: (self.refresh(), self._select_tab("Resultados")),
            bg="#57C1FF",
            fg="#08111F",
            bd=0,
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=12,
        ).pack(fill="x", pady=12)

    def _build_results_tab(self, parent: tk.Widget) -> None:
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        band_frame = tk.Frame(parent, bg=self.panel_bg)
        band_frame.grid(row=0, column=0, sticky="ew", padx=18, pady=(12, 8))
        for i in range(4):
            band_frame.columnconfigure(i, weight=1, uniform="metrics")

        self._build_dashboard_card(band_frame, "Frecuencia Central", self.frequency_value, "MHz", 0)
        self._build_dashboard_card(band_frame, "Ancho de Banda", self.bandwidth_value, "", 1)
        self._build_dashboard_card(band_frame, "Velocidad Convoy", self.velocity_main, "", 2)
        self._build_dashboard_card(band_frame, "Estabilidad", self.metric_stability, "", 3)

        zoom_frame = tk.Frame(parent, bg=self.panel_bg)
        zoom_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 10))
        zoom_frame.columnconfigure(0, weight=1)
        zoom_frame.columnconfigure(1, weight=0)
        zoom_frame.columnconfigure(2, weight=0)
        zoom_frame.columnconfigure(3, weight=0)

        self._build_zoom_controls(zoom_frame)

        dashboard = tk.Frame(parent, bg=self.panel_bg)
        dashboard.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        dashboard.columnconfigure(0, weight=2)
        dashboard.columnconfigure(1, weight=1)
        dashboard.rowconfigure(0, weight=2)
        dashboard.rowconfigure(1, weight=1)

        left_panel = tk.Frame(dashboard, bg=self.card_bg)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=(0, 12))
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(0, weight=1)

        self.main_chart_frame = tk.Frame(left_panel, bg=self.card_bg)
        self.main_chart_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        right_panel = tk.Frame(dashboard, bg=self.card_bg)
        right_panel.grid(row=0, column=1, sticky="nsew", pady=(0, 12))
        right_panel.columnconfigure(0, weight=1)
        for i in range(3):
            right_panel.rowconfigure(i, weight=1)

        self._build_side_status(right_panel)

        self.side_chart_top = tk.Frame(right_panel, bg=self.card_alt_bg)
        self.side_chart_top.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 8))
        self.side_chart_bottom = tk.Frame(right_panel, bg=self.card_alt_bg)
        self.side_chart_bottom.grid(row=2, column=0, sticky="nsew", padx=16, pady=(8, 0))

        bottom_panel = tk.Frame(dashboard, bg=self.panel_bg)
        bottom_panel.grid(row=1, column=0, columnspan=2, sticky="nsew")
        for i in range(3):
            bottom_panel.columnconfigure(i, weight=1, uniform="bottom")

        self.bottom_chart_1 = tk.Frame(bottom_panel, bg=self.card_alt_bg)
        self.bottom_chart_1.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 0))
        self.bottom_chart_2 = tk.Frame(bottom_panel, bg=self.card_alt_bg)
        self.bottom_chart_2.grid(row=0, column=1, sticky="nsew", padx=8, pady=(0, 0))
        self.bottom_chart_3 = tk.Frame(bottom_panel, bg=self.card_alt_bg)
        self.bottom_chart_3.grid(row=0, column=2, sticky="nsew", padx=(8, 0), pady=(0, 0))

        self.diagram_frame = self.bottom_chart_3

    def _build_side_status(self, parent: tk.Widget) -> None:
        status_card = tk.Frame(parent, bg=self.card_alt_bg, padx=16, pady=16)
        status_card.grid(row=0, column=0, sticky="nsew", padx=16)
        status_card.columnconfigure(0, weight=1)
        tk.Label(status_card, text="Control de Misión", bg=self.card_alt_bg, fg=self.text_fg, font=("Segoe UI", 12, "bold"), anchor="w").grid(row=0, column=0, sticky="ew")
        tk.Label(status_card, text="Parámetros activos y estado operativo", bg=self.card_alt_bg, fg=self.subtext_fg, font=("Segoe UI", 9), anchor="w", pady=4).grid(row=1, column=0, sticky="ew")

        info_frame = tk.Frame(status_card, bg=self.card_alt_bg)
        info_frame.grid(row=2, column=0, sticky="ew", pady=(12, 14))
        for i in range(2):
            info_frame.columnconfigure(i, weight=1)
        self._build_info_box(info_frame, "Doppler", self.doppler_value, "Hz", 0)
        self._build_info_box(info_frame, "Coherencia", self.coherence_value, "ms", 1)

        tk.Button(
            status_card,
            text="EJECUTAR CÁLCULO",
            command=lambda: (self.refresh(), self._select_tab("Resultados")),
            bg="#57C1FF",
            fg="#08111F",
            bd=0,
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=12,
        ).grid(row=3, column=0, sticky="ew")

    def _build_dashboard_card(self, parent: tk.Widget, title: str, value_var: tk.StringVar, suffix: str, col: int) -> None:
        card = tk.Frame(parent, bg=self.card_bg, bd=0, relief="flat", padx=14, pady=14)
        card.grid(row=0, column=col, sticky="nsew", padx=(0, 12) if col < 3 else 0)
        tk.Label(card, text=title, bg=self.card_bg, fg=self.subtext_fg, font=("Segoe UI", 9)).pack(anchor="w")
        row = tk.Frame(card, bg=self.card_bg)
        row.pack(anchor="w", pady=(10, 0))
        tk.Label(row, textvariable=value_var, bg=self.card_bg, fg="#FFFFFF", font=("Segoe UI", 20, "bold")).pack(side="left")
        if suffix:
            tk.Label(row, text=f" {suffix}", bg=self.card_bg, fg=self.accent, font=("Segoe UI", 12, "bold")).pack(side="left")

    def _build_zoom_controls(self, parent: tk.Widget) -> None:
        label = tk.Label(parent, text="Zoom resultados:", bg=self.panel_bg, fg=self.text_fg, font=("Segoe UI", 10, "bold"))
        label.grid(row=0, column=0, sticky="w")

        minus_btn = tk.Button(parent, text="-", command=self._decrease_zoom, width=3, bg="#0F1A2C", fg=self.text_fg, bd=0, relief="flat", font=("Segoe UI", 10, "bold"))
        minus_btn.grid(row=0, column=1, padx=(8, 0))
        zoom_slider = ttk.Scale(
            parent,
            from_=0.5,
            to=2.0,
            orient="horizontal",
            variable=self.zoom_factor,
            command=self._slider_zoom,
            length=220,
        )
        zoom_slider.grid(row=0, column=2, padx=(8, 0), sticky="ew")
        zoom_value = tk.Label(parent, textvariable=self.zoom_factor, bg=self.panel_bg, fg=self.accent, font=("Segoe UI", 10, "bold"))
        zoom_value.grid(row=0, column=3, padx=(8, 0))
        plus_btn = tk.Button(parent, text="+", command=self._increase_zoom, width=3, bg="#0F1A2C", fg=self.text_fg, bd=0, relief="flat", font=("Segoe UI", 10, "bold"))
        plus_btn.grid(row=0, column=4, padx=(8, 0))

    def _increase_zoom(self) -> None:
        zoom = min(2.0, self.zoom_factor.get() + 0.1)
        self.zoom_factor.set(round(zoom, 2))
        self.refresh()

    def _decrease_zoom(self) -> None:
        zoom = max(0.5, self.zoom_factor.get() - 0.1)
        self.zoom_factor.set(round(zoom, 2))
        self.refresh()

    def _slider_zoom(self, value: str) -> None:
        zoom = round(float(value), 2)
        self.zoom_factor.set(zoom)
        self.refresh()

    def _on_content_configure(self, event: tk.Event) -> None:
        self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        self.content_canvas.itemconfig(self.content_window, width=event.width)

    def _on_mousewheel(self, event: tk.Event) -> None:
        if event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1
        else:
            delta = -1 * int(event.delta / 120)
        self.content_canvas.yview_scroll(delta, "units")

    def _build_info_box(self, parent: tk.Widget, title: str, value_var: tk.StringVar, unit: str, col: int) -> None:
        box = tk.Frame(parent, bg="#0F1A2C", bd=1, relief="solid", highlightbackground="#23496C", highlightcolor="#23496C", highlightthickness=1)
        box.grid(row=0, column=col, sticky="nsew", padx=(0, 8) if col == 0 else 0)
        tk.Label(box, text=title, bg="#0F1A2C", fg=self.subtext_fg, font=("Segoe UI", 9)).pack(anchor="w", padx=10, pady=(10, 0))
        value_frame = tk.Frame(box, bg="#0F1A2C")
        value_frame.pack(anchor="w", padx=10, pady=(6, 12))
        tk.Label(value_frame, textvariable=value_var, bg="#0F1A2C", fg="#FFFFFF", font=("Segoe UI", 16, "bold")).pack(side="left")
        tk.Label(value_frame, text=f" {unit}", bg="#0F1A2C", fg=self.accent, font=("Segoe UI", 11, "bold")).pack(side="left")

    def _build_sidebar(self, parent: tk.Widget) -> None:
        tk.Label(parent, text="Protocolo Titán", bg=self.sidebar_bg, fg="#ffffff", font=("Segoe UI", 16, "bold"), pady=22).pack(fill="x", padx=18)
        tk.Label(parent, text="v2.0.4 · Operacional", bg=self.sidebar_bg, fg=self.subtext_fg, font=("Segoe UI", 9), pady=2).pack(fill="x", padx=18)

        nav_box = tk.Frame(parent, bg=self.sidebar_bg)
        nav_box.pack(fill="x", padx=12, pady=(22, 0))
        nav_buttons = [
            ("Ver parámetros", "Parámetros"),
            ("Ver resultados", "Resultados"),
            ("Escenario Alpha", "Parámetros"),
            ("Escenario Beta", "Resultados"),
            ("ARFCN", "Resultados"),
            ("Telemetría", "Resultados"),
        ]
        for label, tab_name in nav_buttons:
            btn = tk.Button(
                nav_box,
                text=label,
                bg=self.sidebar_bg,
                fg=self.text_fg,
                bd=0,
                relief="flat",
                anchor="w",
                padx=16,
                pady=10,
                font=("Segoe UI", 10),
                command=lambda name=tab_name: self._select_tab(name),
            )
            btn.pack(fill="x", pady=4)

        config_card = tk.Frame(parent, bg=self.card_bg, bd=0, padx=14, pady=14)
        config_card.pack(fill="x", padx=16, pady=(18, 0))
        tk.Label(config_card, text="Parámetros", bg=self.card_bg, fg=self.text_fg, font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x")
        tk.Label(config_card, text="Ajusta el modelo antes de ejecutar el cálculo.", bg=self.card_bg, fg=self.subtext_fg, font=("Segoe UI", 8), anchor="w", pady=8).pack(fill="x")

        def input_row(label_text, variable, step, digits=None):
            row = tk.Frame(config_card, bg=self.card_bg)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=label_text, bg=self.card_bg, fg=self.subtext_fg, font=("Segoe UI", 9)).pack(anchor="w")
            spin = tk.Spinbox(row, textvariable=variable, from_=-9999, to=99999, increment=step, width=18, font=("Segoe UI", 10), bd=0, relief="flat", justify="center")
            if digits is not None:
                spin.config(format="%.{}f".format(digits))
            spin.pack(anchor="w", pady=4)
            return spin

        input_row("Frecuencia (MHz)", self.fc_mhz, 10.0, 1)
        input_row("Timeslot (µs)", self.timeslot_us, 1.0, 0)
        input_row("Velocidad baja (km/h)", self.speed_low, 10.0, 0)
        input_row("Velocidad alta (km/h)", self.speed_high, 10.0, 0)
        input_row("Portadoras totales", self.total_carriers, 1, 0)
        input_row("Clúster N", self.cluster_size, 1, 0)
        input_row("Radio celda (km)", self.radius_km, 0.1, 1)
        input_row("Figura de ruido (NF dB)", self.nf_db, 0.5, 1)

        tk.Button(
            parent,
            text="EJECUTAR CÁLCULO",
            bg="#57C1FF",
            fg="#08111F",
            bd=0,
            relief="flat",
            padx=18,
            pady=12,
            font=("Segoe UI", 11, "bold"),
            command=lambda: (self.refresh(), self._select_tab("Resultados")),
        ).pack(fill="x", padx=16, pady=18)

    def _build_stat_card(self, parent: tk.Widget, title: str, value_var: tk.StringVar, col: int, row: int) -> None:
        card = tk.Frame(parent, bg=self.card_bg, bd=0, relief="flat", padx=14, pady=14)
        card.grid(row=row, column=col, sticky="nsew", padx=(0, 12) if col == 0 else 0, pady=4)
        tk.Label(card, text=title, bg=self.card_bg, fg=self.subtext_fg, font=("Segoe UI", 9)).pack(anchor="w")
        tk.Label(card, textvariable=value_var, bg=self.card_bg, fg="#ffffff", font=("Segoe UI", 14, "bold"), pady=8).pack(anchor="w")

    def _build_metric_card(self, parent: tk.Widget, title: str, value_var: tk.StringVar, value_sub: tk.StringVar | None, col: int) -> None:
        card = tk.Frame(parent, bg=self.card_bg, bd=0, relief="flat", padx=16, pady=16)
        card.grid(row=0, column=col, sticky="nsew", padx=(0, 12) if col < 2 else 0)
        tk.Label(card, text=title, bg=self.card_bg, fg=self.subtext_fg, font=("Segoe UI", 10)).pack(anchor="w")
        tk.Label(card, textvariable=value_var, bg=self.card_bg, fg="#ffffff", font=("Segoe UI", 18, "bold"), pady=8).pack(anchor="w")
        if value_sub:
            subframe = tk.Frame(card, bg=self.card_bg)
            subframe.pack(anchor="w", pady=(4, 0))
            tk.Label(subframe, textvariable=value_sub, bg=self.card_bg, fg=self.subtext_fg, font=("Segoe UI", 9)).pack(side="left")

    def _draw_figure(self, fig, frame: tk.Widget) -> None:
        for child in frame.winfo_children():
            child.destroy()
        frame.update_idletasks()
        width = frame.winfo_width() or 640
        height = frame.winfo_height() or 360
        if width < 10:
            width = 640
        if height < 10:
            height = 360
        zoom = self.zoom_factor.get()
        fig.set_size_inches((width * zoom) / fig.dpi, (height * zoom) / fig.dpi)
        fig.tight_layout(pad=0.8)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh(self) -> None:
        try:
            plt.close("all")
            
            # Validar que total_carriers sea divisible por cluster_size
            total_carriers = self.total_carriers.get()
            cluster_size = self.cluster_size.get()
            
            if total_carriers % cluster_size != 0:
                print(f"⚠ Portadoras ({total_carriers}) debe ser divisible por Clúster ({cluster_size})")
                self.metric_doppler.set("—")
                self.metric_coherence.set("—")
                self.metric_stability.set("Error de configuración")
                return
            
            gsm = GSMConfig(carrier_frequency_hz=self.fc_mhz.get() * 1e6, timeslot_duration_s=self.timeslot_us.get() * 1e-6)
            convoy = ConvoyScenario(speeds_kmh=(self.speed_low.get(), self.speed_high.get()))
            camp = CampScenario(total_carriers=total_carriers, cluster_size=cluster_size, cell_radius_km=self.radius_km.get())
            analyzer = AnalyzerConfig(noise_figure_db=self.nf_db.get())

            print(f"Analizando: GSM {self.fc_mhz.get()} MHz, Velocidades {self.speed_low.get()}-{self.speed_high.get()} km/h...")
            
            mobility = analyze_convoy_mobility(convoy, gsm)
            fading_summary, traces = analyze_convoy_fading(convoy, gsm)
            camp_results = analyze_camp_base(camp, gsm, analyzer)

            try:
                speed = int(self.speed_profile.get())
            except (ValueError, tk.TclError):
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
            self.doppler_value.set(f"{selected_row['max_doppler_hz']:.0f} Hz")
            self.coherence_value.set(f"{selected_row['coherence_time_ms']:.2f} ms")
            self.velocity_main.set(f"{speed} km/h")
            self.velocity_sub.set(f"{self.speed_low.get():.0f} km/h")
            self.frequency_value.set(f"{self.fc_mhz.get():.3f} MHz")
            self.bandwidth_value.set("200 kHz")

            print("Dibujando figuras...")
            self._draw_figure(figure_doppler_coherence(mobility), self.main_chart_frame)
            self._draw_figure(figure_timeslot_signal(selected_trace), self.side_chart_top)
            self._draw_figure(figure_noise(camp_results["rbw_noise"]), self.side_chart_bottom)
            self._draw_figure(figure_cluster_map(), self.bottom_chart_1)
            self._draw_figure(figure_reuse_distance(camp_results["frequency_planning"]), self.bottom_chart_2)
            self._draw_figure(
                figure_carrier_distribution(camp_results["frequency_planning"], camp_results["logical_channels"]),
                self.diagram_frame,
            )
            
            print("✓ Actualización completada exitosamente")
            
        except Exception as e:
            print(f"✗ Error: {type(e).__name__}: {e}")
            self.metric_doppler.set("Error")
            self.metric_coherence.set("Error")
            self.metric_stability.set("Error")


def main() -> None:
    app = TitanGuiApp()
    app.mainloop()


if __name__ == "__main__":
    main()
