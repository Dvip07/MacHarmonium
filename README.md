# 🎹 MacHarmonium — Fast Mode

**MacHarmonium** turns your MacBook hinge into a real-time musical instrument.
Open or close your laptop lid to control *air pressure*, volume, and expression — just like the bellows of a harmonium.

[https://github.com/Dvip07/MacHarmonium](https://github.com/Dvip07/MacHarmonium)

> “Built out of boredom, sustained by caffeine, and blessed by the hinge gods.”

---

## ⚙️ Features

* 🧠 **Lid Angle Control:** Uses the [`LidAngleSensor`](https://github.com/samhenrigold/LidAngleSensor) macOS app to read real-time hinge angles
* 🎛️ **Dynamic Bellows Simulation:** Hinge angle → air pressure → sound volume
* 🎹 **Playable Keys (A–K):** Each key triggers a looping tone (c4–c5 range)
* 🌈 **Animated Visuals:** Gradient background + glowing knobs for angle, velocity, and pressure
* 🌀 **Modes:** Bellows / Pitch Bend / Filter / Chaos (press **M** to toggle)
* 🧩 **Fully Local:** No internet, no APIs — just Python, sound files, and your Mac hinge

---

## 🧪 Requirements

* macOS 12+
* Python 3.10 or higher
* [Homebrew](https://brew.sh/)
* [LidAngleSensor](https://github.com/samhenrigold/LidAngleSensor) (for real hinge data)

---

## 🥉 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Dvip07/MacHarmonium.git
cd MacHarmonium
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install the Lid Angle Sensor

Credit to [@samhenrigold](https://github.com/samhenrigold) for building this tool ❤️

```bash
brew tap samhenrigold/lidanglesensor
brew install lidanglesensor
```

Then launch the app once:

```bash
open -a LidAngleSensor
```

### 4️⃣ Run the synth!

```bash
python src/macharmonium.py
```

---

## 🎹️ Controls

| Key         | Action                         |
| ----------- | ------------------------------ |
| A–K         | Play notes (C4–C5)             |
| SPACE       | Hold a drone note              |
| M           | Toggle mode                    |
| ⌘ + Q / ESC | Quit                           |
| Mac Lid     | Adjust air pressure & dynamics |

---

## 🧠 How It Works

1. A background thread polls the current lid angle from **LidAngleSensor** via AppleScript.
2. The hinge angle is smoothed into an *air pressure* value.
3. Pygame’s mixer adjusts the volume of every active channel in real time.
4. Visual feedback shows your pressure, angle, and movement velocity.

Essentially: **your laptop lid becomes a breath controller**.

---

## 🥉 Project Structure

```
MacHarmonium/
├── src/
│   ├─ macharmonium.py      # main script
│   ├─ *.wav              # wav files (keep <10MB each)
├─ requirements.txt
├─ .gitignore
└─ README.md
```

---

## 🎖️ Credits

* **Lid Angle Data:** [samhenrigold/LidAngleSensor](https://github.com/samhenrigold/LidAngleSensor)
* **Synth Logic & Visuals:** [@Dvip07](https://github.com/Dvip07)
* **Inspiration:** MacBook hinge, boredom, and a love of strange instruments

---

## 📜 License

MIT License © 2025 [Dvip Patel](https://github.com/Dvip07)
See `LICENSE` for details.

---

## 🦃 Bonus Ideas for the Open Source Contribution

* 🎧 Add MIDI / OSC output (so hinge = modulation wheel)
* 🎨 Support more modes (e.g., “Reverb Chaos”)
* 🐧 Add mock mode for Windows/Linux (randomized hinge angles)
* 💾 Record performances as `.mid` files
