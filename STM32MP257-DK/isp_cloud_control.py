# SPDX-License-Identifier: MIT
# Copyright (C) 2024 Avnet
# Authors: Nikola Markovic <nikola.markovic@avnet.com> et al.

import random
import sys
import time
import gi
import threading
from avnet.iotconnect.sdk.lite import Client, DeviceConfig, C2dCommand, Callbacks, DeviceConfigError
from avnet.iotconnect.sdk.sdklib.mqtt import C2dAck
from avnet.iotconnect.sdk.lite import __version__ as SDK_VERSION

gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)

pipeline = None
src = None

def start_pipeline():
    global pipeline, src
    pipeline_desc = ("libcamerasrc name=src ! video/x-raw,format=I420,width=1280,height=720 "
                     "! videoconvert ! autovideosink sync=false")
    pipeline = Gst.parse_launch(pipeline_desc)
    pipeline.set_state(Gst.State.PLAYING)
    time.sleep(2)
    src = pipeline.get_by_name("src")
    if src:
        src.set_property("statistic-profile", 0)
        print("Pipeline started.")
    else:
        print("Error: libcamerasrc not found!")

def stop_pipeline():
    global pipeline
    if pipeline:
        pipeline.send_event(Gst.Event.new_eos())
        time.sleep(1)
        pipeline.set_state(Gst.State.NULL)
        pipeline = None
        print("Pipeline stopped.")

def read_isp_stats():
    global src
    if src:
        contrast_vals = list(src.get_property("contrast-values"))
        avg_rgb_vals = list(src.get_property("statistic-get-average-down"))
        histogram_vals = list(src.get_property("statistic-get-histogram-down"))

        stats = {
            "sdk_version": SDK_VERSION,
            "exposure": int(src.get_property("sensor-exposure")),
            "sensor_gain": float(src.get_property("sensor-gain")),
            "isp_gain": {
                "R": float(src.get_property("isp-gain-values")[0]),
                "G": float(src.get_property("isp-gain-values")[1]),
                "B": float(src.get_property("isp-gain-values")[2])
            },
            "black_level": {
                "R": int(src.get_property("black-level-values")[0]),
                "G": int(src.get_property("black-level-values")[1]),
                "B": int(src.get_property("black-level-values")[2])
            },
            "aec_enabled": bool(src.get_property("aec-algo-enable")),
            "aec_exposure_compensation": float(src.get_property("aec-algo-exposure-compensation")),
            "awb_enabled": bool(src.get_property("awb-algo-enable")),
            "demosaicing_enabled": bool(src.get_property("demosaicing-enable")),
            "luminance": {
                "lum_0": contrast_vals[0],
                "lum_32": contrast_vals[1],
                "lum_64": contrast_vals[2],
                "lum_96": contrast_vals[3],
                "lum_128": contrast_vals[4],
                "lum_160": contrast_vals[5],
                "lum_192": contrast_vals[6],
                "lum_224": contrast_vals[7],
                "lum_256": contrast_vals[8]
            },
            "awb_profile": str(src.get_property("awb-current-profile-name")),
            "awb_temperature": int(src.get_property("awb-current-profile-color-temp")),
            "avg_red": avg_rgb_vals[0],
            "avg_green": avg_rgb_vals[1],
            "avg_blue": avg_rgb_vals[2],
            "avg_luminance": avg_rgb_vals[3],
            "histogram": {f"bin_{i}": histogram_vals[i] for i in range(12)}
        }
        return stats
    return None

