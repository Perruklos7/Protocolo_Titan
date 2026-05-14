# Protocolo Titán — GSM/EDGE, movilidad, planificación y certificación

Este repositorio implementa una práctica reproducible para el reto **Protocolo Titán**. El objetivo es analizar una red GSM/EDGE táctica en dos escenarios de operación con desafíos opuestos:

- **Escenario A — Convoy de alta velocidad**: despliegue lineal en una vía férrea que cruza un valle, con celdas de 3 km y velocidades de 50 km/h y 250 km/h. El análisis se centra en Doppler, tiempo de coherencia y estabilidad del canal durante un timeslot GSM de 577 µs.
- **Escenario B — Campamento base**: entorno denso con equipos de rescate, celdas de 1,5 km, 24 portadoras y clúster de planificación N = 4. El análisis se centra en eficiencia espectral, reutilización celular, interferencia co-canal, asignación BCCH/TCH y certificación/instrumentación.

El código está pensado para que el alumno pueda entregar tablas, gráficas, simulaciones sencillas y anexos de cálculo.

---

## 1. Instalación

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 2. Ejecución completa

```bash
python -m protocolo_titan.main
```

Si ejecutas desde la raíz del repositorio y Python no encuentra el paquete:

```bash
set PYTHONPATH=src
python -m protocolo_titan.main
```

En Linux/macOS:

```bash
export PYTHONPATH=src
python -m protocolo_titan.main
```

---

## 3. Dashboard opcional

```bash
streamlit run src/protocolo_titan/streamlit_app.py
```

La interfaz Streamlit ha sido rediseñada para ofrecer una visualización tipo **mission control dashboard**, inspirada en un panel de analítica ferroviaria y RF:

- **Escenario A · Physics & Spectrum**: tarjetas de capa física, Doppler/coherencia, señal temporal y telemetría GSM.
- **Escenario B · Base Camp**: mapa de clúster N=4, distribución BCCH/TCH, panel de planificación celular, espectro y checklist RED.

La interfaz Streamlit ha sido rediseñada para ofrecer una visualización tipo **mission control dashboard**, inspirada en un panel de analítica ferroviaria y RF: 

- **Escenario A · Physics & Spectrum**: tarjetas de capa física, Doppler/coherencia, señal temporal y telemetría GSM.
- **Escenario B · Base Camp**: mapa de clúster N=4, distribución BCCH/TCH, panel de planificación celular, espectro y checklist RED.

---

## 4. Notebook docente

```bash
jupyter notebook notebooks/protocolo_titan_replanteado.ipynb
```

---

## 5. Estructura del repositorio

```text
protocolo_titan_replanteado/
├── README.md
├── requirements.txt
├── pyproject.toml
├── docs/
│   └── guia_uso_docente.md
├── notebooks/
│   └── protocolo_titan_replanteado.ipynb
├── outputs/
│   ├── escenario_a_movilidad.csv
│   ├── escenario_a_fading_metricas.csv
│   ├── escenario_b_planificacion.csv
│   ├── escenario_b_canales_logicos.csv
│   ├── certificacion_rbw.csv
│   └── figures/
├── src/
│   └── protocolo_titan/
│       ├── __init__.py
│       ├── config.py
│       ├── radio_access.py
│       ├── propagation.py
│       ├── scenario_a.py
│       ├── cellular_planning.py
│       ├── instrumentation.py
│       ├── scenario_b.py
│       ├── plots.py
│       ├── report.py
│       ├── main.py
│       └── streamlit_app.py
└── tests/
    └── test_core.py
```

---

## 6. Fórmulas principales

### Acceso GSM

- FDMA: portadoras de 200 kHz.
- TDMA: 8 timeslots por trama.
- Timeslot GSM utilizado en la práctica: 577 µs.

### Doppler máximo

```text
f_d = v · f_c / c
```

### Tiempo de coherencia

```text
T_c ≈ 0.423 / f_d
```

### Distancia de reutilización

```text
D / R = sqrt(3N)
D = R · sqrt(3N)
```

### Suelo de ruido instrumental

```text
N(dBm) = -174 dBm/Hz + 10 log10(RBW) + NF
```

---

## 7. Resultados esperados con parámetros base

| Parámetro | Resultado |
|---|---:|
| Doppler a 50 km/h, 900 MHz | 41,67 Hz |
| Tiempo de coherencia a 50 km/h | 10,15 ms |
| Doppler a 250 km/h, 900 MHz | 208,33 Hz |
| Tiempo de coherencia a 250 km/h | 2,03 ms |
| Timeslot GSM | 0,577 ms |
| Portadoras por celda en N=4 | 6 |
| Distancia de reutilización con R=1,5 km y N=4 | 5,20 km |
| Suelo de ruido con RBW=100 kHz y NF=6 dB | -118 dBm |
| Suelo de ruido con RBW=10 kHz y NF=6 dB | -128 dBm |
| Suelo de ruido con RBW=1 kHz y NF=6 dB | -138 dBm |

---

## 8. Uso docente sugerido

1. Ejecutar `main.py`.
2. Revisar las tablas CSV generadas.
3. Abrir el notebook para interpretar resultados.
4. Modificar parámetros:
   - frecuencia central;
   - velocidades;
   - radio de celda;
   - número de portadoras;
   - tamaño del clúster;
   - RBW;
   - figura de ruido.
5. Incorporar gráficas y tablas al informe IMRyD ampliado.
