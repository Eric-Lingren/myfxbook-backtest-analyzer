import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import jinja2
import calendar
from datetime import datetime, timedelta
import numpy as np

from chart_generators.bar_generators import BarGenerators


class Report_Plotter():
    def __init__(self, output_path, xls_location):
        self.output_path = output_path
        self.xls_location = xls_location
        self.df = None
        # self.trades_data_df = None
        # self.summary_data_df = None
        # self.trades_duration_dataset = None
        # self.account_balance_df = None
        # self.monthly_trades_df = None
        # self.monthly_order_types_df = None
        # self.monthly_profits_df = None


    def generate_report(self):
        self.load_data()
        self.generate_duration_timedeltas()
        # self.generate_account_balance_df()
        # self.generate_monthly_trades_df()
        # self.generate_monthly_profits_df()
        self.build_html_report()
    

    #* Load data from excel into dataframes
    def load_data(self):
        self.df = pd.read_excel(self.xls_location, sheet_name='trade_data')  
        


    def generate_trade_action_chart(self):
        action_type_counts = self.df['Action'].value_counts().rename_axis('Action').reset_index(name='Count')
        chart_params = {
            'data' : action_type_counts,
            'title' : 'Total Trades By Direction',
            'x' : action_type_counts['Action'],
            'y' : action_type_counts['Count'],
            'labels' : None,
            'legend' : None
        }
        return BarGenerators().generate_bar_chart(chart_params)



    def generate_trade_assets_chart(self):
        asset_counts = self.df['Symbol'].value_counts().rename_axis('Symbol').reset_index(name='Count')
        chart_params = {
            'data' : asset_counts,
            'title' : 'Total Trades By Asset',
            'x' : asset_counts['Symbol'],
            'y' : asset_counts['Count'],
            'labels' : None,
            'legend' : None
        }
        return BarGenerators().generate_bar_chart(chart_params)



    def generate_duration_timedeltas(self):
        self.df['Duration Delta'] = ''
        self.df['Duration Seconds'] = ''
        for i, row in self.df.iterrows():
            duration_value = row['Duration (DD:HH:MM:SS)']
            index = duration_value.find(':')
            days = int(duration_value[:index])
            hours = int(duration_value[index+1:index+3])
            minutes = int(duration_value[index+4:index+6])
            seconds = int(duration_value[index+7:])
            time_delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
            self.df.at[i, 'Duration Delta'] = time_delta
            self.df.at[i, 'Duration Seconds'] = time_delta.total_seconds()




    def generate_average_duration_by_action_chart(self):
        print(self.df.head())
        print(self.df.columns.to_list())

        new = self.df[['Symbol','Duration Seconds']].copy()
        print(new)

        means = new.groupby('Symbol').mean()
        # means['new'] = pd.to_timedelta(means['new'])
        print(means)

        std = new.groupby('Symbol').std()
        # std['new'] = pd.to_timedelta(std['new'])
        print(std)

        # asset_counts = self.df['Symbol'].value_counts().rename_axis('Symbol').reset_index(name='Count')
        # chart_params = {
        #     'data' : asset_counts,
        #     'title' : 'Total Trades By Asset',
        #     'x' : asset_counts['Symbol'],
        #     'y' : asset_counts['Count'],
        #     'labels' : None,
        #     'legend' : None
        # }
        # return BarGenerators().generate_bar_chart(chart_params)




    # def generate_account_balance_df(self):
    #     account_balance_dataset = self.trades_data_df.filter(['Profit', 'Balance'], axis=1)
    #     self.account_balance_df = account_balance_dataset[account_balance_dataset['Profit'].notna()]


    # #* Builds the data to count order types by months
    # def generate_monthly_trades_df(self):
    #     monthly_trades_dataset = self.trades_data_df.filter(['Time','Type','Profit'], axis=1)
    #     monthly_trades_dataset['Month'] = pd.DatetimeIndex(monthly_trades_dataset['Time']).month
    #     monthly_trades_dataset['Month'] = monthly_trades_dataset['Month'].apply(lambda x: calendar.month_abbr[x])
    #     self.monthly_trades_df = monthly_trades_dataset
    #     count_series = monthly_trades_dataset.groupby(['Month', 'Type',]).size().reset_index()
    #     count_series = count_series.pivot_table(0, ['Month'], 'Type').fillna(0)
    #     cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    #     count_series.index = pd.CategoricalIndex(count_series.index, categories=cats, ordered=True)
    #     self.monthly_order_types_df = count_series.sort_index()


    # #* Builds the data to evalutate Net Profit by months
    # def generate_monthly_profits_df(self):
    #     profit_series = self.monthly_trades_df.groupby(['Month', 'Profit',]).size().reset_index()
    #     profit_series['Total'] = profit_series.groupby(['Month'])['Profit'].transform('sum')
    #     profit_series = profit_series.drop_duplicates(subset=['Month']).reset_index(drop=True)
    #     cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    #     profit_series.set_index('Month', inplace=True)
    #     profit_series.index = pd.CategoricalIndex(profit_series.index, categories=cats, ordered=True)
    #     profit_series = profit_series.sort_index()
    #     self.monthly_profits_df = profit_series

    
    def build_html_report(self): # Obtain Template
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "/reports/template.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        self.inject_html_data(template)

    
    # #* Inject Data into HTML Template
    def inject_html_data(self, template): # Populate Template
        output_html= template.render(
    #         #! Report Text:
    #         system_name = self.get_system_name(),
    #         symbol = self.get_equity(),
    #         period = self.get_period(),
    #         duration = self.get_duration(),
    #         bars = self.get_bars(),
    #         ticks_modeled = self.get_ticks_modeled(),
    #         modelling_quality = self.get_modeling_quality(),
    #         mismatched_charts_errors = self.get_mismatched_chart_errors(),
    #         gross_profit = self.get_gross_profit(),
    #         gross_loss = self.get_gross_loss(),
    #         net_profit = self.get_net_profit(),
    #         absolute_drawdown = self.get_absolute_drawdown(),
    #         maximal_drawdown = self.get_max_drawdown(),
    #         relative_drawdown = self.get_relative_drawdown(),
    #         total_trades = self.get_total_positions_count(),
    #         short_positions = self.get_short_postions_count(),
    #         long_positions = self.get_long_postions_count(),
    #         largest_profit_trade = self.get_largest_profitable_trade(),
    #         largest_loss_trade = self.get_largest_unprofitable_trade(),
    #         average_profit_trade = self.get_average_profit_per_trade() ,
    #         average_loss_trade = self.get_average_loss_per_trade(),
    #         max_consecutive_wins = self.get_max_consecutive_wins(),
    #         max_consecutive_losses = self.get_max_consecutive_losses() ,
    #         max_consecutive_profit = self.get_max_consecutive_profit_amt(),
    #         max_consecutive_loss = self.get_max_consecutive_loss_amt(),
    #         average_consecutive_wins = self.get_avg_consecutive_win_count(),
    #         average_consecutive_losses = self.get_avg_consecutive_loss_count(),
    #         #! Report Charts:
    #         account_balance_fig_jpeg = self.generate_line_chart({
    #             'data' : self.account_balance_df,
    #             'title' : 'Net Account Balance',
    #             'y' : 'Balance',
    #             'labels' : {"index":"Trade"},
    #         }),
    #         monthly_profit_fig_jpeg = self.generate_bar_chart({
    #             'data' : self.monthly_profits_df,
    #             'title' : 'Total Net Profit by Month',
    #             'x' : self.monthly_profits_df.index,
    #             'y' : self.monthly_profits_df['Total'],
    #             'labels' : {"Total":"Profit in $"},
    #             'legend' : {'title_text':'Order Type'}
    #         }),
    #         monthly_trades_fig_jpeg = self.generate_bar_chart({
    #             'data' : self.monthly_order_types_df,
    #             'title' : 'Order Type Count by Month',
    #             'x' : self.monthly_order_types_df.index,
    #             'y' : ['buy', 'sell', 'close', 'close at stop'],
    #             'labels' : {"value":"Count"},
    #             'legend' : {'title_text':'Order Type'}
    #         }),
            fig1_jpeg = self.generate_trade_action_chart(),
            fig2_jpeg = self.generate_trade_assets_chart(),
            fig3_jpeg = self.generate_average_duration_by_action_chart(),
    #         fig2_jpeg = self.generate_heatmap({
    #             'data' : self.trades_duration_dataset,
    #             'x' : 'Duration (hrs)',
    #             'y' : 'Profit',
    #             'nbinsx' : 50,
    #             'nbinsy' : 20
    #         }),
    #         fig4_jpeg = self.generate_2d_histogram_contour({
    #             'x' : self.trades_duration_dataset['Duration (hrs)'],
    #             'y' : self.trades_duration_dataset['Profit'],
    #         }),
    #         # fig6_jpeg = self.generate_density_contour({
    #         #     'data' : self.trades_duration_dataset,
    #         #     'x' : self.trades_duration_dataset['Duration (hrs)'],
    #         #     'y' : self.trades_duration_dataset['Profit'],
    #         # }),
    #         fig6_jpeg = self.generate_histogram({
    #             'data' : self.trades_duration_dataset,
    #             'x' : 'Duration (hrs)',
    #             'nbins' : 20,
    #         }),
        ) 

        with open(self.xls_location[:-5] + '.html', "w") as f:
            f.write(output_html)







    # def get_system_name(self):
    #     system_name = self.summary_data_df.loc[self.summary_data_df['Key'] == 'System Name']
    #     return system_name.iloc[0]['Value']
    
    # def get_equity(self):
    #     symbol_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Symbol']
    #     return symbol_data.iloc[0]['Value']
    
    # def get_period(self):
    #     period_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Period']
    #     return period_data.iloc[0]['Value']

    # def get_duration(self):
    #     duration_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Duration']
    #     return duration_data.iloc[0]['Value']

    # def get_bars(self):
    #     bars_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Bars in test']
    #     return bars_data.iloc[0]['Value']
    
    # def get_ticks_modeled(self):
    #     ticks_modeled_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Ticks modelled']
    #     return ticks_modeled_data.iloc[0]['Value']
    
    # def get_modeling_quality(self):
    #     modelling_quality_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Modelling quality']
    #     return modelling_quality_data.iloc[0]['Value']

    # def get_mismatched_chart_errors(self):
    #     mismatched_charts_errors = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Mismatched charts errors']
    #     return mismatched_charts_errors.iloc[0]['Value']

    # def get_gross_profit(self):
    #     gross_profit = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Gross profit']
    #     return gross_profit.iloc[0]['Value']

    # def get_gross_loss(self):
    #     gross_loss = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Gross loss']
    #     return gross_loss.iloc[0]['Value']

    # def get_net_profit(self):
    #     net_profit = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Total net profit']
    #     return net_profit.iloc[0]['Value']

    # def get_absolute_drawdown(self):
    #     absolute_drawdown = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Absolute drawdown']
    #     return absolute_drawdown.iloc[0]['Value']

    # def get_max_drawdown(self):
    #     maximal_drawdown = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Maximal drawdown']
    #     return  maximal_drawdown.iloc[0]['Value']

    # def get_relative_drawdown(self):
    #     relative_drawdown = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Relative drawdown']
    #     relative_drawdown_value = relative_drawdown.iloc[0]['Value']
    #     slice_index = relative_drawdown_value.find('(')
    #     relative_drawdown_dollar = relative_drawdown_value[slice_index+1:-1]
    #     relative_drawdown_percent = relative_drawdown_value[:slice_index-1]
    #     return relative_drawdown_dollar + ' (' + relative_drawdown_percent + ')'
    
    # def get_total_positions_count(self):
    #     total_trades = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Total trades']
    #     return total_trades.iloc[0]['Value']
    
    # def get_short_postions_count(self):
    #     short_positions = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Short positions (won %)']
    #     return short_positions.iloc[0]['Value']

    # def get_long_postions_count(self):
    #     long_positions = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Long positions (won %)']
    #     return long_positions.iloc[0]['Value']
    
    # def get_largest_profitable_trade(self):
    #     largest_profit_trade = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Largest profit trade']
    #     return largest_profit_trade.iloc[0]['Value']
    
    # def get_largest_unprofitable_trade(self):
    #     largest_loss_trade = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Largest loss trade']
    #     return largest_loss_trade.iloc[0]['Value']

    # def get_average_profit_per_trade(self):
    #     average_profit_trade = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Average profit trade']
    #     return  average_profit_trade.iloc[0]['Value']
    
    # def get_average_loss_per_trade(self):
    #     average_loss_trade = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Average loss trade']
    #     return average_loss_trade.iloc[0]['Value']
    
    # def get_max_consecutive_wins(self):
    #     max_consecutive_wins = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Maximum consecutive wins (profit in money)']
    #     return max_consecutive_wins.iloc[0]['Value']

    # def get_max_consecutive_losses(self):
    #     max_consecutive_losses = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Maximum consecutive losses (loss in money)']
    #     return max_consecutive_losses.iloc[0]['Value']

    # def get_max_consecutive_profit_amt(self):
    #     max_consecutive_profit = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Maximal consecutive profit (count of wins)']
    #     return max_consecutive_profit.iloc[0]['Value']
    
    # def get_max_consecutive_loss_amt(self):
    #     max_consecutive_loss = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Maximal consecutive loss (count of losses)']
    #     return  max_consecutive_loss.iloc[0]['Value']

    # def get_avg_consecutive_win_count(self):
    #     average_consecutive_wins = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Average consecutive wins']
    #     return average_consecutive_wins.iloc[0]['Value']

    # def get_avg_consecutive_loss_count(self):
    #     average_consecutive_losses = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Average consecutive losses']
    #     return average_consecutive_losses.iloc[0]['Value']