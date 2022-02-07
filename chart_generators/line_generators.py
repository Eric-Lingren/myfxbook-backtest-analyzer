from operator import itemgetter
import plotly.express as px

class LineGenerators():

    def generate_line_chart(self, chart_params):
        data, title, y, labels = itemgetter('data', 'title', 'y', 'labels')(chart_params)
        line_fig = px.line(
            data, 
            title=title,
            y=y, 
            labels=labels, 
            color_discrete_sequence=["#00FF00"] 
        )
        line_chart_jpeg = self.convert_chart_figure_to_jpeg(line_fig)
        return line_chart_jpeg