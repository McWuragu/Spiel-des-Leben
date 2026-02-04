import argparse
import random
import time
from typing import List

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
                new_row[x] = 0 if (white_neighbors <= 1 or white_neighbors > 3)  else 1
    return new_grid


def count_white_cells(grid: Grid) -> int:
    return sum(sum(row) for row in grid)


def render_ascii(grid: Grid, view_size: int) -> str:
    size = len(grid)
    view_size = max(1, min(view_size, size))
    step = max(1, size // view_size)
    lines: list[str] = []
    for y in range(0, size, step):
        row_chars = []
        for x in range(0, size, step):
            white_count = 0
            total = 0
            for yy in range(y, min(y + step, size)):
                for xx in range(x, min(x + step, size)):
                    white_count += grid[yy][xx]
                    total += 1
            row_chars.append("⬜" if white_count * 2 >= total else "⬛")
        lines.append("".join(row_chars))
    return "\n".join(lines)


def run(
    size: int,
    delay: float,
    seed: int | None,
    steps: int | None,
    white_ratio: float,
    visualize: bool,
    view_size: int,
) -> None:
    grid = create_grid(size, seed, white_ratio)
    generation = 0
    try:
        while steps is None or generation < steps:
            white_cells = count_white_cells(grid)
            black_cells = size * size - white_cells
            if visualize:
                print("\x1b[2J\x1b[H", end="")
                print(render_ascii(grid, view_size))
                print()
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
        help="ASCII-Visualisierung der Zellen",
    )
    parser.add_argument(
        "--view-size",
        type=int,
        default=64,
        help="Größe der ASCII-Ansicht (z.B. 64 zeigt 64x64)",
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
        args.view_size,
    )


if __name__ == "__main__":
    main()
