import math
import numpy as np
import shapely.geometry as geometry

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure


def get_trig_geometries(angle_in_radians: float, radius: float):
    sin_of_angle = math.sin(angle_in_radians)
    cos_of_angle = math.cos(angle_in_radians)

    hypotenuse_length = radius
    opposite_length = hypotenuse_length * sin_of_angle
    adjacent_lenth = hypotenuse_length * cos_of_angle

    radial_line = geometry.LineString([(0, 0), (adjacent_lenth, opposite_length)])
    opposite_line = geometry.LineString(
        [(adjacent_lenth, 0), (adjacent_lenth, opposite_length)]
    )
    adjacent_line = geometry.LineString([(0, 0), (adjacent_lenth, 0)])

    return {
        "radial_line": radial_line,
        "opposite_line": opposite_line,
        "adjacent_line": adjacent_line,
    }


def update_data_sources(data_sources):
    def update_linestring_data_source(linestring, data_source):
        x, y = linestring.xy
        data_source.data = dict(x=x, y=y)

    geometries = get_trig_geometries(
        angle_in_radians=data_sources["angle_in_radians"], radius=data_sources["radius"]
    )

    update_linestring_data_source(
        linestring=geometries["radial_line"],
        data_source=data_sources["radial_coordinates"],
    )
    update_linestring_data_source(
        linestring=geometries["opposite_line"],
        data_source=data_sources["opposite_coordinates"],
    )
    update_linestring_data_source(
        linestring=geometries["adjacent_line"],
        data_source=data_sources["adjacent_coordinates"],
    )


def create_circle_figure(data_sources):

    radius = data_sources["radius"]

    def plot_radius_circle():
        circle = geometry.Point((0, 0)).buffer(radius).exterior.coords

        circle_figure.line(*circle.xy, color="gray", line_width=2, line_alpha=0.6)

    def plot_trig_geometries():

        circle_figure.line(
            "x",
            "y",
            source=data_sources["radial_coordinates"],
            color="green",
            line_width=3,
            line_alpha=0.6,
        )
        circle_figure.line(
            "x",
            "y",
            source=data_sources["opposite_coordinates"],
            color="blue",
            line_width=3,
            line_alpha=0.6,
        )
        circle_figure.line(
            "x",
            "y",
            source=data_sources["adjacent_coordinates"],
            color="red",
            line_width=3,
            line_alpha=0.6,
        )

    circle_figure = figure(
        plot_height=int(radius * 4),
        plot_width=int(radius * 4),
        title="Trigonometric Values",
        tools="crosshair,reset,save",
        x_range=[-radius * 1.5, radius * 1.5],
        y_range=[-radius * 1.5, radius * 1.5],
    )

    plot_radius_circle()
    plot_trig_geometries()

    return circle_figure


def create_trig_figure(trig_function, linear_resolution, color):

    x_range = [-2.0 * math.pi - 1.0, 2.0 * math.pi + 1.0]
    trig_figure = figure(
        plot_height=300,
        plot_width=600,
        title=trig_function.__name__,
        tools="crosshair,reset,save",
        x_range=x_range,
        y_range=[-1.2, 1.2],
    )
    xs = np.arange(x_range[0], x_range[1], linear_resolution)
    ys = trig_function(xs)
    trig_figure.line(xs, ys, line_color=color)
    return trig_figure


def main():

    data_sources = dict(
        radial_coordinates=ColumnDataSource(),
        opposite_coordinates=ColumnDataSource(),
        adjacent_coordinates=ColumnDataSource(),
        radius=100.0,
        angular_resolution=0.05,
        linear_resolution=0.1,
        angle_in_radians=1.0,
    )
    linear_resolution = data_sources["linear_resolution"]
    update_data_sources(data_sources)

    circle_figure = create_circle_figure(data_sources=data_sources)
    sin_figure = create_trig_figure(
        trig_function=np.sin, linear_resolution=linear_resolution, color="blue"
    )
    cos_figure = create_trig_figure(
        trig_function=np.cos, linear_resolution=linear_resolution, color="red"
    )
    tan_figure = create_trig_figure(
        trig_function=np.tan, linear_resolution=linear_resolution, color="purple"
    )

    angle_in_radians_slider = Slider(
        title="angle (radians)",
        value=data_sources["angle_in_radians"],
        start=-2 * math.pi,
        end=2 * math.pi,
        step=data_sources["angular_resolution"],
    )

    def update(attr, old, new):
        data_sources["angle_in_radians"] = angle_in_radians_slider.value
        update_data_sources(data_sources)

    angle_in_radians_slider.on_change("value", update)

    # Set up layouts and add to document
    inputs = column(angle_in_radians_slider)

    curdoc().add_root(
        column(inputs, circle_figure, sin_figure, cos_figure, tan_figure, width=800)
    )
    curdoc().title = "Trigonometry Values"


main()
