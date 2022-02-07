import plotly.express as px
from operator import itemgetter
from chart_generators.utilities import convert_chart_figure_to_jpeg

class BarGenerators():

    def generate_bar_chart(self, chart_params):
        data, title, x, y, labels, legend = itemgetter('data', 'title', 'x', 'y', 'labels', 'legend')(chart_params)
        bar_fig = px.bar(
            data, 
            title=title,
            x=x, 
            y=y, 
            text_auto=True,
            labels=labels, 
        )
        bar_fig.update_layout(barmode='relative')
        bar_fig.update_layout(legend=legend)
        bar_chart_jpeg = convert_chart_figure_to_jpeg(bar_fig)
        return bar_chart_jpeg