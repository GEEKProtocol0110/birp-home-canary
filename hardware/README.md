# Hardware planning

No final bill of materials or electrical schematic exists in this package.

| Subsystem | Candidate direction | Evidence needed |
| --- | --- | --- |
| Controller | ESP32-S3 | Pin budget, driver feasibility, power budget |
| CO₂ | Model unselected | Actual CO₂ measurement method, units, readiness, limits, calibration |
| PM2.5 | Model unselected | Airflow needs, readiness, cadence, maintenance |
| Temperature/humidity | Model unselected | Accuracy, placement, self-heating effects |
| Bird motion | Magnetic track or linkage | Torque/travel, clearance, position reference, failure behavior |
| Halo/display | Halo LEDs and round display | Visibility, current draw, dimensions |
| Power | USB-C direction | Supply and protection requirements |
| Enclosure | Approximately 127 mm circular concept | Air path, sensor isolation, access, fit |

Select parts only after reviewing their current manufacturer documentation. Record exact part numbers and revision-specific evidence. Do not wire from this planning table.
