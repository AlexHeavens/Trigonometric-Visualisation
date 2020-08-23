import math
import shapely.geometry as geometry

from bokeh.io import curdoc
from bokeh.layouts import column, row
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


def update_data_sources(data_sources, angle_in_radians, radius):
    def update_linestring_data_source(linestring, data_source):
        x, y = linestring.xy
        data_source.data = dict(x=x, y=y)

    geometries = get_trig_geometries(angle_in_radians=angle_in_radians, radius=radius)

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


def plot_trig_geometries(plot, data_sources):

    plot.line(
        "x",
        "y",
        source=data_sources["radial_coordinates"],
        color="green",
        line_width=3,
        line_alpha=0.6,
    )
    plot.line(
        "x",
        "y",
        source=data_sources["opposite_coordinates"],
        color="blue",
        line_width=3,
        line_alpha=0.6,
    )
    plot.line(
        "x",
        "y",
        source=data_sources["adjacent_coordinates"],
        color="red",
        line_width=3,
        line_alpha=0.6,
    )


def main():
    angular_resolution = 0.05
    radius = 100

    angle_in_radians_slider = Slider(
        title="angle (radians)",
        value=1.0,
        start=-2 * math.pi,
        end=2 * math.pi,
        step=angular_resolution,
    )

    plot = figure(
        plot_height=radius * 4,
        plot_width=radius * 4,
        title="Trigonometric Values",
        tools="crosshair,reset,save",
        x_range=[-radius * 1.5, radius * 1.5],
        y_range=[-radius * 1.5, radius * 1.5],
    )

    data_sources = dict(
        radial_coordinates=ColumnDataSource(),
        opposite_coordinates=ColumnDataSource(),
        adjacent_coordinates=ColumnDataSource(),
    )

    angle_in_radians = angle_in_radians_slider.value
    plot_trig_geometries(plot=plot, data_sources=data_sources)
    update_data_sources(
        data_sources=data_sources, angle_in_radians=angle_in_radians, radius=radius
    )

    def update(attr, old, new):
        update_data_sources(
            data_sources=data_sources,
            angle_in_radians=angle_in_radians_slider.value,
            radius=radius,
        )

    angle_in_radians_slider.on_change("value", update)

    # Set up layouts and add to document
    inputs = column(angle_in_radians_slider)

    curdoc().add_root(row(inputs, plot, width=800))
    curdoc().title = "Trigonometry Values"


main()