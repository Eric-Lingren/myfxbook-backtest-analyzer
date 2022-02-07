import tkinter as tk
from tkinter import ttk
from tkinter import Label
from tkinter import filedialog
import tkinter.font as font
from cleaners.myfxbook_report_cleaner import Myfxbook_Report_Cleaner
from reports.report_plotter import Report_Plotter


class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.chosen_input_path = ''
        self.chosen_output_path = ''
        self.init_build_app_options()
    

    def init_build_app_options(self):
        self.init_myfxbook_file_select()
        self.init_analysis_output_folder_select()
        self.init_run_button()


    #* Renders Browse Myfxbook Report Selection
    def init_myfxbook_file_select(self):
        output_path_label = Label(
            root, 
            text='Select Myfxbook Report:', 
            font=("Helvetica", 20) 
        )
        output_path_label.grid(row = 2, column = 1, pady=(40, 10))

        def getFilePath():
            self.chosen_input_path = filedialog.askopenfilename()
            output_path_text.config(text = 'Myfxbook Report Location: '+ self.chosen_input_path)

        folder_btn = ttk.Button(root, text="Browse Files",command=getFilePath)
        folder_btn.grid(row = 3, column = 1, pady=(5, 5))
        output_path_text = Label(root, text='Myfxbook Report Location: ' )
        output_path_text.grid(row = 4, column = 1, pady=(5, 5))


    #* Renders Browse Folder Output Location
    def init_analysis_output_folder_select(self):
        output_path_label = Label(
            root, 
            text='Select Report Output Location:', 
            font=("Helvetica", 20) 
        )
        output_path_label.grid(row = 5, column = 1, pady=(40, 10))

        def getFolderPath():
            self.chosen_output_path = filedialog.askdirectory()
            output_path_text.config(text = 'Analysis Report Output Location: '+ self.chosen_output_path)

        folder_btn = ttk.Button(root, text="Browse Folders",command=getFolderPath)
        folder_btn.grid(row = 6, column = 1, pady=(5, 5))
        output_path_text = Label(root, text='Analysis Report Output Location: ' )
        output_path_text.grid(row = 7, column = 1, pady=(5, 5))


    #* Download Button
    def init_run_button(self):
        download_button = tk.Button(
            root, 
            text='Run', 
            command=self.run_analyzer
        )
        download_btn_font = font.Font(family='Helvetica', size=18, weight='bold')
        download_button['font'] = download_btn_font
        download_button.grid(row = 8, column = 1, pady=(30, 5))

    
    def run_analyzer(self):
        system_paths = { 'input_file': self.chosen_input_path, 'output_path': self.chosen_output_path }
        xls_location = Myfxbook_Report_Cleaner(**system_paths).run_cleaner()
        system_paths['xls_location'] = xls_location
        del system_paths['input_file']
        Report_Plotter(**system_paths).generate_report()



#* Configures Global GUI Settings and Starts App
if __name__ == "__main__":
    root = tk.Tk()
    App(root).grid(sticky="nsew")
    root.title('Myfxbook Backtest Report Analyzer')
    root.geometry('1000x700')
    heading=Label(root, text='Myfxbook Backtest Report Analyzer', font=("Helvetica", 28))
    heading.grid(row=0, column=1, pady=(0,20))
    root.grid_columnconfigure((0, 1, 2), weight=1)
    root.mainloop()
