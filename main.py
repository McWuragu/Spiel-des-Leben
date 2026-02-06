import argparse
import random
import time
from typing import List, Sequence

import tkinter as tk

try:
    import numpy as np
except ImportError:  # pragma: no cover - optional dependency
    np = None

Grid = List[bytearray]
GridLike = Sequence[Sequence[int]]


def create_grid(size: int, seed: int | None = None, white_ratio: float = 0.5) -> Grid:
    if seed is not None:
        random.seed(seed)
    threshold = max(0.0, min(1.0, white_ratio))
    return [
        bytearray(1 if random.random() < threshold else 0 for _ in range(size))
        for _ in range(size)
    ]


def count_white_neighbors(grid: GridLike, x: int, y: int) -> int:
    size = len(grid)
    count = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy
            if 0 <= nx < size and 0 <= ny < size:
                count += grid[ny][nx]
    return count


def step(grid: GridLike) -> Grid:
    size = len(grid)
    new_grid: Grid = [bytearray(size) for _ in range(size)]
    for y in range(size):
        row = grid[y]
        new_row = new_grid[y]
        for x in range(size):
            white_neighbors = count_white_neighbors(grid, x, y)
            cell = row[x]
            if cell == 0:
                new_row[x] = 1 if white_neighbors == 3 else 0
            else:
                new_row[x] = 0 if (white_neighbors <= 1 or white_neighbors > 3)  else 1
    return new_grid


def step_numpy(grid: "np.ndarray") -> "np.ndarray":
    if np is None:
        raise RuntimeError("NumPy ist nicht verfügbar.")
    padded = np.pad(grid, 1, mode="constant", constant_values=0)
    neighbors = (
        padded[:-2, :-2]
        + padded[:-2, 1:-1]
        + padded[:-2, 2:]
        + padded[1:-1, :-2]
        + padded[1:-1, 2:]
        + padded[2:, :-2]
        + padded[2:, 1:-1]
        + padded[2:, 2:]
    )
    alive = grid == 1
    born = neighbors == 3
    survive = alive & ((neighbors == 2) | (neighbors == 3))
    return (born | survive).astype(np.uint8)


class TkVisualizer:
    def __init__(self, size: int, window_size: int) -> None:
        self.grid_size = size
        self.window_size = max(100, window_size)
        self.root = tk.Tk()
        self.root.title("Spiel des Lebens")
        self.root.geometry(f"{self.window_size}x{self.window_size}")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.running = True

        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.image: tk.PhotoImage | None = None
        self.image_id: int | None = None
        self.display_pixels = 0
        self.ranges_x: list[tuple[int, int]] = []
        self.ranges_y: list[tuple[int, int]] = []
        self.zoom = 1.0
        self.min_zoom = 1.0
        self.max_zoom = 8.0
        self.center_x = self.grid_size // 2
        self.center_y = self.grid_size // 2
<<<<<<< codex/add-zoom-functionality-to-visualization
        self.view_size = self.grid_size
        self.last_zoom: float | None = None
        self.last_center: tuple[int, int] | None = None
        self.pan_anchor: tuple[int, int] | None = None
=======
        self.last_zoom: float | None = None
        self.last_center: tuple[int, int] | None = None
>>>>>>> main
        self._configure(self.window_size, self.window_size)
        self.root.bind("<Configure>", self._on_configure)
        self.root.bind("<MouseWheel>", self._on_mousewheel)
        self.root.bind("<Button-4>", self._on_mousewheel)
        self.root.bind("<Button-5>", self._on_mousewheel)
        self.root.bind("+", lambda _event: self._change_zoom(1))
        self.root.bind("-", lambda _event: self._change_zoom(-1))
<<<<<<< codex/add-zoom-functionality-to-visualization
        self.canvas.bind("<ButtonPress-1>", self._on_pan_start)
        self.canvas.bind("<B1-Motion>", self._on_pan_move)
=======
>>>>>>> main

    def _on_configure(self, event: tk.Event) -> None:
        if event.width <= 1 or event.height <= 1:
            return
        self._configure(event.width, event.height)

    def _configure(self, width: int, height: int) -> None:
        canvas_size = max(1, min(width, height))
        if (
            canvas_size == self.display_pixels
            and self.last_zoom == self.zoom
            and self.last_center == (self.center_x, self.center_y)
        ):
            return
        self.display_pixels = canvas_size
        view_size = max(1, int(round(self.grid_size / self.zoom)))
<<<<<<< codex/add-zoom-functionality-to-visualization
        self.view_size = view_size
