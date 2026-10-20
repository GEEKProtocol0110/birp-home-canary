# Builder handoff

Read `docs/PRODUCT_VISION.md`, `docs/SOURCE_RECONCILIATION.md`, `docs/STATUS.md`, `docs/DECISIONS.md`, and `docs/control-spec-v0.2.md` before implementation.

- Preserve the founder's signature perimeter movement: top is better, bottom is worse. Orbital position and body tilt are independent.
- The sensor-only scope is a proposed first experiment, not the whole product. Preserve broader camera/intercom and optional-service requirements in PRODUCT_VISION.
- Core standalone use must not require an app or subscription.
- Prioritize the low-cost founder/partner packet before resource-dependent hardware work.
- Label proposed behavior, simulated data, and unverified hardware clearly.
- Do not claim functioning firmware, physical validation, certification, or production readiness without evidence.
- Keep classification thresholds unassigned until a documented policy is reviewed.
- Do not show CALM for missing air-quality readings.
- Keep sensor processing nonblocking and enforce physical motion limits.
- Update STATUS, decisions, and roadmap when work changes their claims.
- Website source lives in `website/`; hosted publication is a separate step. See STATUS for the live URL.
- No open-source license has been selected; do not add one without an owner decision.
