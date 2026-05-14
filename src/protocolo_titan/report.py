from pathlib import Path
import pandas as pd


def write_markdown_report(
    output_path: Path,
    mobility: pd.DataFrame,
    fading_metrics: pd.DataFrame,
    frequency_planning: pd.DataFrame,
    logical_channels: pd.DataFrame,
    rbw_noise: pd.DataFrame,
) -> None:
    """Genera un resumen Markdown que puede usarse como base del informe."""
    lines = []
    lines.append("# Informe de resultados — Protocolo Titán")
    lines.append("")
    lines.append("## Escenario A — Convoy de alta velocidad")
    lines.append("")
    lines.append(mobility.to_markdown(index=False))
    lines.append("")
    lines.append("Interpretación: el criterio principal es comparar el tiempo de coherencia con el timeslot GSM de 577 µs.")
    lines.append("")
    lines.append("### Métricas de fading")
    lines.append("")
    lines.append(fading_metrics.to_markdown(index=False))
    lines.append("")
    lines.append("## Escenario B — Campamento base")
    lines.append("")
    lines.append("### Planificación de frecuencias")
    lines.append("")
    lines.append(frequency_planning.to_markdown(index=False))
    lines.append("")
    lines.append("### Canales lógicos y físicos")
    lines.append("")
    lines.append(logical_channels.to_markdown(index=False))
    lines.append("")
    lines.append("### Instrumentación y RBW")
    lines.append("")
    lines.append(rbw_noise.to_markdown(index=False))
    lines.append("")
    lines.append("## Conclusión técnica")
    lines.append("")
    lines.append(
        "El escenario A está dominado por movilidad, Doppler y variación temporal del canal. "
        "El escenario B está dominado por eficiencia espectral, reutilización de frecuencias, "
        "control de interferencia co-canal y criterio instrumental para medidas RED."
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")