=======
>>>>>>> main
        half_view = view_size // 2
        view_start_x = max(0, min(self.grid_size - view_size, self.center_x - half_view))
        view_start_y = max(0, min(self.grid_size - view_size, self.center_y - half_view))
        ratio = view_size / canvas_size
        ranges_x: list[tuple[int, int]] = []
        ranges_y: list[tuple[int, int]] = []
        for index in range(canvas_size):
            start = int(index * ratio)
            end = int((index + 1) * ratio)
            if end <= start:
                end = min(start + 1, view_size)
            ranges_x.append((start + view_start_x, end + view_start_x))
            ranges_y.append((start + view_start_y, end + view_start_y))
        self.ranges_x = ranges_x
        self.ranges_y = ranges_y
        self.last_zoom = self.zoom
        self.last_center = (self.center_x, self.center_y)
        self.image = tk.PhotoImage(width=canvas_size, height=canvas_size)
        if self.image_id is None:
            self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.canvas.itemconfigure(self.image_id, image=self.image)
        self.canvas.config(width=canvas_size, height=canvas_size)

    def _on_mousewheel(self, event: tk.Event) -> None:
        if hasattr(event, "delta") and event.delta:
            direction = 1 if event.delta > 0 else -1
        else:
            direction = 1 if getattr(event, "num", None) == 4 else -1
        self._change_zoom(direction)

    def _change_zoom(self, direction: int) -> None:
        if direction == 0:
            return
        new_zoom = self.zoom * (1.2 if direction > 0 else 1 / 1.2)
        new_zoom = max(self.min_zoom, min(self.max_zoom, new_zoom))
        if new_zoom == self.zoom:
            return
        self.zoom = new_zoom
        self._configure(self.display_pixels, self.display_pixels)

<<<<<<< codex/add-zoom-functionality-to-visualization
    def _on_pan_start(self, event: tk.Event) -> None:
        self.pan_anchor = (event.x, event.y)

    def _on_pan_move(self, event: tk.Event) -> None:
        if self.pan_anchor is None:
            return
        anchor_x, anchor_y = self.pan_anchor
        delta_x = event.x - anchor_x
        delta_y = event.y - anchor_y
        self.pan_anchor = (event.x, event.y)
        self._pan_by(delta_x, delta_y)

    def _pan_by(self, delta_x: int, delta_y: int) -> None:
        if self.display_pixels <= 0:
            return
        units_per_pixel = self.view_size / self.display_pixels
        move_x = int(round(delta_x * units_per_pixel))
        move_y = int(round(delta_y * units_per_pixel))
        if move_x == 0 and move_y == 0:
            return
        new_center_x = self.center_x - move_x
        new_center_y = self.center_y - move_y
        half_view = self.view_size // 2
        min_center = half_view
        max_center = self.grid_size - (self.view_size - half_view)
        self.center_x = max(min_center, min(max_center, new_center_x))
        self.center_y = max(min_center, min(max_center, new_center_y))
        self._configure(self.display_pixels, self.display_pixels)

=======
>>>>>>> main
    def close(self) -> None:
        self.running = False
        self.root.destroy()

    def update(self, grid: Grid) -> None:
        if not self.running or self.image is None:
            return
        display_pixels = self.display_pixels
        ranges_x = self.ranges_x
        ranges_y = self.ranges_y
        for y in range(display_pixels):
            y_start, y_end = ranges_y[y]
            row_colors = []
            for x in range(display_pixels):
                x_start, x_end = ranges_x[x]
                white_count = 0
                total = 0
                for yy in range(y_start, y_end):
                    row = grid[yy]
                    for xx in range(x_start, x_end):
                        white_count += row[xx]
                        total += 1
                row_colors.append("#ffffff" if white_count * 2 >= total else "#000000")
            self.image.put("{" + " ".join(row_colors) + "}", to=(0, y))
        self.root.update_idletasks()
        self.root.update()


def run(
    size: int,
    delay_ms: int,
    seed: int | None,
    steps: int | None,
    white_ratio: float,
    window_size: int,
    backend: str,
) -> None:
    use_numpy = backend == "numpy"
    if use_numpy and np is None:
        raise RuntimeError("NumPy-Backend gewählt, aber NumPy ist nicht installiert.")
    if use_numpy:
        grid = np.array(create_grid(size, seed, white_ratio), dtype=np.uint8)
        step_fn = step_numpy
    else:
        grid = create_grid(size, seed, white_ratio)
        step_fn = step
    generation = 0
    visualizer = TkVisualizer(size, window_size)
    delay_seconds = max(0, delay_ms) / 1000
    try:
        while (steps is None or generation < steps) and visualizer.running:
            visualizer.update(grid)
            print(".", end="", flush=True)
            time.sleep(delay_seconds)
            grid = step_fn(grid)
            generation += 1
    except KeyboardInterrupt:
        print("Simulation stopped.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulation mit schwarzem/weißem 1024x1024-Feld.",
    )
    parser.add_argument("--size", type=int, default=1024, help="Kantenlänge des Feldes")
    parser.add_argument(
        "--delay",
        type=int,
        default=500,
        help="Millisekunden zwischen den Generationen",
    )
    parser.add_argument("--seed", type=int, default=None, help="Zufalls-Seed")
    parser.add_argument(
        "--steps",
        type=int,
        default=None,
        help="Anzahl der Schritte (Standard: unendlich)",
    )
    parser.add_argument(
        "--white-ratio",
        type=float,
        default=0.5,
        help="Startanteil weißer Zellen (0.0 bis 1.0)",
    )
    parser.add_argument(
        "--window-size",
        type=int,
        default=800,
        help="Fenstergröße der Visualisierung in Pixeln",
    )
    parser.add_argument(
        "--backend",
        choices=("python", "numpy"),
        default="python",
        help="Berechnungs-Backend für den nächsten Schritt",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(
        args.size,
        args.delay,
        args.seed,
        args.steps,
        args.white_ratio,
        args.window_size,
        args.backend,
    )


if __name__ == "__main__":
    main()
