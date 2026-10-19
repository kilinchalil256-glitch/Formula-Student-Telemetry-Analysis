# Formula Student Telemetry Analyzer

A Python-based telemetry analysis project designed to process and visualize vehicle test data.

This project was developed as a practical learning exercise in mechanical engineering, data analysis, and scientific Python programming, with Formula Student applications in mind.

## Features

**Telemetry Analysis**
- Maximum and average vehicle speed
- Maximum and average engine RPM
- Maximum and average temperature
- Longitudinal acceleration and deceleration calculations

**Braking Analysis**
- Identification of measurements with active braking
- Peak deceleration during braking
- Detection of simultaneous throttle and brake inputs

**Data Validation**
- Empty dataset detection
- Negative vehicle speed detection
- Invalid or non-increasing timestamps
- Missing value detection
- Minimum measurement count validation

**Data Visualization**

A four-panel Matplotlib dashboard displaying:

1. Vehicle speed vs. time
2. Engine RPM vs. time
3. Longitudinal acceleration vs. time
4. Temperature vs. time

**CSV Reporting**

Automatically exports a summary of calculated metrics to `report.csv`.

## Technologies

- **Python** — Core application logic
- **NumPy** — Numerical calculations and acceleration analysis
- **Pandas** — CSV processing and DataFrame operations
- **Matplotlib** — Telemetry visualization
- **Git & GitHub** — Version control

## Getting Started

Clone the repository:

`git clone https://github.com/kilinchalil256-glitch/Formula-Student-Telemetry-Analysis.git`

Enter the project directory:

`cd Formula-Student-Telemetry-Analysis`

Create and activate a virtual environment on macOS or Linux:

`python3 -m venv .venv`

`source .venv/bin/activate`

Install the dependencies:

`python -m pip install -r requirements.txt`

Run the analyzer:

`python main.py`

## CSV Data Format

The application expects a CSV file with the following columns:

| Column | Description | Unit |
|---|---|---|
| `time_s` | Measurement timestamp | s |
| `speed_kmh` | Vehicle speed | km/h |
| `rpm` | Engine speed | RPM |
| `throttle_pct` | Throttle input | % |
| `brake_pct` | Brake input | % |
| `temp_c` | Temperature | °C |

The repository includes `telemetry.csv` as a small example dataset.

To analyze another dataset, update the input filename in `main.py`. Input data should contain at least two measurements and valid, increasing timestamps.

## Outputs

Running the program produces:

- A terminal summary of telemetry statistics
- `report.csv` containing calculated metrics
- `telemetry_dashboard.png` containing four telemetry plots
- An interactive Matplotlib plot window

Generated reports and images are excluded from version control.

## Current Limitations

- Supports offline CSV analysis, not live sensor streaming
- Acceleration is estimated from consecutive speed measurements
- Braking measurements are not yet grouped into complete braking events
- Input column names and numerical types are not fully validated
- Vehicle measurements are intended for educational analysis and should not be interpreted as validated physical testing results

## Future Improvements

- Detailed braking-event analysis
- Automated testing
- Interactive telemetry visualization using Plotly
- Comparison of multiple driving sessions
- Live telemetry visualization and sensor integration

## Project Status

**Version 1 — CSV telemetry analysis and visualization**

An educational engineering project focused on developing practical numerical analysis and Python programming skills.