from operator import itemgetter
import plotly.graph_objects as go
import plotly.express as px


class HistogramGenerators():

    def generate_2d_histogram_contour(self, chart_params):
        x, y = itemgetter('x', 'y')(chart_params)
        histogram_contour_fig = go.Figure(go.Histogram2dContour(
            x=x, 
            y=y,
            colorscale = 'Jet',
            contours = dict(
                showlabels = True,
                labelfont = dict(
                    family = 'Raleway',
                    color = 'white'
                )
            ),
            hoverlabel = dict(
                bgcolor = 'white',
                bordercolor = 'black',
                font = dict(
                    family = 'Raleway',
                    color = 'black'
                )
            )
        ))
        histogram_contour_jpeg = self.convert_chart_figure_to_jpeg(histogram_contour_fig)
        return histogram_contour_jpeg



    def generate_histogram(self, chart_params):
        data, x, nbins = itemgetter('data', 'x', 'nbins')(chart_params)
        histogram_fig = px.histogram(
            data, 
            x=x, 
            nbins=nbins
        )
        histogram_jpeg = self.convert_chart_figure_to_jpeg(histogram_fig)
        return histogram_jpeg