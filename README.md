# Spiel des Lebens

Eine einfache Python-Implementierung von Conways **Game of Life** („Spiel des Lebens“) mit einer Tkinter-Visualisierung. Das Spielfeld besteht aus schwarzen und weißen Zellen; weiße Zellen gelten als lebendig, schwarze Zellen als tot.

## Funktionsweise

Beim Start wird ein quadratisches Feld zufällig erzeugt. Anschließend wird in jeder Generation für jede Zelle die Anzahl der lebenden Nachbarn in den acht umliegenden Feldern gezählt. Daraus entsteht nach den klassischen Regeln von Conway die nächste Generation:

- Eine tote Zelle wird lebendig, wenn sie genau drei lebende Nachbarn hat.
- Eine lebende Zelle stirbt bei Unterbevölkerung mit null oder einem lebenden Nachbarn.
- Eine lebende Zelle stirbt bei Überbevölkerung mit mehr als drei lebenden Nachbarn.
- Eine lebende Zelle überlebt mit zwei oder drei lebenden Nachbarn.

Die Simulation läuft in einem Tkinter-Fenster. Während der Ausführung wird pro Generation ein Punkt (`.`) in der Konsole ausgegeben.

## Voraussetzungen

- Python 3.10 oder neuer
- Tkinter, normalerweise bereits in vielen Python-Installationen enthalten
- Optional: NumPy für das schnellere Berechnungs-Backend

NumPy kann bei Bedarf installiert werden mit:

```bash
pip install numpy
```

## Starten

```bash
python main.py
```

Standardmäßig startet das Programm mit einem `1024 x 1024` großen Feld, einer Verzögerung von `500 ms` zwischen den Generationen und dem reinen Python-Backend.

## Parameter

Das Skript verwendet Kommandozeilenparameter über `argparse`:

| Parameter | Standardwert | Beschreibung |
| --- | --- | --- |
| `--size` | `1024` | Kantenlänge des quadratischen Spielfelds. Ein Wert von `200` erzeugt zum Beispiel ein `200 x 200` Feld. |
| `--delay` | `500` | Wartezeit zwischen zwei Generationen in Millisekunden. `0` lässt die Simulation ohne absichtliche Pause laufen. |
| `--seed` | `None` | Zufalls-Seed für eine reproduzierbare Startverteilung. Bei gleichem Seed entsteht dieselbe Anfangsgeneration. |
| `--steps` | `None` | Anzahl der zu berechnenden Generationen. Ohne Angabe läuft die Simulation, bis das Fenster geschlossen oder das Programm beendet wird. |
| `--white-ratio` | `0.5` | Anteil lebender/weißer Zellen in der Startgeneration. Werte werden intern auf den Bereich `0.0` bis `1.0` begrenzt. |
| `--window-size` | `800` | Größe des Visualisierungsfensters in Pixeln. Das Fenster ist quadratisch. |
| `--backend` | `python` | Berechnungs-Backend. Möglich sind `python` und `numpy`. Das NumPy-Backend benötigt eine installierte NumPy-Bibliothek. |

## Beispiele

Simulation mit kleinerem Feld und schnellerer Aktualisierung:

```bash
python main.py --size 200 --delay 100
```

Reproduzierbare Simulation mit festem Seed und 100 Generationen:

```bash
python main.py --seed 42 --steps 100
```

Simulation mit weniger lebenden Startzellen:

```bash
python main.py --white-ratio 0.2
```

Schnelleres NumPy-Backend verwenden:

```bash
python main.py --backend numpy
```

## Bedienung im Fenster

- Mit dem Mausrad kann in das Spielfeld hinein- und herausgezoomt werden.
- Mit `+` und `-` kann ebenfalls gezoomt werden.
- Mit gedrückter linker Maustaste kann der sichtbare Ausschnitt verschoben werden.
- Das Schließen des Fensters beendet die Simulation.

## Projektstruktur

- `main.py` enthält die komplette Simulation, die Berechnung der nächsten Generation, die optionale NumPy-Variante, die Tkinter-Visualisierung und die Kommandozeilenparameter.
- `README.md` enthält diese Projektbeschreibung und Hinweise zur Verwendung.
