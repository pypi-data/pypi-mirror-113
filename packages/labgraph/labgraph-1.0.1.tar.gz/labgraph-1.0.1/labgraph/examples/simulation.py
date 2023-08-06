#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import asyncio
import time
from typing import Tuple

import labgraph as df
import numpy as np
from arvr.libraries.labgraph_viz.v1.plots import LinePlot, LinePlotConfig, Mode
from scipy import signal
from scipy.stats import gamma

# Constants used by nodes
SAMPLE_RATE = 10.0
NUM_FEATURES = 100
WINDOW = 2.0

# Simulation configurations
SAMPLE_SIZE_CYCLE = 30
SAMPLES_REST = 9
ORDER_OF_ZERO_DAUB = 10
PEAK_GAMMA_SHAPE = 6
UNDERSHOOT_GAMMA_SHAPE = 12
TIME_TO_ZERO_HFR = 0.35


class SimulationFunction:
    """
    Simulation functions to generate a cycle (one cycle of the function).
    """

    # Last element is removed to ensure no overlaps between cycles.
    phase_data = np.linspace(-np.pi, np.pi, SAMPLE_SIZE_CYCLE)[:-1]

    # Generate a sine cycle
    def sin_cycle(self):
        return np.sin(self.phase_data)

    # Generate a square cycle
    def square_cycle(self):
        return np.sign(np.sin(self.phase_data))

    # Generate a heartbeat-like cycle using daubechies cycle
    def daub_cycle(self):
        hb = signal.wavelets.daub(ORDER_OF_ZERO_DAUB)
        zero_array = np.zeros(SAMPLES_REST, dtype=float)
        hb_full = np.concatenate([hb, zero_array])
        return hb_full

    # Generate a hemodynamic responses (HRFs) cycle
    def hrf_cycle(self):
        times = np.arange(1, SAMPLE_SIZE_CYCLE)
        peak_values = gamma.pdf(times, PEAK_GAMMA_SHAPE)
        undershoot_values = gamma.pdf(times, UNDERSHOOT_GAMMA_SHAPE)
        values = peak_values - TIME_TO_ZERO_HFR * undershoot_values
        return values / np.max(values)


class SimulationMessage(df.Message):
    timestamp: float
    sin_data: float
    square_data: float
    daub_data: float
    hrf_data: float


class GeneratorConfig(df.Config):
    sample_rate: float
    num_features: int


class SimulationGenerator(df.Node):
    """
    Generate messages to visualize
    Repeatedly generate cycles using simulation functions.

    Note: Cycle periods of different functions are chosen
    the same in this example.
    """

    OUTPUT = df.Topic(SimulationMessage)
    config: GeneratorConfig

    @df.publisher(OUTPUT)
    async def generate_simulation(self) -> df.AsyncPublisher:
        SF = SimulationFunction()
        sin_base_data = SF.sin_cycle()
        square_base_data = SF.square_cycle()
        daub_base_data = SF.daub_cycle()
        hrf_base_data = SF.hrf_cycle()

        while True:
            for sin_data, square_data, daub_data, hrf_data in zip(
                sin_base_data, square_base_data, daub_base_data, hrf_base_data
            ):
                ts = time.time()
                yield self.OUTPUT, SimulationMessage(
                    timestamp=ts,
                    sin_data=sin_data,
                    square_data=square_data,
                    daub_data=daub_data,
                    hrf_data=hrf_data,
                )
                await asyncio.sleep(1 / self.config.sample_rate)


class Window(df.Node):
    """
    This is an example of a custom Window Node.
    It creates a new window, sets some properties of the Window,
    adds some plots and starts the QT application.
    """

    SIN_PLOT: LinePlot
    SQ_PLOT: LinePlot
    DAUB_PLOT: LinePlot
    HRF_PLOT: LinePlot

    @df.main
    def run_plot(self) -> None:
        import pyqtgraph as pg  # type: ignore
        from pyqtgraph.Qt import QtGui  # type: ignore

        plots = [self.SIN_PLOT, self.SQ_PLOT, self.DAUB_PLOT, self.HRF_PLOT]

        win = pg.GraphicsWindow()
        win.setWindowTitle("LabGraph Simulation")

        for plot in plots:
            win.addItem(plot.build())
            win.nextRow()

        QtGui.QApplication.instance().exec_()

    def cleanup(self) -> None:
        from pyqtgraph.Qt import QtGui  # type: ignore

        QtGui.QApplication.instance().quit()


class VizGroup(df.Group):
    """
    This is an example of how we can display the LinePlot
    in a custom Window Node.

    Note that we map the message fields to x_field and y_field
    in self.PLOT.configure to tell the LinePlot which data is associated
    with which axis.
    """

    SIN_PLOT: LinePlot
    SQ_PLOT: LinePlot
    DAUB_PLOT: LinePlot
    HRF_PLOT: LinePlot
    WINDOW: Window

    def __init__(self) -> None:
        super().__init__()
        self.SIN_PLOT.configure(self.plot_config("Sin Wave", "sin_data"))
        self.SQ_PLOT.configure(self.plot_config("Square Wave", "square_data"))
        self.DAUB_PLOT.configure(self.plot_config("Daubechies Wave", "daub_data"))
        self.HRF_PLOT.configure(self.plot_config("HRF Wave", "hrf_data"))
        self.WINDOW.SIN_PLOT = self.SIN_PLOT
        self.WINDOW.SQ_PLOT = self.SQ_PLOT
        self.WINDOW.DAUB_PLOT = self.DAUB_PLOT
        self.WINDOW.HRF_PLOT = self.HRF_PLOT

    def plot_config(self, title, y_field) -> LinePlotConfig:
        return LinePlotConfig(
            x_field="timestamp",
            y_field=y_field,
            mode=Mode.APPEND,
            window_size=200,
            style={
                "setLabels": {
                    "title": title,
                    "left": "Value",
                    "bottom": "Lab Timestamp",
                }
            },
        )

    def process_modules(self) -> Tuple[df.Module, ...]:
        return (self.SIN_PLOT, self.SQ_PLOT, self.DAUB_PLOT, self.HRF_PLOT, self.WINDOW)


class Demo(df.Graph):
    """
    A simple graph showing how we can add our group
    """

    GENERATOR: SimulationGenerator
    VIZ: VizGroup

    def setup(self) -> None:
        self.GENERATOR.configure(
            GeneratorConfig(sample_rate=SAMPLE_RATE, num_features=NUM_FEATURES)
        )

    def connections(self) -> df.Connections:
        return (
            (self.GENERATOR.OUTPUT, self.VIZ.SIN_PLOT.INPUT),
            (self.GENERATOR.OUTPUT, self.VIZ.SQ_PLOT.INPUT),
            (self.GENERATOR.OUTPUT, self.VIZ.DAUB_PLOT.INPUT),
            (self.GENERATOR.OUTPUT, self.VIZ.HRF_PLOT.INPUT),
        )

    def process_modules(self) -> Tuple[df.Module, ...]:
        return (self.GENERATOR, self.VIZ)


if __name__ == "__main__":
    graph = Demo()
    runner = df.LocalRunner(module=graph)
    runner.run()
