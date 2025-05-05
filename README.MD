# STM32 ISP Cloud Control Demos with IoTConnect

This repository demonstrates how to remotely control and monitor the Image Signal Processor (ISP) on various STM32-based boards using the Avnet IoTConnect platform. Users can stream video remotely, manage ISP parameters, and gather real-time telemetry through a cloud interface.

Currently supported hardware platforms:

- [STM32MP257F Discovery Kit](./STM32MP257-DK/README.MD)
- *STM32N6 (planned future support)*

---

## Project Overview

Each hardware platform folder provides a detailed setup and quick-start guide, including hardware connections, software installation, and cloud integration steps. The demos illustrate the following capabilities:

- **Remote Video Streaming** – Control and view live video streams from cloud commands.
- **ISP Parameter Control** – Adjust critical ISP settings remotely (exposure, contrast, gain, etc.).
- **Real-time Telemetry** – Receive detailed telemetry on sensor and image processing statistics.

---

## Repository Structure
    ├── STM32MP257-DK
    
    │ ├── README.md # STM32MP257 Discovery Kit specific instructions
    
    │ └── isp-cloud-control.py
    
    └── STM32N6 (Future)
    
    └── README.md # Planned support for STM32N6 MCU


---

## Additional Resources

- [IoTConnect SDK Documentation](https://github.com/avnet-iotconnect/iotc-python-lite-sdk)
- [STM32MP2 Official Documentation](https://www.st.com/en/evaluation-tools/stm32mp257f-dk2.html)
- [STMicroelectronics ISP Wiki](https://wiki.st.com/stm32mpu/wiki/X-LINUX-ISP)

---
