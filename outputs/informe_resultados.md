# Informe de resultados — Protocolo Titán

## Escenario A — Convoy de alta velocidad

| scenario                |   cell_radius_km |   speed_kmh |   speed_ms |   carrier_frequency_mhz |   max_doppler_hz |   coherence_time_ms |   gsm_timeslot_ms |   coherence_to_timeslot_ratio | stability_class             |
|:------------------------|-----------------:|------------:|-----------:|------------------------:|-----------------:|--------------------:|------------------:|------------------------------:|:----------------------------|
| A_convoy_alta_velocidad |                3 |          50 |    13.8889 |                     900 |          41.6667 |             10.152  |             0.577 |                      17.5945  | cuasiestatico               |
| A_convoy_alta_velocidad |                3 |         250 |    69.4444 |                     900 |         208.333  |              2.0304 |             0.577 |                       3.51889 | estable_con_margen_reducido |

Interpretación: el criterio principal es comparar el tiempo de coherencia con el timeslot GSM de 577 µs.

### Métricas de fading

| model    |   doppler_hz |   envelope_min |   envelope_max |   envelope_std |   relative_peak_to_peak |   speed_kmh |   coherence_time_ms | stability_class             |
|:---------|-------------:|---------------:|---------------:|---------------:|------------------------:|------------:|--------------------:|:----------------------------|
| rayleigh |      41.6667 |     0.00894961 |        3.32166 |       0.586993 |                3.31271  |          50 |             10.152  | cuasiestatico               |
| rician   |      41.6667 |     0.734056   |        1.25486 |       0.100871 |                0.5208   |          50 |             10.152  | cuasiestatico               |
| rayleigh |     208.333  |     0.145474   |        3.0415  |       0.453328 |                2.89602  |         250 |              2.0304 | estable_con_margen_reducido |
| rician   |     208.333  |     0.694197   |        1.2311  |       0.105082 |                0.536901 |         250 |              2.0304 | estable_con_margen_reducido |

## Escenario B — Campamento base

### Planificación de frecuencias

| scenario          | cell   |   cell_radius_km |   cluster_size_N |   total_carriers |   carriers_per_cell | arfcn_range   | arfcn_list             |   reuse_ratio_D_over_R |   reuse_distance_km |
|:------------------|:-------|-----------------:|-----------------:|-----------------:|--------------------:|:--------------|:-----------------------|-----------------------:|--------------------:|
| B_campamento_base | A      |              1.5 |                4 |               24 |                   6 | 1-6           | 1, 2, 3, 4, 5, 6       |                 3.4641 |             5.19615 |
| B_campamento_base | B      |              1.5 |                4 |               24 |                   6 | 7-12          | 7, 8, 9, 10, 11, 12    |                 3.4641 |             5.19615 |
| B_campamento_base | C      |              1.5 |                4 |               24 |                   6 | 13-18         | 13, 14, 15, 16, 17, 18 |                 3.4641 |             5.19615 |
| B_campamento_base | D      |              1.5 |                4 |               24 |                   6 | 19-24         | 19, 20, 21, 22, 23, 24 |                 3.4641 |             5.19615 |

### Canales lógicos y físicos

| cell   |   arfcn | carrier_role      | frequency_hopping_recommended   | power_policy          |   available_timeslots | engineering_note                                                             |
|:-------|--------:|:------------------|:--------------------------------|:----------------------|----------------------:|:-----------------------------------------------------------------------------|
| A      |       1 | BCCH/CCCH control | False                           | fixed/stable          |                     8 | BCCH debe ser detectable y estable para camping, sincronización y control.   |
| A      |       2 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| A      |       3 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| A      |       4 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| A      |       5 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| A      |       6 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| B      |       7 | BCCH/CCCH control | False                           | fixed/stable          |                     8 | BCCH debe ser detectable y estable para camping, sincronización y control.   |
| B      |       8 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| B      |       9 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| B      |      10 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| B      |      11 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| B      |      12 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| C      |      13 | BCCH/CCCH control | False                           | fixed/stable          |                     8 | BCCH debe ser detectable y estable para camping, sincronización y control.   |
| C      |      14 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| C      |      15 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| C      |      16 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| C      |      17 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| C      |      18 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| D      |      19 | BCCH/CCCH control | False                           | fixed/stable          |                     8 | BCCH debe ser detectable y estable para camping, sincronización y control.   |
| D      |      20 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| D      |      21 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| D      |      22 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| D      |      23 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |
| D      |      24 | TCH traffic       | True                            | adaptive if supported |                     8 | TCH transporta tráfico; puede beneficiarse de hopping y control de potencia. |

### Instrumentación y RBW

|   rbw_hz |   rbw_khz |   noise_figure_db |   noise_floor_dbm |   delta_vs_100khz_db | measurement_interpretation                              |
|---------:|----------:|------------------:|------------------:|---------------------:|:--------------------------------------------------------|
|   100000 |       100 |                 6 |              -118 |                    0 | RBW ancho: medida rápida, más ruido integrado.          |
|    10000 |        10 |                 6 |              -128 |                  -10 | RBW estrecho: menor ruido integrado, barrido más lento. |
|     1000 |         1 |                 6 |              -138 |                  -20 | RBW estrecho: menor ruido integrado, barrido más lento. |

## Conclusión técnica

El escenario A está dominado por movilidad, Doppler y variación temporal del canal. El escenario B está dominado por eficiencia espectral, reutilización de frecuencias, control de interferencia co-canal y criterio instrumental para medidas RED.