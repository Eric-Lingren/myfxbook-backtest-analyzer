import pandas as pd


class Myfxbook_Report_Cleaner():
    def __init__(self, input_file, output_path):
        self.input_file = input_file
        self.output_path = output_path
        self.output_filename = ''
        self.df = None



    def run_cleaner(self):
        self.open_report()
        self.drop_withdrawls_deposits()
        self.drop_unused_columns()
        self.write_data_to_xls()
        return self.output_filename



    def open_report(self):
        self.df = pd.read_csv(self.input_file)
        output_filename = self.input_file.replace('.csv', '-cleaned.xlsx') 
        slice_index = output_filename.rfind('/')
        self.output_filename = self.output_path + output_filename[slice_index:]



    #* Drops all withdrawal and deposit orders to leave only trades
    def drop_withdrawls_deposits(self):
        self.df.drop(self.df[self.df['Action'] == 'Deposit'].index, inplace = True)
        self.df.drop(self.df[self.df['Action'] == 'Withdrawal'].index, inplace = True)



    #* Drops all Unused Columns
    def drop_unused_columns(self):
        self.df.drop(['Tags', 'SL', 'TP', 'Commission', 'Swap', 'Comment', 'Magic Number'], axis = 1, inplace = True) 



    # #*  Output the contents of the trade data table in excel format
    def write_data_to_xls(self):
        #  Create a Pandas Excel writer using XlsxWriter as the engine.
        with pd.ExcelWriter(self.output_filename, engine='xlsxwriter') as writer:    
            # Write each dataframe to a different worksheet.
            self.df.to_excel(writer, sheet_name='trade_data', index=False)
    