# 🎵 CybrPlay

A minimalist cyber-themed music visualizer for Linux built with **Python**, **Raylib**, **CAVA**, and **MPRIS**.

CybrPlay is designed to blend seamlessly into a Hyprland desktop while displaying live music metadata and a real-time audio visualizer.

![Screenshot](screenshots/cybrplay.png)

---

## ✨ Features

- 🎵 Real-time CAVA audio visualizer
- 🎧 Live song title, artist and album
- ⏱ Animated playback progress indicator
- 🖥 Transparent desktop window
- 🎨 Minimal cyber-inspired interface
- ⚡ Lightweight Python + Raylib implementation

---

## 📸 Preview

Add screenshots here.

```
screenshots/
├── cybrplay.png
└── preview.gif
```

---

## 🛠 Requirements

- Python 3.13+
- Raylib
- CAVA
- playerctl
- Linux (tested on Arch Linux)

Install dependencies:

```bash
sudo pacman -S cava playerctl raylib
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Running

```bash
python renderer.py (until i setup cybrplay.py)
```

Or launch from the included desktop entry.

---

## 📂 Project Structure

```
cybrplay/
├── assets/
├── music.py
├── cava.py
├── renderer.py
├── cybrplay.py (working on it)
├── requirements.txt
└── README.md
```

---

## 🗺 Roadmap

- [x] CAVA integration
- [x] Song metadata (MPRIS)
- [x] Progress indicator
- [x] Custom fonts
- [x] Transparent window
- [ ] Play / Pause overlay
- [ ] Smooth animations
- [ ] Configuration file
- [ ] Theme support
- [ ] Lyrics
- [ ] Plugin system

---

## 🖥 Desktop Environment

Designed primarily for:

- Hyprland
- Wayland
- Arch Linux

Although it should work on any Linux desktop supporting MPRIS and CAVA.

---

## ❤️ Inspiration

CybrPlay was created as a lightweight music visualizer that feels like part of the desktop rather than a traditional music player.

The focus is on simplicity, smooth animations, and a cyber-inspired aesthetic.

---

## 📄 License

MIT License
