import os
import json
import ctypes
import tkinter as tk
from win32api import GetSystemMetrics, EnumDisplaySettings, ChangeDisplaySettings
import pywintypes
import win32con

FALLBACK_RES = [
    [1920, 1080],
    [1440, 1080],
    [1680, 1050],
    [1280, 960]
]

BASE_RES = (1920, 1080)  # reset if re-click

cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resolutions.json")
if os.path.exists(cfg_path):
    try:
        with open(cfg_path, "r", encoding="utf-8") as fh:
            RES_LIST = json.load(fh)
            if not isinstance(RES_LIST, list):
                raise ValueError("resolutions.json must be a list of [w,h] pairs")
    except Exception:
        RES_LIST = FALLBACK_RES
else:
    RES_LIST = FALLBACK_RES


def get_supported_resolutions():
    modes = set()
    i = 0
    while True:
        try:
            dm = EnumDisplaySettings(None, i)
        except Exception:
            break
        try:
            modes.add((int(dm.PelsWidth), int(dm.PelsHeight)))
        except Exception:
            pass
        i += 1
    return modes

_supported = get_supported_resolutions()

def aspect_group(w, h):
    ratio = round(w / h, 2)
    if abs(ratio - 1.33) < 0.02:
        return "4:3"
    elif abs(ratio - 1.6) < 0.02:
        return "16:10"
    elif abs(ratio - 1.78) < 0.02:
        return "16:9"
    else:
        return "Other"


filtered_groups = {}
for (w, h) in RES_LIST:
    if (w, h) not in _supported:
        continue
    group = aspect_group(w, h)
    filtered_groups.setdefault(group, []).append((w, h))

for k in filtered_groups:
    filtered_groups[k].sort()


def change_resolution(width, height):
    cur_x, cur_y = GetSystemMetrics(0), GetSystemMetrics(1)
    new_res = (width, height)
    if (cur_x, cur_y) == new_res:
        new_res = BASE_RES

    dm = pywintypes.DEVMODEType()
    dm.PelsWidth = int(new_res[0])
    dm.PelsHeight = int(new_res[1])
    dm.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    result = ChangeDisplaySettings(dm, 0)

    if result == 0:
        nx, ny = GetSystemMetrics(0), GetSystemMetrics(1)
        current_label.config(text=f"Current Resolution: {nx}x{ny}")
        status_label.config(text=f"Resolution set to {nx}x{ny}")
    else:
        status_label.config(text=f"Resolution change failed ({result})")

def set_gamma(gamma_value: float):
    if gamma_value <= 0:
        status_label.config(text="Gamma must be > 0")
        return

    hdc = ctypes.windll.user32.GetDC(0)
    if not hdc:
        return

    GammaArray = ctypes.c_ushort * (256 * 3)
    ramp = GammaArray()
    for i in range(256):
        normalized = i / 255.0
        corrected = normalized ** (1.0 / gamma_value)
        val = int(min(65535, corrected * 65535.0 + 0.5))
        ramp[i] = ramp[256 + i] = ramp[512 + i] = val

    ok = ctypes.windll.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))
    ctypes.windll.user32.ReleaseDC(0, hdc)

    if ok:
        status_label.config(text=f"Gamma set to {gamma_value}")
    else:
        status_label.config(text="Gamma change failed")


def reset_defaults():
    change_resolution(*BASE_RES)
    set_gamma(1.0)
    status_label.config(text="Reset to defaults (1920x1080, gamma 1.0)")

# GUI
BG = "#0F1113"
BTN_BG = "#1F2225"
BTN_FG = "#E6EEF6"
ACCENT = "#2EA3FF"
FONT = ("Segoe UI", 10)

root = tk.Tk()
root.title("Aperture")
root.configure(bg=BG)

cur_x, cur_y = GetSystemMetrics(0), GetSystemMetrics(1)
current_label = tk.Label(root, text=f"Current Resolution: {cur_x}x{cur_y}", bg=BG, fg="white", font=("Segoe UI", 11, "bold"))
current_label.pack(pady=(12, 6))

container = tk.Frame(root, bg=BG)
container.pack(padx=12, pady=8)

ratio_keys = list(filtered_groups.keys())
for col_index, ratio in enumerate(ratio_keys):
    col_frame = tk.Frame(container, bg=BG)
    col_frame.grid(row=0, column=col_index, padx=10, sticky="n")

    tk.Label(col_frame, text=ratio, bg=BG, fg="white", font=("Segoe UI", 10, "bold")).pack(pady=(0, 8))

    for (w, h) in filtered_groups[ratio]:
        btn = tk.Button(col_frame, text=f"{w}x{h}",
                        command=lambda w=w, h=h: change_resolution(w, h),
                        bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, relief="flat", padx=12, pady=6, font=FONT)
        btn.pack(fill="x", pady=4)

# Gamma column
gamma_col = len(ratio_keys)
gamma_frame = tk.Frame(container, bg=BG)
gamma_frame.grid(row=0, column=gamma_col, padx=14, sticky="n")

tk.Label(gamma_frame, text="Gamma", bg=BG, fg="white", font=("Segoe UI", 10, "bold")).pack(pady=(0, 8))
for gval in (1.0, 1.3, 1.5):
    tk.Button(gamma_frame, text=str(gval), command=lambda g=gval: set_gamma(g),
              bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, relief="flat", padx=12, pady=6, font=FONT).pack(fill="x", pady=4)

# Status bar
status_label = tk.Label(root, text="", bg=BG, fg="#BBBBBB", font=("Segoe UI", 9))
status_label.pack(pady=(6, 10))

# Bottom buttons
bottom_frame = tk.Frame(root, bg=BG)
bottom_frame.pack(pady=(0, 12))

reset_btn = tk.Button(bottom_frame, text="Reset", command=reset_defaults,
                      bg=ACCENT, fg="white", relief="flat", padx=14, pady=6, font=FONT)
reset_btn.pack(side="left", padx=6)

exit_btn = tk.Button(bottom_frame, text="Exit", command=root.destroy,
                     bg="#CC3333", fg="white", relief="flat", padx=14, pady=6, font=FONT)
exit_btn.pack(side="left", padx=6)

root.resizable(False, False)
root.mainloop()
