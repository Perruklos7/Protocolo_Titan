from pathlib import Path

from .config import GSMConfig, ConvoyScenario, CampScenario, AnalyzerConfig
from .radio_access import gsm_access_summary
from .scenario_a import analyze_convoy_mobility, analyze_convoy_fading
from .scenario_b import analyze_camp_base
from .plots import (
    save_doppler_plot,
    save_coherence_plot,
    save_fading_plot,
    save_reuse_plot,
    save_noise_plot,
)
from .report import write_markdown_report


def main() -> None:
    project_root = Path.cwd()
    outputs = project_root / "outputs"
    figures = outputs / "figures"
    outputs.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    gsm = GSMConfig()
    convoy = ConvoyScenario()
    camp = CampScenario()
    analyzer = AnalyzerConfig()

    access = gsm_access_summary(gsm)
    mobility = analyze_convoy_mobility(convoy, gsm)
    fading_summary, traces = analyze_convoy_fading(convoy, gsm)
    camp_results = analyze_camp_base(camp, gsm, analyzer)

    access.to_csv(outputs / "gsm_fdma_tdma_resumen.csv", index=False)
    mobility.to_csv(outputs / "escenario_a_movilidad.csv", index=False)
    fading_summary.to_csv(outputs / "escenario_a_fading_metricas.csv", index=False)
    camp_results["frequency_planning"].to_csv(outputs / "escenario_b_planificacion.csv", index=False)
    camp_results["logical_channels"].to_csv(outputs / "escenario_b_canales_logicos.csv", index=False)
    camp_results["rbw_noise"].to_csv(outputs / "certificacion_rbw.csv", index=False)
    camp_results["red_checklist"].to_csv(outputs / "certificacion_red_checklist.csv", index=False)

    save_doppler_plot(mobility, figures / "escenario_a_doppler.png")
    save_coherence_plot(mobility, figures / "escenario_a_coherencia_vs_timeslot.png")
    save_reuse_plot(camp_results["frequency_planning"], figures / "escenario_b_reutilizacion.png")
    save_noise_plot(camp_results["rbw_noise"], figures / "certificacion_rbw_ruido.png")

    for name, trace in traces.items():
        trace.to_csv(outputs / f"traza_{name}.csv", index=False)
        save_fading_plot(trace, figures / f"traza_{name}.png")

    write_markdown_report(
        outputs / "informe_resultados.md",
        mobility=mobility,
        fading_metrics=fading_summary,
        frequency_planning=camp_results["frequency_planning"],
        logical_channels=camp_results["logical_channels"],
        rbw_noise=camp_results["rbw_noise"],
    )

    print("\n=== Resumen FDMA/TDMA ===")
    print(access.to_string(index=False))

    print("\n=== Escenario A: movilidad ===")
    print(mobility.to_string(index=False))

    print("\n=== Escenario A: fading ===")
    print(fading_summary.to_string(index=False))

    print("\n=== Escenario B: planificación ===")
    print(camp_results["frequency_planning"].to_string(index=False))

    print("\n=== Escenario B: canales lógicos ===")
    print(camp_results["logical_channels"].head(12).to_string(index=False))

    print("\n=== Certificación: RBW ===")
    print(camp_results["rbw_noise"].to_string(index=False))

    print(f"\nResultados exportados en: {outputs.resolve()}")


if __name__ == "__main__":
    main()
