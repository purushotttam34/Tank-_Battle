# Tank Battle

A fast-paced 2D tank battle game built with Python and Pygame. Fight against a smart AI opponent or challenge a friend in local two-player mode.

## Features

- **Two Game Modes**: Play against a smart AI bot or against a friend (local multiplayer)
- **Smart AI**: Advanced enemy AI with bullet dodging, pathfinding, and tactical behavior
- **5 Unique Maps**: Randomly generated obstacle layouts for varied gameplay
- **Health & Ammo System**: Manage your ammo wisely as it regenerates over time
- **Sprite-Based Graphics**: Custom tank sprites for each player
- **Sound Effects**: Background music and shooting sounds (requires pygame with mixer support)
- **Fullscreen Support**: Press F11 to toggle fullscreen mode

## Tech Stack

- **Language**: Python 3.14+
- **Framework**: pygame 2.6.1

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Tank-_Battle
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install pygame
```

### 4. Install System Libraries (For Sound Support)
On Ubuntu/Debian:
```bash
sudo apt install libsdl2-dev libsdl2-mixer-dev libsdl2-ttf-dev libsdl2-image-dev
```

Then reinstall pygame:
```bash
pip uninstall pygame -y
pip install pygame
```

## How to Run

```bash
# Using the module
python -m tank_game.main

# Or directly
python tank_game/main.py
```

## Controls

### Player 1 (Red Tank)
| Key | Action |
|-----|--------|
| W | Move Forward |
| S | Move Backward |
| A | Turn Left |
| D | Turn Right |
| SPACE | Shoot |

### Player 2 (Blue Tank) - Two Player Mode Only
| Key | Action |
|-----|--------|
| ↑ | Move Forward |
| ↓ | Move Backward |
| ← | Turn Left |
| → | Turn Right |
| LSHIFT / RSHIFT | Shoot |

### System Controls
| Key | Action |
|-----|--------|
| F11 | Toggle Fullscreen |
| ESC | Pause Game (in-game) |

## Project Structure

```
Tank-_Battle/
├── tank_game/
│   ├── __init__.py           # Package initialization
│   ├── constants.py          # Game constants and configuration
│   ├── main.py               # Game entry point
│   ├── game_state.py         # Game state management
│   ├── ai.py                 # AI control logic
│   ├── audio.py              # Sound manager
│   ├── renderer.py           # Rendering functions
│   ├── ui.py                 # UI and menu components
│   ├── models/
│   │   ├── tank.py           # Tank class
│   │   └── bullet.py         # Bullet class
│   └── utils/
│       ├── physics.py        # Physics and collision detection
│       └── maps.py           # Map definitions
├── sprites/
│   ├── Player1.png           # Player 1 tank sprite
│   └── Player2.png           # Player 2 tank sprite
├── sounds/
│   ├── background_music.mp3  # Background music
│   └── bullet_fire.wav.mp3    # Shooting sound
├── README.md                 # This file
```

## License

This project is provided as-is for educational and personal use.

## Screenshots

*Add your own screenshots by placing them in the repository and updating this section.*

---

Enjoy the battle!