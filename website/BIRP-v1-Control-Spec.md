# BIRP — The Home Canary™

## v1 control specification · draft 0.2 · October 20, 2026

**Purpose:** translate measured room conditions into an understandable bird pose, halo, and display. This document turns the earlier motion concept into a proposed firmware contract. It is a specification, not tested firmware or a completed hardware design.

## Scope and provenance

This revision follows a direct review of the founder's two shared conversations. See [source reconciliation](https://github.com/GEEKProtocol0110/birp-home-canary/blob/main/docs/SOURCE_RECONCILIATION.md) and [product vision](https://github.com/GEEKProtocol0110/birp-home-canary/blob/main/docs/PRODUCT_VISION.md).

The founder's signature design is a **physical bird traveling around a 5-inch round display**, with top representing better conditions and bottom worse conditions. Core use must not require an app or subscription. Camera/intercom, optional services, and a multi-room/master-unit system remain in the broader vision.

The sensor-only CO₂/PM2.5/temperature/humidity build is a proposed first bench experiment, not an approved removal of those broader features. This control contract covers that limited experiment. ESP32-S3, USB-C, magnetic coupling, and display resolution remain candidates. Five inches describes the requested display, not a validated enclosure diameter.

The earlier invention PDF remains unrecovered. Two original reference images were subsequently supplied; see the asset register. Those illustrations are conceptual, not mechanical validation. The original motion examples are assistant proposals and mix body tilt with dial-position language. This draft separates those coordinates. State logic, timings, and orbital presets below are new proposals, not physical test results.

## User experience

- **Calm:** bird at the top of the perimeter; teal halo; readings visible.
- **Attention:** bird moves partway downward; amber halo; display identifies the cause.
- **High:** bird at the lower perimeter; red halo; display identifies the cause.
- **Unavailable:** violet halo and explicit missing-reading message; retain the last referenced position if possible, without presenting it as a current reading.
- **Recovery:** bird returns toward the top after qualified improvement.

“High” is a prototype tier, not a certified emergency alarm. This experiment does not include smoke or carbon-monoxide detection.

## Separate three kinds of state

| Layer | Values | Purpose |
| --- | --- | --- |
| Measurement | UNAVAILABLE, CALM, ATTENTION, HIGH | Separate classification for each air-quality channel |
| Device health | STARTING, READY, DEGRADED, FAULT, SETUP_REQUIRED | Whether required sensors and configuration are usable |
| Motion | HOLD, IDLE, ATTENTION_MOVE, HIGH_MOVE, RECOVERY_MOVE, DISABLED | How the actuator expresses a known condition |

Keep temperature and humidity visible as measurements. Do not assign them air-quality tiers until a separate comfort policy is defined. Never average CO₂ and PM2.5 into one number that could hide an elevated channel.

## Required configuration

Each CO₂ and PM2.5 channel requires its own thresholds and durations:

| Field | Meaning |
| --- | --- |
| attention_enter / attention_exit | Threshold to enter attention and lower threshold to clear it |
| high_enter / high_exit | Threshold to enter high and lower threshold to clear it |
| rise_hold_ms | Continuous eligible time before an upward transition |
| clear_hold_ms | Continuous eligible time before a downward transition |
| stale_after_ms | Maximum age of a usable reading |
| startup_ready_rule | Readiness rule specific to the chosen sensor |
| valid_range / quality_rule | Sensor-specific criteria for accepting a sample |

Threshold values are deliberately **unassigned**. Units must be ppm for CO₂ and µg/m³ for PM2.5. Validate units, finite numbers, positive durations, and this ordering before enabling classification:

`attention_exit < attention_enter < high_exit < high_enter`

This ordering is a proposed simple two-tier hysteresis policy. Alternative bands require an explicit policy revision. Missing or invalid configuration produces SETUP_REQUIRED, not CALM. A build with unassigned thresholds may exercise motion using labeled simulated input only.

Sensor readiness, cadence, limits, and staleness must be set from the selected manufacturer's documentation and verified on the bench. No specific sensor model is selected by this specification.

## Channel transition rules

Use a monotonic clock. Evaluate sample age on every control tick, including when no new sample arrives. Use the latest accepted reading only while it remains fresh. Invalid new samples make that channel unavailable immediately; they must not extend the age of the last accepted sample.

| Current channel state | Condition held continuously | Next state |
| --- | --- | --- |
| UNAVAILABLE | Ready, valid, fresh samples for the startup rule | Classify as described below |
| CALM | Value ≥ high_enter for rise_hold_ms | HIGH |
| CALM | Value ≥ attention_enter for rise_hold_ms | ATTENTION, unless HIGH qualifies on that tick |
| ATTENTION | Value ≥ high_enter for rise_hold_ms | HIGH |
| ATTENTION | Value < attention_exit for clear_hold_ms | CALM |
| HIGH | Value < high_exit for clear_hold_ms | ATTENTION |
| Any | Invalid sample, stale reading, sensor fault, or loss of readiness | UNAVAILABLE |

On first readiness, a value at or above high_enter becomes HIGH; otherwise a value at or above attention_enter becomes ATTENTION; otherwise CALM. Readiness itself is the startup qualification, so an elevated initial reading does not wait for a second rise timer.

HIGH clears one tier at a time. Begin a new attention-clear timer after entering ATTENTION; do not reuse the high-clear timer. A condition becoming false resets its timer. Unavailability resets all qualification timers. On reacquisition, apply startup qualification again.

## Aggregation and output priority