def on_command(msg: C2dCommand):
    global src
    print("Received command", msg.command_name, msg.command_args, msg.ack_id)

    if msg.command_name == "start-stream":
        threading.Thread(target=start_pipeline, daemon=True).start()
        c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "Stream started.")

    elif msg.command_name == "stop-stream":
        stop_pipeline()
        c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "Stream stopped.")

    elif msg.command_name == "set-exposure":
        if src and len(msg.command_args) == 1:
            exposure = int(msg.command_args[0])
            src.set_property("sensor-exposure", exposure)
            c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, f"Exposure set to {exposure}")
        else:
            c.send_command_ack(msg, C2dAck.CMD_FAILED, "Exposure command error")

    elif msg.command_name == "set-contrast":
        if src:
            contrast = [int(x) for x in msg.command_args]

            if len(contrast) == 9:
                src.set_property("contrast-enable", True)
                src.set_property("contrast-values", contrast)
                c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "Contrast adjusted")
            else:
                c.send_command_ack(msg, C2dAck.CMD_FAILED, "Contrast requires 9 values")

    elif msg.command_name == "set-gain":
        if src and len(msg.command_args) == 1:
            src.set_property("sensor-gain", float(msg.command_args[0]))
            c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "Gain set")
        else:
            c.send_command_ack(msg, C2dAck.CMD_FAILED, "Gain command error")

    elif msg.command_name == "set-awb":
        if src and msg.command_args[0] in ("enable", "disable"):
            src.set_property("awb-algo-enable", msg.command_args[0] == "enable")
            c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "AWB set")
        else:
            c.send_command_ack(msg, C2dAck.CMD_FAILED, "AWB command error")

    elif msg.command_name == "set-black-level":
        if src and len(msg.command_args) == 3:
            bl = [int(x) for x in msg.command_args]
            src.set_property("black-level-values", bl)
            src.set_property("black-level-enable", True)
            c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "Black level set")
        else:
            c.send_command_ack(msg, C2dAck.CMD_FAILED, "Black level command error")

    elif msg.command_name == "set-isp-gain":
        if src and len(msg.command_args) == 3:
            isp_gain = [float(x) for x in msg.command_args]
            src.set_property("isp-gain-values", isp_gain)
            src.set_property("isp-gain-enable", True)
            c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "ISP gain set")
        else:
            c.send_command_ack(msg, C2dAck.CMD_FAILED, "ISP gain command error")

    elif msg.command_name == "set-aec":
        if src and msg.command_args[0] in ("enable", "disable"):
            src.set_property("aec-algo-enable", msg.command_args[0] == "enable")
            c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "AEC set")
        else:
            c.send_command_ack(msg, C2dAck.CMD_FAILED, "AEC command error")

    elif msg.command_name == "set-aec-compensation":
        if src and len(msg.command_args) == 1:
            src.set_property("aec-algo-exposure-compensation", float(msg.command_args[0]))
            c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "AEC compensation set")
        else:
            c.send_command_ack(msg, C2dAck.CMD_FAILED, "AEC compensation command error")

    elif msg.command_name == "set-demosaicing":
        if src and msg.command_args[0] in ("enable", "disable"):
            src.set_property("demosaicing-enable", msg.command_args[0] == "enable")
            c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "Demosaicing set")
        else:
            c.send_command_ack(msg, C2dAck.CMD_FAILED, "Demosaicing command error")

    elif msg.command_name == "get-isp-settings":
        stats = read_isp_stats()
        if stats:
            c.send_telemetry(stats)
            c.send_command_ack(msg, C2dAck.CMD_SUCCESS_WITH_ACK, "ISP telemetry sent")
        else:
            c.send_command_ack(msg, C2dAck.CMD_FAILED, "Pipeline not started")

def on_disconnect(reason: str, disconnected_from_server: bool):
    print("Disconnected:", reason)


try:
    device_config = DeviceConfig.from_iotc_device_config_json_file(
        device_config_json_path="iotcDeviceConfig.json",
        device_cert_path="device-cert.pem",
        device_pkey_path="device-pkey.pem"
    )

    c = Client(
        config=device_config,
        callbacks=Callbacks(
            command_cb=on_command,
            disconnected_cb=on_disconnect
        )
    )

    while True:
        if not c.is_connected():
            print('(re)connecting...')
            c.connect()
            if not c.is_connected():
                print('Unable to connect. Exiting.')
                sys.exit(2)

        telemetry = {
            'sdk_version': SDK_VERSION,
            'random': random.randint(0, 100),
        }

        isp_stats = read_isp_stats()
        if isp_stats:
            telemetry.update(isp_stats)

        c.send_telemetry(telemetry)
        time.sleep(10)

except DeviceConfigError as dce:
    print(dce)
    sys.exit(1)

except KeyboardInterrupt:
    stop_pipeline()
    print("Exiting.")
    sys.exit(0)
