
# STM32MP2 Discovery Kit ISP Cloud Control Demo

This demo provides instructions on configuring and using the Avnet /IOTCONNECT cloud platform to remotely control and monitor the Image Signal Processor (ISP) on the **STM32MP257F Discovery Kit**. It enables users to remotely stream video, control ISP settings, and view real-time telemetry data.

---
## Index

- [STM32MP2 Discovery Kit ISP Cloud Control Demo](#stm32mp2-discovery-kit-isp-cloud-control-demo)
  - [Hardware Requirements](#hardware-requirements)
  - [Software Requirements](#software-requirements)
    - [Pre-installation Steps](#pre-installation-steps)
    - [/IOTCONNECT SDK Setup](#iotconnect-sdk-setup)
  - [Running the ISP Cloud Control Demo](#running-the-isp-cloud-control-demo)
    - [Step-by-Step Guide](#step-by-step-guide)
  - [Available Commands from IoTConnect Cloud](#available-commands-from-iotconnect-cloud)
  - [Telemetry Data Sent to /IOTCONNECT](#telemetry-data-sent-to-iotconnect)
  - [Relevant Images and Documentation](#relevant-images-and-documentation)

--- 

## Hardware Requirements

- **STM32MP257F Discovery Kit**  

  ![STM32MP257F Discovery Kit](./mp2DK.jpg?quality=80&bg-color=255,255,255&fit=bounds&height=&width=)

- **Camera module compatible with STM32MP257F** (recommended IMX335)

![B-CAMS-IMX](https://estore.st.com/media/catalog/product/p/f/pf275440_m.jpg?quality=80&bg-color=255,255,255&fit=bounds&height=&width=)

- **5V External Power Supply** (Required due to high current draw with camera and ISP)

- **Ethernet cable** (for network connectivity)

---

## Software Requirements

### Pre-installation Steps

1. **Setup X-LINUX-ISP Starter Package**  

Follow these instructions to set up the STM32MP257F Discovery Kit with the X-LINUX-ISP Starter Package:

- Visit the official STMicroelectronics guide:
  - [X-LINUX-ISP Starter Package](https://wiki.st.com/stm32mpu/wiki/X-LINUX-ISP_Starter_package)

- **Populate and boot the STM32MP257F Discovery Kit** following these instructions:
  - [Populate and Boot Instructions](https://wiki.st.com/stm32mpu/wiki/Getting_started/STM32MP2_boards/STM32MP257x-EV1/Let%27s_start/Populate_the_target_and_boot_the_image)

  or build your custom Yocto image using the meta-layer:
  - [meta-st-x-linux-isp](https://github.com/STMicroelectronics/meta-st-x-linux-isp)

- Complete steps **5 to 7** on the official page:
  - [Configure and test ISP](https://wiki.st.com/stm32mpu/wiki/X-LINUX-ISP_Starter_package)

---

### /IOTCONNECT  SDK Setup

Install /IOTCONNECT  Python SDK Lite using the Quickstart guide:

- **Quickstart Guide:**  
  [/IOTCONNECT  Python Lite SDK](https://github.com/avnet-iotconnect/iotc-python-lite-sdk/blob/main/QUICKSTART.md)

```bash
sudo apt-get update
sudo apt-get install python3-pip -y
python3 -m pip install iotconnect-sdk-lite
```

---

## Running the ISP Cloud Control Demo

### Step-by-Step Guide

1. **Clone the demo repository** to your STM32MP2 board (optional):

```bash
git clone https://github.com/avnet-iotconnect/iotc-python-lite-sdk-demos.git
cd iotc-python-lite-sdk-demos/stm32mp2-isp-control
```

Alternatively, copy the provided script directly onto the board.

2. **Modify device credentials** (`iotcDeviceConfig.json`, `device-cert.pem`, and `device-pkey.pem`) from your IoTConnect account and copy them to the device directory.

3. **Run the ISP cloud control script**:

```bash
python3 isp-cloud-control.py
```

---
## Available Commands from IoTConnect Cloud
| Command                | Parameters                           | Example                        | Description                               |
| ---------------------- | ------------------------------------ | ------------------------------ | ----------------------------------------- |
| `start-stream`         | None                                 | `start-stream`                 | Starts video streaming                    |
| `stop-stream`          | None                                 | `stop-stream`                  | Stops video streaming                     |
| `set-exposure`         | Integer (in microseconds)            | `set-exposure 33000`           | Sets sensor exposure                      |
| `set-contrast`         | 9 integers (space-separated)         | `set-contrast 256 256 128 ...` | Sets luminance contrast                   |
| `set-gain`             | Float or integer (sensor gain in dB) | `set-gain 4`                   | Sets sensor gain                          |
| `set-awb`              | String (`enable` or `disable`)       | `set-awb enable`               | Enables/Disables auto white balance (AWB) |
| `set-black-level`      | 3 integers for RGB values            | `set-black-level 16 16 16`     | Sets black level correction               |
| `set-isp-gain`         | 3 floats (R, G, B gains)             | `set-isp-gain 1.0 1.2 1.1`     | Adjusts ISP gain                          |
| `set-aec`              | String (`enable` or `disable`)       | `set-aec enable`               | Enables/Disables Auto Exposure Control    |
| `set-aec-compensation` | Float (-2 to +2 EV)                  | `set-aec-compensation 0.5`     | Sets exposure compensation                |
| `set-demosaicing`      | String (`enable` or `disable`)       | `set-demosaicing enable`       | Enables/Disables ISP demosaicing          |
| `get-isp-settings`     | None                                 | `get-isp-settings`             | Returns current ISP settings as telemetry |

## Telemetry Data Sent to /IOTCONNECT
| Telemetry Field   | Data Type         | Description                             |
| ----------------- | ----------------- | --------------------------------------- |
| `sdk_version`     | String            | SDK version                             |
| `exposure`        | Integer           | Sensor exposure time (µs)               |
| `awb_profile`     | String            | Current AWB profile                     |
| `awb_temperature` | Integer           | AWB color temperature (K)               |
| `avg_red`         | Integer           | Average red channel value               |
| `avg_green`       | Integer           | Average green channel value             |
| `avg_blue`        | Integer           | Average blue channel value              |
| `avg_luminance`   | Integer           | Average luminance value                 |
| `luminance`       | Object (integers) | Luminance values (`lum_0` to `lum_256`) |
| `histogram`       | Object (integers) | Histogram bins (`bin_0` to `bin_11`)    |

--- 
## Relevant Images and Documentation

- **STM32MP257 Discovery Kit Official Page:**  
  [STM32MP257 Discovery Kit](https://www.st.com/en/evaluation-tools/stm32mp257f-dk2.html)

- **/IOTCONNECT  Documentation and SDKs:**  
  [/IOTCONNECT  GitHub](https://github.com/avnet-iotconnect)

- **STMicroelectronics ISP Wiki:**  
  [STMicroelectronics ISP Documentation](https://wiki.st.com/stm32mpu/wiki/X-LINUX-ISP)

- **STM32MP257 ISP Demo in action:**  
  ![ISP tuning demo](https://wiki.st.com/stm32mpu/images/6/6b/IQTune-FineTuning.JPG)
