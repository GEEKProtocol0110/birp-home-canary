# BIRP — The Home Canary™

**A little bird. A clearer picture.**

[Visit the BIRP website](https://birp-home-canary.oolongee.chatgpt.site) · [Read the control specification](docs/control-spec-v0.2.md) · [See the roadmap](docs/ROADMAP.md)

BIRP is a home environmental-monitor concept that expresses room conditions through a physical bird traveling around a round display, a light halo, and a simple display.

**Stage: concept / prototype specification.** This repository contains documentation and a working browser demonstration. It does not yet contain functioning device firmware, validated electronics, CAD, or physical test results.

## Start here

- [Product vision](docs/PRODUCT_VISION.md)
- [Original-source reconciliation](docs/SOURCE_RECONCILIATION.md)
- [Minimal founder checklist](docs/FOUNDER_CHECKLIST.md)
- [One-page overview](docs/ONE_PAGE_OVERVIEW.md)
- [Project status and next step](docs/STATUS.md)
- [v1 control specification](docs/control-spec-v0.2.md)
- [Development roadmap](docs/ROADMAP.md)
- [Hardware planning](hardware/README.md)
- [Firmware implementation plan](firmware/README.md)
- [Contribution guide](CONTRIBUTING.md)

## The product and the first experiment

The founder specified a 5-inch round display with a physical bird moving around its perimeter: top represents better conditions and bottom worse conditions. Core standalone use must not require an app or subscription. The broader vision includes optional connected services, camera/video intercom functions, and room/master-unit networking.

A proposed first bench experiment focuses on CO₂, PM2.5, temperature/humidity, bird, halo, and display. That experiment is not the complete product or an approved removal of broader features. Hardware and classification thresholds remain unvalidated.

## Run the website

No build or package installation is required. From the repository root:

```bash
python3 -m http.server 8080 --directory website
```

Open http://localhost:8080. The four state buttons simulate perimeter bird positions and halo colors; they do not read sensors or implement the firmware state engine.

## Repository map

| Directory | Purpose |
| --- | --- |
| `docs/` | Specification, roadmap, decisions, and handoff status |
| `hardware/` | Hardware candidates and evidence required before selection |
| `firmware/` | Firmware boundaries and next implementation milestone |
| `website/` | Static promotional site and simulated bird demo |
| `.github/` | Issue templates for documented work |

## Current milestone

Complete the low-cost founder/partner packet and choose one initial use case. A partner-supported bench loop follows: sensor readings → classification → visible cause → bounded perimeter movement → recovery. See the control specification for planned acceptance cases.

## Project scope

BIRP is in development, not a certified emergency alarm. This version does not detect carbon monoxide or replace smoke or CO alarms. Product imagery and browser behavior are conceptual.

## Rights

No open-source license has been selected. Public visibility does not grant an open-source license. Project naming and marks remain with their respective rights holders; no patent or trademark registration claim is made here.
