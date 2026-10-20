# BIRP — The Home Canary™

**A little bird. A clearer picture.**

[Visit the BIRP website](https://birp-home-canary.oolongee.chatgpt.site) · [Read the control specification](docs/control-spec-v0.1.md) · [See the roadmap](docs/ROADMAP.md)

BIRP is a home environmental-monitor concept that expresses room conditions through a moving bird, a light halo, and a simple display.

**Stage: concept / prototype specification.** This repository contains documentation and a working browser demonstration. It does not yet contain functioning device firmware, validated electronics, CAD, or physical test results.

## Start here

- [Project status and next step](docs/STATUS.md)
- [v1 control specification](docs/control-spec-v0.1.md)
- [Development roadmap](docs/ROADMAP.md)
- [Hardware planning](hardware/README.md)
- [Firmware implementation plan](firmware/README.md)
- [Contribution guide](CONTRIBUTING.md)

## The first version

CO₂, PM2.5, temperature, humidity, moving bird, halo, and readable display. The focused version excludes camera, intercom, and subscriptions. Air-quality classification thresholds have not been selected or validated.

## Run the website

No build or package installation is required. From the repository root:

```bash
python3 -m http.server 8080 --directory website
```

Open http://localhost:8080. The four state buttons simulate bird poses and halo colors; they do not read sensors or implement the firmware state engine.

## Repository map

| Directory | Purpose |
| --- | --- |
| `docs/` | Specification, roadmap, decisions, and handoff status |
| `hardware/` | Hardware candidates and evidence required before selection |
| `firmware/` | Firmware boundaries and next implementation milestone |
| `website/` | Static promotional site and simulated bird demo |
| `.github/` | Issue templates for documented work |

## Current milestone

Prove one measured bench loop: sensor readings → classification → visible cause → bounded bird movement → recovery. See the control specification for planned acceptance cases.

## Project scope

BIRP is in development, not a certified emergency alarm. This version does not detect carbon monoxide or replace smoke or CO alarms. Product imagery and browser behavior are conceptual.

## Rights

No open-source license has been selected. Public visibility does not grant an open-source license. Project naming and marks remain with their respective rights holders; no patent or trademark registration claim is made here.