1. Classify each configured air-quality channel independently.
2. If any available channel is HIGH, express HIGH and show its cause.
3. Otherwise, if any available channel is ATTENTION, express ATTENTION and show its cause.
4. Express CALM only when both required air-quality channels are available and CALM.
5. With no elevated channel and any required air-quality channel unavailable, express UNAVAILABLE.

If an elevated channel is known while another sensor has failed, retain the elevated pose and color, and add the sensor fault on the display. Known concern must remain visible. A missing temperature or humidity reading adds a degraded-status message but does not erase known air-quality results.

STARTING applies while required sensors complete readiness. READY requires all required measurements. DEGRADED applies when some required measurements are unavailable; FAULT applies when none are available after startup. SETUP_REQUIRED takes precedence when classification configuration is invalid. Display each channel's status so a fault cannot be mistaken for a low measurement.

## Bird motion contract

The main coordinate is **orbital position**, measured clockwise from 12 o'clock: 0° top, 90° right, 180° bottom. These angles describe display-relative indicator position, not motor commands. Mechanism selection must establish direction, travel, homing, clearance, gravity loading, and the position-to-actuator mapping. The 90° intermediate state is a new demo preset; the founder specified only the top/bottom semantics.

| Output | Proposed orbital position | Proposed movement duration |
| --- | --- | --- |
| CALM | 0° / top | Hold after recovery |
| ATTENTION | 90° / right | 2,200 ms from current position |
| HIGH | 180° / bottom | 1,700 ms from current position |
| Recovery to CALM | 0° / top | 2,700 ms, after aggregate CALM qualifies and remains stable another 5 seconds |
| UNAVAILABLE | Retain last referenced position; do not home automatically | Cancel decorative motion; stop safely under the chosen mechanism's fault policy |

These durations are conceptual; do not attempt them on hardware before measuring required speed, torque, limits, and clearance. Use easing without overshoot for the first bench build. Known HIGH/ATTENTION still takes priority over a different unavailable channel, as defined in aggregation.

At power-up, actual position is unknown. Disable movement until a mechanism-appropriate reference procedure succeeds. During a motion fault, do not repeatedly attempt homing. Continue independent sensor, halo, and display processing. A held bird position during a sensor fault must be identified as a previous position, never a current all-clear signal.

### Historical body-motion proposals

The original assistant suggested calm micro-tilts of 1.5–2.5°, warning tilts of 8–15°, stronger tilts of 20–40°, and a curiosity gesture of 4–8°. It also proposed overshoot, chirps, and night-mode variations. These were not calibrated orbital coordinates. Body tilt, curiosity sensing, sound, and idle animation are deferred; they require separate design and must not obscure the main perimeter indicator.

Move once per qualified output transition, then hold. Higher concern preempts recovery immediately. Replan from the current commanded position. Update halo and cause text immediately. Every animation must be nonblocking and bounded by validated mechanical travel.

The browser demonstration switches among illustrative targets; it does not implement sensor qualification, a motor driver, or the full recovery timer. Missing-reading mode holds its last illustrated location and explicitly labels that location as historical.

## Control-loop pseudocode

```text
on_control_tick(now):
    config_ok = validate_configuration()
    samples = ingest_sensor_events_without_blocking()

    for each required sensor:
        update_readiness_and_validity(sensor, samples, now)
        expire_stale_reading(sensor, now)

    if not config_ok:
        reset_classification_timers()
        output = UNAVAILABLE
        health = SETUP_REQUIRED
    else:
        for channel in [CO2, PM25]:
            advance_channel_state_and_timers(channel, now)
        output = aggregate_air_quality_channels()
        health = derive_device_health()

    update_display(output, health, readings, per_sensor_status)
    update_halo(output, health)
    update_motion_target_on_transition(output, health, now)
    advance_bounded_animation_if_calibrated(now)
```

Sensor I/O, display work, and actuator work need bounded execution times. Watchdog and error handling must avoid a loop in which a failed peripheral prevents freshness checks. Confirm feasibility against the final hardware and drivers.

## Acceptance scenarios for implementation

These are planned verification cases; no firmware or physical test has run.

| Scenario | Required result |
| --- | --- |
| Boot without thresholds | SETUP_REQUIRED; no reassuring calm status |
| Boot while sensors become ready | STARTING; no decorative motion |
| A short threshold crossing | No upward transition before rise qualification |
| Persistent elevated CO₂ with low PM2.5 | Attention/high based on CO₂; display names CO₂ |
| Persistent elevated PM2.5 with low CO₂ | Attention/high based on PM2.5; display names PM2.5 |
| Oscillation near a threshold | Hysteresis and continuous timers prevent rapid state changes |
| One sensor stale, other calm | UNAVAILABLE output with a specific sensor message |
| One sensor stale, other high | HIGH output plus degraded-status message |
| Invalid sample arrives | Channel becomes unavailable and timers reset |
| Sensor reconnects while elevated | Startup qualification, then appropriate elevated state |
| HIGH clears | ATTENTION first; independent calm qualification follows |
| Concern appears during idle/recovery | Concern preempts motion; target starts at current position |
| Device resets without position reference | Motion disabled until successful referencing |
| Mechanical limit would be exceeded | Clamp or reject command; record fault; no repeated forcing |
| Actuator fails | Readings, halo, and display continue with motion-fault status |

## Next build milestone

Prove one complete bench loop: **sensor readings → channel states → visible cause → bounded perimeter bird motion → qualified recovery**.

Before claiming this milestone, select and document the sensor models and motion mechanism, establish electrical and mechanical limits, populate and review the classification policy, implement the loop, and execute the acceptance scenarios. Keep hardware receipts, firmware version, configuration version, and measured results together so another builder can reproduce the demonstration.
