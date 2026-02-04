import argparse
import random
import time
from typing import List

import tkinter as tk

Grid = List[bytearray]


def create_grid(size: int, seed: int | None = None, white_ratio: float = 0.5) -> Grid:
    if seed is not None:
        random.seed(seed)
    threshold = max(0.0, min(1.0, white_ratio))
    return [
        bytearray(1 if random.random() < threshold else 0 for _ in range(size))
        for _ in range(size)
    ]


def count_white_neighbors(grid: Grid, x: int, y: int) -> int:
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


def step(grid: Grid) -> Grid:
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
                new_row[x] = 0 if white_neighbors <= 1 or white_neighbors > 3 else 1
    return new_grid


def count_white_cells(grid: Grid) -> int:
    return sum(sum(row) for row in grid)


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
        self.ranges: list[tuple[int, int]] = []
        self._configure(self.window_size, self.window_size)
        self.root.bind("<Configure>", self._on_configure)

    def _on_configure(self, event: tk.Event) -> None:
        if event.width <= 1 or event.height <= 1:
            return
        self._configure(event.width, event.height)

    def _configure(self, width: int, height: int) -> None:
        canvas_size = max(1, min(width, height))
        if canvas_size == self.display_pixels:
            return
        self.display_pixels = canvas_size
        ratio = self.grid_size / canvas_size
        ranges: list[tuple[int, int]] = []
        for index in range(canvas_size):
            start = int(index * ratio)
            end = int((index + 1) * ratio)
            if end <= start:
                end = min(start + 1, self.grid_size)
            ranges.append((start, end))
        self.ranges = ranges
        self.image = tk.PhotoImage(width=canvas_size, height=canvas_size)
        if self.image_id is None:
            self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.canvas.itemconfigure(self.image_id, image=self.image)
        self.canvas.config(width=canvas_size, height=canvas_size)

    def close(self) -> None:
        self.running = False
        self.root.destroy()

    def update(self, grid: Grid) -> None:
        if not self.running or self.image is None:
            return
        display_pixels = self.display_pixels
        ranges = self.ranges
        for y in range(display_pixels):
            y_start, y_end = ranges[y]
            row_colors = []
            for x in range(display_pixels):
                x_start, x_end = ranges[x]
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
    delay: float,
    seed: int | None,
    steps: int | None,
    white_ratio: float,
    visualize: bool,
    window_size: int,
) -> None:
    grid = create_grid(size, seed, white_ratio)
    generation = 0
    visualizer = TkVisualizer(size, window_size) if visualize else None
    try:
        while (steps is None or generation < steps) and (
            visualizer is None or visualizer.running
        ):
            white_cells = count_white_cells(grid)
            black_cells = size * size - white_cells
            if visualizer is not None:
                visualizer.update(grid)
            print(f"Generation {generation}: white={white_cells} black={black_cells}", flush=True)
            time.sleep(delay)
            grid = step(grid)
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
        type=float,
        default=1.0,
        help="Sekunden zwischen den Generationen",
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
        "--visualize",
        action="store_true",
        help="Grafische Visualisierung der Zellen",
    )
    parser.add_argument(
        "--window-size",
        type=int,
        default=800,
        help="Fenstergröße der Visualisierung in Pixeln",
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
        args.visualize,
        args.window_size,
    )


if __name__ == "__main__":
    main()
