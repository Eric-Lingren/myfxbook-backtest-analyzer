from msilib.schema import Class
from operator import itemgetter
import plotly.express as px


class ContourGenerator():

    def generate_density_contour(self, chart_params):
        data, x, y = itemgetter('data', 'x', 'y')(chart_params)
        density_contour_fig = px.density_contour(
            data,     
            x=x, 
            y=y
        )
        density_contour_fig.update_traces(contours_coloring="fill", contours_showlabels = True)
        density_contour_jpeg = self.convert_chart_figure_to_jpeg(density_contour_fig)
        return density_contour_jpeg