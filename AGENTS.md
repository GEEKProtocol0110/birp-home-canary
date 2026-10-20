# Builder handoff

Read `docs/STATUS.md`, `docs/DECISIONS.md`, and `docs/control-spec-v0.1.md` before implementation.

- Preserve the focused v1 scope: CO₂, PM2.5, temperature, humidity, moving bird, halo, simple display.
- Label proposed behavior, simulated data, and unverified hardware clearly.
- Do not claim functioning firmware, physical validation, certification, or production readiness without evidence.
- Keep classification thresholds unassigned until a documented policy is reviewed.
- Do not show CALM for missing air-quality readings.
- Keep sensor processing nonblocking and enforce physical motion limits.
- Update STATUS, decisions, and roadmap when work changes their claims.
- Website source lives in `website/`; hosted publication is a separate step. See STATUS for the live URL.
- No open-source license has been selected; do not add one without an owner decision.
