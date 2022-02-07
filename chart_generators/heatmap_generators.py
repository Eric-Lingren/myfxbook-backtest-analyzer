from operator import itemgetter
import plotly.express as px


class HeatmapGenerators():

    def generate_heatmap(self, chart_params):
        data, x, y, nbinsx, nbinsy = itemgetter('data', 'x', 'y', 'nbinsx', 'nbinsy')(chart_params)
        heatmap_fig = px.density_heatmap(
            data, 
            x=x, 
            y=y, 
            nbinsx=nbinsx, 
            nbinsy=nbinsy
        )
        heatmap_jpeg = self.convert_chart_figure_to_jpeg(heatmap_fig)
        return heatmap_jpeg