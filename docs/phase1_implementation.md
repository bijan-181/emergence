# Phase 1 Implementation — Interactive Sandbox

## Overview

Phase 1 delivers a fully functional interactive Conway's Game of Life sandbox with terminal-based rendering, mouse/keyboard input, independent render/simulation timing, and developer diagnostics.

---

## Configuration

### World Size

Default world size is **200×200 cells**, configurable via `WorldConfig`:

```python
from config.settings import WorldConfig

wc = WorldConfig(width=500, height=500)  # Larger world
```

The `Settings` container aggregates all subsystem configs:

```python
from config.settings import Settings

settings = Settings()
settings.world.width = 1000
settings.world.height = 1000
```

### Render FPS

Render FPS is independent of simulation speed. Default: **60 FPS**.

```python
settings.simulation.render_fps = 30  # Slower rendering
```

### Simulation Speed

Simulation speed (generations per second) is independent of render FPS. Default: **10 gen/s**.

```python
settings.simulation.default_speed = 20.0  # Faster simulation
```

---

## Camera Constraints

The camera enforces world boundaries at all times. The viewport never shows negative coordinates or extends beyond world edges.

### Clamping Behavior

Every camera mutation (`pan`, `zoom_in`, `zoom_out`, `center_on`, `resize`, `set_world_size`) triggers boundary clamping:

```python
# Camera offset is clamped to [0, world_dim - viewport_dim / zoom]
max_x = max(0, world_width - view_width / zoom)
max_y = max(0, world_height - view_height / zoom)
offset_x = clamp(offset_x, 0, max_x)
offset_y = clamp(offset_y, 0, max_y)
```

### Edge Cases

- **World smaller than viewport**: offset stays at 0, world is displayed at top-left
- **Zoom out beyond world**: viewport shows entire world, offset clamps to 0
- **Pan near edge**: offset clamps so last row/column is visible

### API

```python
from camera.camera import Camera
from config.settings import CameraConfig

cam = Camera(CameraConfig(), view_width=80, view_height=24,
             world_width=200, world_height=200)

cam.pan(10, 5)          # Shift viewport
cam.zoom_in()            # Zoom in (clamped)
cam.zoom_out()           # Zoom out (clamped)
cam.center_on(100, 100)  # Center on world position
cam.set_world_size(500, 500)  # Update world size (re-clamps)
```

---

## Input Pipeline

### Mouse Support

Mouse events are processed through curses with the following mask:

- `BUTTON1_CLICKED/PRESSED/RELEASED` — Left click, drag
- `BUTTON2_CLICKED/PRESSED/RELEASED` — Middle click, drag (pan)
- `BUTTON3_CLICKED` — Right click (erase)
- `BUTTON4/BUTTON5` — Scroll wheel (zoom)
- `REPORT_MOUSE_POSITION` — Motion events (drag painting)

### Event Flow

```
curses.getch() → KEY_MOUSE → InputHandler.handle_mouse()
    ↓
curses.getmouse() → decode bstate → determine action
    ↓
EventBus.publish(INPUT_CELL_TOGGLE | INPUT_CELL_ERASE | INPUT_CELL_PAINT)
    ↓
App._on_cell_toggle/erase/paint → World.set()
```

### Coordinate Conversion

Mouse screen coordinates → camera `screen_to_world()` → world coordinates:

1. Mouse position from curses is relative to stdscr
2. Simulation area starts at column 0
3. Camera converts screen (col, row) to world (x, y) using zoom and offset

### Interactions

| Input | Action |
|-------|--------|
| Left click | Toggle cell |
| Right click | Erase cell |
| Left drag | Paint alive cells |
| Middle drag | Pan camera |
| Scroll up | Zoom in |
| Scroll down | Zoom out |

---

## Simulation Timing Model

### Independent Clocks

Render and simulation run on **completely independent timing**:

```
Main Loop (non-blocking):
  ├── Input: process every iteration
  ├── Simulation: step if elapsed ≥ 1/sim_speed
  └── Render: draw if elapsed ≥ 1/render_fps
```

### Configuration

```python
settings.simulation.render_fps = 60      # Render at 60 FPS
settings.simulation.default_speed = 10.0  # Simulate at 10 gen/s
```

### Speed Control

Simulation speed is controlled via keyboard:

- `+`/`=`: Increase speed
- `-`: Decrease speed
- `Space`: Pause/Resume
- `N`: Single step (when paused)

Speed changes take effect immediately on the next simulation tick.

### Measurement

- **Render FPS**: Measured by `Clock` instance in `App._render_clock`
- **Sim TPS**: Measured by `Engine.tps` (rolling average of step intervals)

Both values are displayed independently in the sidebar.

---

## Render Loop

### Architecture

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Simulation   │  │   Sidebar    │  │  Status Bar  │
│   Subwindow   │  │  Subwindow   │  │  Subwindow   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                    curses.doupdate()
                         │
                    Physical Terminal
```

### Properties

- Each component renders into its own curses subwindow
- Overwrite-only strategy (no erase → no flicker)
- Single `curses.doupdate()` flushes all changes atomically
- On terminal resize, all subwindows are recreated

---

## Debug Overlay

Toggle with **F1**. Disabled by default.

### Displayed Information

- Mouse screen coordinates
- Mouse world coordinates
- Camera position (offset)
- Camera visible bounds
- Zoom level
- Viewport size
- World size
- Render FPS
- Simulation TPS
- Simulation state (RUNNING/PAUSED/IDLE)
- Generation count
- Alive cell count
- Simulation speed
- Drag state

### Implementation

The `DebugOverlay` class renders into stdscr (the main window), floating above all subwindows. It uses `curses.A_REVERSE` for visibility.

---

## Architecture Constraints

The implementation maintains strict separation:

```
Input → Camera → World
                    ↑
Simulation ─────────┘
    ↓
Renderer (read-only)
```

- **Renderer never modifies world state** — it only reads and displays
- **Simulation never depends on render speed** — independent timing
- **Input never modifies rendering directly** — events go through EventBus
- **Camera is decoupled from renderer** — coordinate math is pure

---

## Testing

### Test Coverage

- Camera boundary clamping (11 tests)
- Coordinate mapping (8 tests)
- Engine timing (4 tests)
- Clock measurement (6 tests)
- World size configuration (8 tests)
- Debug overlay state (10 tests)
- Existing tests preserved (62 tests)

**Total: 109 tests, all passing.**

### Running Tests

```bash
python -m pytest tests/ -v
```
