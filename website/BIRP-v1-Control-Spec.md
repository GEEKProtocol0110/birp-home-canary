# BIRP — The Home Canary™

## v1 control specification · draft 0.1 · October 20, 2026

**Purpose:** translate measured room conditions into an understandable bird pose, halo, and display. This document turns the earlier motion concept into a proposed firmware contract. It is a specification, not tested firmware or a completed hardware design.

## Scope and provenance

The recovered March 2026 direction focused v1 on CO₂, PM2.5, temperature, humidity, a moving bird, halo lighting, and a simple display. Camera, intercom, and subscriptions were excluded from that version.

The earlier enclosure concept was approximately 5 inches / 127 mm across, with an ESP32-S3, round display, USB-C power, and a magnetic bird mechanism. These are design candidates; exact parts, mechanical travel, power budget, and pin assignments remain unverified.

The original invention brief was not located during this session. Earlier motion values below were recovered from conversation context. All state logic and timing defaults added here are new proposals.

## User experience

- **Calm:** bird upright; steady teal halo; actual readings visible.
- **Attention:** bird leans; amber halo; display identifies the measurement responsible.
- **High:** deeper lean; slow red halo pulse; display identifies the elevated measurement.
- **Unavailable:** neutral bird pose where mechanically possible; violet halo; plain-language sensor status. Never label unknown readings “good.”
- **Recovery:** bird returns gently after readings have remained below the applicable clearing thresholds.

“High” is a prototype air-quality tier, not a certified emergency alarm. This v1 scope does not include a carbon-monoxide sensor. Product copy and labeling must match that scope.

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

Angles are conceptual bird lean relative to the upright pose, **not raw motor commands**. A magnetic track or linkage needs a calibrated mapping from pose to actuator position. Mechanical travel limits override every animation, including overshoot.

| Motion | Recovered concept | Proposed deterministic prototype setting |
| --- | --- | --- |
| Calm | 0° upright | Hold 0° |
| Idle | 1.5–2.5° every 45–90 seconds | 2° and return; one cycle every 60 seconds |
| Attention | +8–15°, 1,800–2,600 ms; 2° overshoot | +12° over 2,200 ms; overshoot disabled initially |
| High | +20–40°, 1,400–1,900 ms; 3–4° overshoot | +35° over 1,700 ms; overshoot disabled initially |
| Recovery | Return over 2,200–3,200 ms after 3–10 seconds of safe conditions | Return over 2,700 ms after qualified aggregate CALM remains stable another 5 seconds |
| Curiosity | ±4–8°, approach 700–1,100 ms; hold 600–900 ms; return 900–1,300 ms; cooldown 90–180 seconds | Deferred until core motion is proven |

Idle cycle duration is newly proposed as 1 second outward and 1 second back. Idle runs only in READY + CALM, after recovery ends. The first idle cycle is due 60 seconds after entering that combination; a concern, fault, or restart resets that deadline. The earlier stronger-motion sketch included an optional reverse movement; defer it along with overshoot until physical clearance is verified.

Move once on a state change, then hold the resulting pose. Do not repeatedly replay the lean while a state remains elevated. Higher concern preempts idle and recovery immediately. Replan every transition from the current commanded position; never jump to the start of an old animation. HALO and display update immediately even while the bird is moving.

Any unavailable output cancels decorative motion and returns to neutral only if the actuator is calibrated and operational. At power-up, do not assume position. Disable motion until a mechanically appropriate position-reference procedure succeeds. A motion fault must leave measurement, halo, and display processing operational; it must not trigger repeated automatic homing.

All animation is nonblocking and evaluated from elapsed monotonic time. The 5-second recovery delay is an animation choice after clearing qualification; it does not replace the measurement clear_hold_ms interval or imply that a room has been certified safe.

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

Prove one complete bench loop: **sensor readings → channel states → visible cause → bounded bird motion → qualified recovery**.

Before claiming this milestone, select and document the sensor models and motion mechanism, establish electrical and mechanical limits, populate and review the classification policy, implement the loop, and execute the acceptance scenarios. Keep hardware receipts, firmware version, configuration version, and measured results together so another builder can reproduce the demonstration.
