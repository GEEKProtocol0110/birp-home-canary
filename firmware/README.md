# Firmware implementation plan

No device firmware is implemented yet. The browser demo is illustrative only.

Implement against [control spec draft 0.1](../docs/control-spec-v0.1.md).

Suggested boundaries:

1. Sensor adapters expose readiness, accepted sample, units, quality, timestamp, and fault.
2. State engine classifies channels independently using validated configuration and a monotonic clock.
3. Aggregator preserves known elevated readings and identifies unavailable channels.
4. Output layer renders cause, status, and halo without blocking sensing.
5. Motion layer references position, enforces physical limits, and animates without blocking.

The first implementation must not contain guessed production thresholds or raw motor values presented as calibrated bird angles. Add meaningful state-engine tests when implementing the engine, and hardware measurements when integrating actuators.
