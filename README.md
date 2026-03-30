# Egg Hunt

A pygame-based egg collection game with single-player and two-player modes.

## Features

- **Main Menu**: Navigate between single-player and two-player modes
- **Level Selection**: Choose from 3 different levels in single-player mode
- **Single Player Mode**: Collect 10 eggs within 60 seconds as a duck
- **Two Player Mode**: Competitive egg hunting with snake obstacles

## Requirements

- Python 3.x
- pygame

## Installation

```bash
pip install pygame
```

## How to Run

```bash
python main.py
```

## Gameplay

### Single Player (1P)
- **Objective**: Collect all 10 eggs before time runs out
- **Controls**:
  - Arrow Keys: Move
  - Shift: Sprint (faster movement)
  - Q / Esc: Return to level selection
- **Time Limit**: 60 seconds per level

### Two Player (2P)
- **Objective**: Collect more eggs than your opponent
- **Controls**:
  - **Player 1**: Arrow Keys
  - **Player 2**: WASD
  - Q / Esc: Return to main menu
- **Hazards**: Avoid snakes - touching one causes instant loss
- **Win Condition**: Most eggs collected when all eggs are gone

## Project Structure

```
Egg Hunt/
├── main.py              # Main entry point and menu system
├── levelselection.py    # Level selection screen
├── utils.py             # Shared utilities (image loading, collision, etc.)
├── level/               # Level logic modules
│   ├── level1.py        # Level 1 gameplay
│   ├── level2.py        # Level 2 gameplay
│   ├── level3.py        # Level 3 gameplay
│   ├── 1P.py            # Single player module
│   ├── 2P.py            # Two player module (legacy)
│   └── 2P2.py           # Two player module (active)
├── maps/                # Level map definitions
│   ├── level1map.py     # Level 1 map
│   ├── level2map.py     # Level 2 map
│   └── level3map.py     # Level 3 map
├── img/                 # Game assets (images)
└── README.md            # This file
```

## Configuration

Edit `utils.py` to change:
- `WINDOW_SIZE`: Default is (1366, 768)
- `FPS`: Default is 60
- `TILE_SIZE`: Default is 50 pixels

## Assets

All game images are stored in the `img/` directory:
- Player sprites (P1.png, P2.png)
- UI elements (buttons, menus)
- Tile graphics (Grass.png, Rock.png)
- Collectibles (Egg.png)
- Hazards (Snake.png)
- End screens (Won.png, Lost.png, P1Won.png, P2Won.png)
