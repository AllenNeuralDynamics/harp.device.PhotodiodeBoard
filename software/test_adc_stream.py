# /// script
# requires-python = ">=3.11"
# dependencies = ["harp-serial", "harp-device", "numpy"]
# ///
"""Bench test for the PhotodiodeBoard ADC event stream.

Usage:
    uv run software/test_adc_stream.py COM3 [--seconds 5]

Checks:
  1. Device identity (WhoAmI from device.yml) and version info.
  2. Event rate, timestamp spacing and values of ADC in Active mode.
  3. No ADC events in Standby mode.
"""
import argparse
import threading
import time
from pathlib import Path

import numpy as np
from harp import serial
from harp.device import core, schema

DEVICE_YML = Path(__file__).resolve().parents[1] / "device.yml"
EXPECTED_RATE_HZ = 1000
RATE_TOLERANCE = 0.05  # fraction


def set_op_mode(device, mode: core.OperationMode) -> None:
    payload = core.OperationControlPayload(
        operation_mode=mode,
        dump_registers=False,
        mute_replies=False,
        visual_indicators=core.EnableFlag.ENABLED,
        operation_led=core.EnableFlag.ENABLED,
        heartbeat=core.EnableFlag.DISABLED,
    )
    device.write(core.OperationControl, payload)


class Collector:
    """Collects (timestamp, payload) tuples for one register from the event thread."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.events = []

    def __call__(self, msg) -> None:
        with self.lock:
            self.events.append((msg.timestamp, msg.payload))

    def take(self):
        with self.lock:
            events, self.events = self.events, []
        return events


def collect(device, dev, mode: core.OperationMode, seconds: float):
    """Stay in `mode` for `seconds`, then return to Standby. Return ADC events."""
    adc = Collector()
    with device.subscribe(dev.ADC, adc):
        set_op_mode(device, mode)
        time.sleep(seconds)
        set_op_mode(device, core.OperationMode.STANDBY)
        time.sleep(0.2)  # Let in-flight events drain.
    return adc.take()


def summarize(events, seconds: float) -> bool:
    if not events:
        print("  no events")
        return False
    ts = np.array([t for t, _ in events])
    dt_ms = np.diff(ts) * 1e3
    rate = len(events) / seconds
    values = np.array([[int(p.adc0), int(p.adc1)] for _, p in events])
    print(f"  {len(events)} events, {rate:.1f} Hz")
    if dt_ms.size:
        print(f"  dt ms: mean {dt_ms.mean():.4f}  std {dt_ms.std():.4f}  "
              f"min {dt_ms.min():.4f}  max {dt_ms.max():.4f}")
    for ch in range(2):
        print(f"  ADC{ch} mean {values[:, ch].mean():.2f} "
              f"(min {values[:, ch].min()}, max {values[:, ch].max()})")
    return abs(rate - EXPECTED_RATE_HZ) <= EXPECTED_RATE_HZ * RATE_TOLERANCE


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("port", help="Serial port, e.g. COM3 or /dev/ttyACM0")
    parser.add_argument("--seconds", type=float, default=5.0)
    args = parser.parse_args()

    dev = schema.create_device_module(DEVICE_YML.read_bytes())
    results = {}
    # Passing the module validates WhoAmI on open.
    with serial.open_device(dev, port=args.port) as device:
        print(f"WhoAmI:   {device.read(core.WhoAmI).payload}")
        print(f"Name:     {device.read(core.DeviceName).payload}")
        print(f"Firmware: {device.read(core.FirmwareVersionHigh).payload}."
              f"{device.read(core.FirmwareVersionLow).payload}")
        print(f"Hardware: {device.read(core.HardwareVersionHigh).payload}."
              f"{device.read(core.HardwareVersionLow).payload}")
        set_op_mode(device, core.OperationMode.STANDBY)

        print(f"\nOn-demand read: ADC = {device.read(dev.ADC).payload}")

        print(f"\nActive mode, {args.seconds} s:")
        events = collect(device, dev, core.OperationMode.ACTIVE, args.seconds)
        results["ADC rate"] = summarize(events, args.seconds)

        print("\nStandby mode, 1 s:")
        events = collect(device, dev, core.OperationMode.STANDBY, 1.0)
        print(f"  ADC events: {len(events)}")
        results["No events in Standby"] = len(events) == 0

    print("\nResults:")
    for name, ok in results.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    raise SystemExit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
