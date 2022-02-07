from operator import itemgetter
import plotly.express as px


class ScatterGenerators():

    def generate_scatter_plot(self, chart_params):
        data, x, y, height, width = itemgetter('data', 'x', 'y', 'height', 'width')(chart_params)
        scatter_plot_fig = px.scatter(
            data, 
            x=x, 
            y=y, 
            height=height,
            width=width, 
        )
        scatter_plot_jpeg = self.convert_chart_figure_to_jpeg(scatter_plot_fig)
        return scatter_plot_jpeg
