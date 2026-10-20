# Hardware planning

No final bill of materials or electrical schematic exists in this package.

| Subsystem | Candidate direction | Evidence needed |
| --- | --- | --- |
| Controller | ESP32-S3 | Pin budget, driver feasibility, power budget |
| CO₂ | Model unselected | Actual CO₂ measurement method, units, readiness, limits, calibration |
| PM2.5 | Model unselected | Airflow needs, readiness, cadence, maintenance |
| Temperature/humidity | Model unselected | Accuracy, placement, self-heating effects |
| Bird motion | Perimeter carrier with magnetic coupling or another referenced drive | Torque over the full orbit, gravity loading, clearance, position reference, failure behavior |
| Halo/display | Halo LEDs and round display | Visibility, current draw, dimensions |
| Power | USB-C direction | Supply and protection requirements |
| Enclosure | Round enclosure around requested 5-inch display; diameter open | Air path, sensor isolation, access, fit |

Select parts only after reviewing their current manufacturer documentation. Record exact part numbers and revision-specific evidence. Do not wire from this planning table.

The display size and enclosure size are independent. A simple body-tilting servo does not demonstrate the requested perimeter movement. Camera/audio and multi-room requirements remain in PRODUCT_VISION; they need a separate architecture review before any final identical-hardware commitment.
