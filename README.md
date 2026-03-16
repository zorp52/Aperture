---

# Aperture

A lightweight Windows tool to quickly switch between custom screen resolutions and gamma values with a clean, button-based UI.
Built with **Python + Tkinter + pywin32**, it’s ideal for FPS gamers who frequently change display settings.

---

## ✨ Features

* 🔘 **Resolution Switcher**

  * Reads your preferred resolutions from `resolutions.json`.
  * Groups them by aspect ratio (16:9, 16:10, 4:3, etc.).
  * Shows only the resolutions supported by your monitor.
  * One-click toggle: selecting the current resolution resets to your **native resolution**.

* 💡 **Gamma Controller**

  * Predefined gamma values (`1.0`, `1.3`, `1.5`).

* 🖥️ **Super simple**

  * Fast, no popups, no bloat.
  * Dark, modern UI.

---

## 📦 Installation

### Requirements

* Windows 10/11
* Python 3.9+

### Dependencies

Install required libraries:

```bash
pip install pywin32
```

---

## ⚙️ Usage

1. Put your custom resolutions in `resolutions.json` (array of `[width, height]` pairs):

```json
[
    [1920, 1080],
    [1600, 900],
    [1366, 768],
    [1280, 720],

    [1440, 1080],
    [1280, 960],
    [1024, 768],

    [1680, 1050],
    [1440, 900],

    [1568, 1080],
    [1280, 882],

    [1080, 1080]

]

```

2. Run the script:

```bash
python resgamma_switcher.py
```

3. Click buttons to change resolution or gamma instantly.

---

## 📷 Screenshots

![Aperture GUI](https://i.imgur.com/sHAXHx3.png)

## 📄 License

MIT License. Do whatever you want with it, attribution appreciated.

