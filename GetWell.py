
from select import select
import SeisWare
import tkinter as tk
import tkinter.ttk as ttk
import threading
import pandas as pd
import openpyxl
import os
import matplotlib.pyplot as plt
import numpy as np  # Import NumPy
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Button
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

from matplotlib.widgets import Cursor
import numpy as np
import Map
import subprocess


from tkinter import messagebox
import sys
sys.path.append('C:/Users/jerem/AppData/Local/Programs/Python/Python311/Lib/site-packages')


def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()

    root.protocol('WM_DELETE_WINDOW', root.destroy)
    _w1 = ImageGUI(root)
    map_window = Map.MapWindow()
    map_window.map_data()
    root.mainloop()
    _w1.run()

class ImageGUI:

    # MAING DIALOG BUILDING
    def __init__(self, top=None):
        self.top = top

        self.top.geometry("700x700+590+257")
        self.top.minsize(120, 1)
        self.top.maxsize(6500, 1181)
        self.top.resizable(1, 1)

        self.top.title("Deviation Analyzer")
        self.top.configure(background="white")

        self.connection = None
        self.connection = None
        self.project_var = tk.StringVar()
        self.well_list = None
        self.project_names = None
        self.project_list = None
        self.curve_calibration_dict = {}
        self.filter_name = None
        self.grid_xyz_top = []





        self.label_config = {
            "background": "white",
            "foreground": "#000000",
            "anchor": 'w'
        }

        self.project_selection = tk.StringVar(value=None)
        self.project_dropdown = ttk.OptionMenu(self.top, self.project_selection, "", command=self.on_project_select)
        self.project_label = tk.Label(self.top, text="Project:")
        self.project_label.configure(**self.label_config)
        self.project_label.place(relx=0.01, rely=0.005, relwidth=0.09)
        
        self.filter_selection = tk.StringVar(value=None)
        self.filter_label = tk.Label(self.top, text="Well Filter:")
        self.filter_label.configure(**self.label_config)
        self.filter_dropdown = ttk.OptionMenu(self.top, self.filter_selection, "", command=self.on_filter_select)
        self.filter_label.place(relx=0.01, rely=0.035, relwidth=0.09)


        self.uwi_listbox = tk.Listbox(self.top, selectmode=tk.MULTIPLE)
        self.uwi_listbox.place(relx=0.01, rely=0.09, relwidth=0.44, relheight=0.6)
        #self.uwi_listbox.bind('<<ListboxSelect>>', self.on_uwi_select)

        self.selected_uwi_listbox = tk.Listbox(self.top, selectmode=tk.MULTIPLE)
        self.selected_uwi_listbox.place(relx=0.53, rely=0.09, relwidth=0.44, relheight=0.6)
        #self.selected_uwi_listbox.bind('<<ListboxSelect>>', self.on_selected_uwi_select)
        
        # Bind mouse events for moving items
        self.uwi_listbox.bind("<ButtonPress-1>", self.on_uwi_listbox_click)
        self.uwi_listbox.bind("<B1-Motion>", self.on_uwi_listbox_drag)
        self.selected_uwi_listbox.bind("<ButtonPress-1>", self.on_selected_uwi_listbox_click)
        self.selected_uwi_listbox.bind("<B1-Motion>", self.on_selected_uwi_listbox_drag)

        # Create a vertical scrollbar for uwi_listbox
        self.uwi_listbox_scrollbar = tk.Scrollbar(self.top, orient=tk.VERTICAL)
        self.uwi_listbox_scrollbar.place(relx=0.44, rely=0.09, relheight=0.6)
        self.uwi_listbox.config(yscrollcommand=self.uwi_listbox_scrollbar.set)
        self.uwi_listbox_scrollbar.config(command=self.uwi_listbox.yview)


        # Create a vertical scrollbar for selected_uwi_listbox
        self.selected_uwi_listbox_scrollbar = tk.Scrollbar(self.top, orient=tk.VERTICAL)
        self.selected_uwi_listbox_scrollbar.place(relx=0.96, rely=0.09, relheight=0.6)
        self.selected_uwi_listbox.config(yscrollcommand=self.selected_uwi_listbox_scrollbar.set)
        self.selected_uwi_listbox_scrollbar.config(command=self.selected_uwi_listbox.yview)

                # Create a button to move selected items from uwi_listbox to selected_uwi_listbox
        self.move_right_button = tk.Button(self.top, text=">", command=self.move_selected_right)
        self.move_right_button.place(relx=0.47, rely=0.35, relwidth=0.05)

        # Create a button to move selected items from selected_uwi_listbox to uwi_listbox
        self.move_left_button = tk.Button(self.top, text="<", command=self.move_selected_left)
        self.move_left_button.place(relx=0.47, rely=0.4, relwidth=0.05)

                # Create a button to move all items from uwi_listbox to selected_uwi_listbox
        self.move_all_right_button = tk.Button(self.top, text=">>", command=self.move_all_right)
        self.move_all_right_button.place(relx=0.47, rely=0.3, relwidth=0.05)

        # Create a button to move all items from selected_uwi_listbox to uwi_listbox
        self.move_all_left_button = tk.Button(self.top, text="<<", command=self.move_all_left)
        self.move_all_left_button.place(relx=0.47, rely=0.45, relwidth=0.05)
        # Create a context menu for listboxes
        self.context_menu = tk.Menu(self.top, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_selected_item)

        # Bind the right-click event to show the context menu
        self.uwi_listbox.bind("<Button-3>", self.show_context_menu)
        self.selected_uwi_listbox.bind("<Button-3>", self.show_context_menu)




        self.export_label = tk.Label(self.top, text="Export:")
        self.export_label.configure(**self.label_config)
        self.export_label.place(relx=0.01, rely=0.90, relwidth=0.1)
        self.export_button = tk.Button(self.top, text="Export", command=self.export)
        self.export_button.place(relx=0.15, rely=0.90, relwidth=0.2)

        self.plot_label = tk.Label(self.top, text="Plot:")
        self.plot_label.configure(**self.label_config)
        self.plot_label.place(relx=0.01, rely=0.94, relwidth=0.1)
        self.plot_button = tk.Button(self.top, text="Plot", command=self.plot_data)
        self.plot_button.place(relx=0.15, rely=0.94, relwidth=0.2)

        self.map_label = tk.Label(self.top, text="Plot:")
        self.map_label.configure(**self.label_config)
        self.map_label.place(relx=0.01, rely=0.84, relwidth=0.1)
        self.map_button = tk.Button(self.top, text="Map", command=self.map_data)
        self.map_button.place(relx=0.15, rely=0.84, relwidth=0.2)


        # Hide the label and dropdown initially
        self.project_label.place_forget()
        self.project_dropdown.place_forget()
        self.filter_label.place_forget()
        self.filter_dropdown.place_forget()
        self.connection = SeisWare.Connection()
        self.connect_to_seisware()
        self.login_instance = SeisWare.LoginInstance()
        self.grid_df = pd.DataFrame() 
        self.directional_survey_values = []
        self.directional_survey_values = []
        self.Grid_intersec_top = []
        self.Grid_intersec_bottom = []
        self.selected_item = None
        self.uwis_and_offsets = []
        self.line_segments = [] 
        self.drawing = False
        self.line = None
        self.x_data = []
        self.y_data = []
        self.canvas = None



    def show_context_menu(self, event):
        # Get the widget that triggered the event
        source_widget = event.widget

        if source_widget == self.uwi_listbox:
            # The event originated from self.uwi_listbox
            # Deselect all items in both listboxes
            self.uwi_listbox.selection_clear(0, tk.END)
            self.selected_uwi_listbox.selection_clear(0, tk.END)

            # Find the closest item to the right-click position in self.uwi_listbox
            nearest_index = self.uwi_listbox.nearest(event.y)

            # Select the closest item in self.uwi_listbox
            self.uwi_listbox.selection_set(nearest_index)
            self.selected_item = self.uwi_listbox.get(nearest_index)
        elif source_widget == self.selected_uwi_listbox:
            # The event originated from self.selected_uwi_listbox
            # Deselect all items in both listboxes
            self.uwi_listbox.selection_clear(0, tk.END)
            self.selected_uwi_listbox.selection_clear(0, tk.END)

            # Find the closest item to the right-click position in self.selected_uwi_listbox
            nearest_index = self.selected_uwi_listbox.nearest(event.y)

            # Select the closest item in self.selected_uwi_listbox
            self.selected_uwi_listbox.selection_set(nearest_index)
            self.selected_item = self.selected_uwi_listbox.get(nearest_index)  # Corrected here

        # Display the context menu at the cursor position
        self.context_menu.post(event.x_root, event.y_root)

    def copy_selected_item(self):
        if self.selected_item:
            self.top.clipboard_clear()
            self.top.clipboard_append(self.selected_item)
            self.top.update()


 
    # Create a tkinter window (app) and the listboxes, and configure the context menu





    def on_uwi_listbox_click(self, event):
        index = self.uwi_listbox.nearest(event.y)
        self.uwi_listbox.anchor = index
        self.uwi_listbox.selection_clear(0, tk.END)
        self.uwi_listbox.selection_set(index)

    def on_uwi_listbox_drag(self, event):
        if self.uwi_listbox.anchor is not None:
            index = self.uwi_listbox.nearest(event.y)
            self.uwi_listbox.selection_clear(0, tk.END)
            self.uwi_listbox.selection_set(self.uwi_listbox.anchor, index)
            

    def on_selected_uwi_listbox_click(self, event):
        index = self.selected_uwi_listbox.nearest(event.y)
        self.selected_uwi_listbox.anchor = index
        self.selected_uwi_listbox.selection_clear(0, tk.END)
        self.selected_uwi_listbox.selection_set(index)

    def on_selected_uwi_listbox_drag(self, event):
        if self.selected_uwi_listbox.anchor is not None:
            index = self.selected_uwi_listbox.nearest(event.y)
            self.selected_uwi_listbox.selection_clear(0, tk.END)
            self.selected_uwi_listbox.selection_set(self.selected_uwi_listbox.anchor, index)
    def move_selected_right(self):
        selected_indices = self.uwi_listbox.curselection()
        items_to_move = [self.uwi_listbox.get(index) for index in selected_indices]

        # Iterate over the items to move and delete them one by one
        for item in items_to_move:
            self.uwi_listbox.delete(self.uwi_listbox.get(0, tk.END).index(item))

        # Insert the deleted items into the selected_uwi_listbox
        for item in items_to_move:
            self.selected_uwi_listbox.insert(tk.END, item)

        self.store_uwis_and_offsets()
    def move_selected_left(self):
        selected_indices = self.selected_uwi_listbox.curselection()
        items_to_move = [self.selected_uwi_listbox.get(index) for index in selected_indices]

        # Iterate over the items to move and delete them one by one
        for item in items_to_move:
            self.selected_uwi_listbox.delete(self.selected_uwi_listbox.get(0, tk.END).index(item))

        # Insert the deleted items into the uwi_listbox
        for item in items_to_move:
            self.uwi_listbox.insert(tk.END, item)

    def move_all_right(self):
        items_to_move = list(self.uwi_listbox.get(0, tk.END))

        # Delete all items from uwi_listbox
        self.uwi_listbox.delete(0, tk.END)

        # Insert all items into selected_uwi_listbox
        for item in items_to_move:
            self.selected_uwi_listbox.insert(tk.END, item)
        self.store_uwis_and_offsets()
        
    def move_all_left(self):
        items_to_move = list(self.selected_uwi_listbox.get(0, tk.END))

        # Delete all items from selected_uwi_listbox
        self.selected_uwi_listbox.delete(0, tk.END)

        # Insert all items into uwi_listbox
        for item in items_to_move:
            self.uwi_listbox.insert(tk.END, item)

        
    def connect_to_seisware(self):
        # Connect to API
        self.connection = SeisWare.Connection()
        try:
            serverInfo = SeisWare.Connection.CreateServer()
            self.connection.Connect(serverInfo.Endpoint(), 5000)
        except RuntimeError as err:
            messagebox.showerror("Connection Error", f"Failed to connect to the server: {err}")
            return

        self.project_list = SeisWare.ProjectList()
        try:
            self.connection.ProjectManager().GetAll(self.project_list)
        except RuntimeError as err:
            messagebox.showerror("Error", f"Failed to get the project list from the server: {err}")
            return

                # Put project names in Dropdown
        self.project_names = [project.Name() for project in self.project_list]
        self.project_selection = tk.StringVar(value=None)

        # Create the OptionMenu with the updated project_names
        self.project_dropdown = ttk.OptionMenu(self.top, self.project_selection, "", *self.project_names,command=self.on_project_select)


        # Show the label and dropdown
        self.project_label.place(relx=0.01, rely=0.005, relwidth=0.1)
        self.project_dropdown.place(relx=0.15, rely=0.005, relwidth=0.2)
       

    def clear_widgets(self):
        # Clear the UWI listbox and selected UWI listbox
        if hasattr(self, 'uwi_listbox') and self.uwi_listbox:
            self.uwi_listbox.delete(0, 'end')

        if hasattr(self, 'selected_uwi_listbox') and self.selected_uwi_listbox:
            self.selected_uwi_listbox.delete(0, 'end')

        # Clear the grid_combobox and grid_bottom_combobox
        if hasattr(self, 'grid_combobox') and self.grid_combobox:
            self.grid_combobox.delete(0, 'end')

        if hasattr(self, 'grid_bottom_combobox') and self.grid_bottom_combobox:
            self.grid_bottom_combobox.delete(0, 'end')

        # Clear the planned_uwi entry field
        if hasattr(self, 'planned_uwi') and self.planned_uwi:
            self.planned_uwi.delete(0, 'end')

    def on_project_select(self, event):
                # Clear the content of the list selectors
        self.clear_widgets()

        #self.connection = SeisWare.Connection()
        self.login_instance = SeisWare.LoginInstance()


        # Clear previous selections and values
        self.filter_selection.set("")  # Clear the filter selection

        # Clear the filter dropdown if it exists
        try:
            self.filter_dropdown.set("")
        except AttributeError:
            pass

        # Clear the well UWI selection if it exists
        try:
            self.planned_uwi.set("")
        except AttributeError:
            pass

        # Clear the top grid selection if it exists
        try:
            self.grid_combobox.set("")
        except AttributeError:
            pass

        # Clear the bottom grid selection if it exists
        try:
            self.grid_bottom_combobox.set("")
        except AttributeError:
            pass
        
        project_name = self.project_selection.get()
        self.projects = [project for project in self.project_list if project.Name() == project_name]
        if not self.projects:
            messagebox.showerror("Error", "No project was found")
            sys.exit(1)

        
        try:
            self.login_instance.Open(self.connection, self.projects[0])
        except RuntimeError as err:
            messagebox.showerror("Error", "Failed to connect to the project: " + str(err))

        self.well_filter = SeisWare.FilterList()
        try:
            self.login_instance.FilterManager().GetAll(self.well_filter)
        except RuntimeError as err:
            messagebox.showerror("Error", f"Failed to filters: {err}")
            print(self.well_filter)

        filter_list = []

        for filter in self.well_filter:
            filter_type = filter.FilterType()  # Replace with the appropriate method to get filter type
            if filter_type == 2:
                filter_name = filter.Name()  # Replace with the appropriate method to get filter name
                filter_info = f"{filter_name}"
                filter_list.append(filter_info)

        # Create the Well Filter dropdown using OptionMenu and populate it with filter_list
        self.filter_selection = tk.StringVar(value="")
        self.filter_dropdown = ttk.OptionMenu(self.top, self.filter_selection, "", *filter_list, command=self.on_filter_select)
        self.fiilter_label = tk.Label(self.top, text="Project:")
        self.filter_label.configure(**self.label_config)
        self.filter_label.place(relx=0.01, rely=0.035, relwidth=0.1)
        # Place the Well Filter dropdown on the interface
        self.filter_dropdown.place(relx=0.15, rely=0.035, relwidth=0.2)


        project_name = self.project_selection.get()
        self.projects = [project for project in self.project_list if project.Name() == project_name]
        if not self.projects:
            messagebox.showerror("Error", "No project was found")
            sys.exit(1)

        login_instance = SeisWare.LoginInstance()
        try:
            login_instance.Open(self.connection, self.projects[0])
        except RuntimeError as err:
            messagebox.showerror("Error", "Failed to connect to the project: " + str(err))

        # Get the wells from the project
        self.well_list = SeisWare.WellList()
        try:
            login_instance.WellManager().GetAll(self.well_list)
        except RuntimeError as err:
            messagebox.showerror("Error", "Failed to get all the wells from the project: " + str(err))


        # Retrieve UWIs from the well_list
       # Retrieve UWIs from the well_list and sort them
        uwi_list = [well.UWI() for well in self.well_list]
        self.sorted_uwi_list = sorted(uwi_list, reverse=False)

        # Create a label for the UWI dropdown
        self.planned_uwi_label = tk.Label(self.top, text="UWI Intersect:")
        self.planned_uwi_label.configure(background='white')
        self.planned_uwi_label.place(relx=0.01, rely=0.8, relwidth=0.1)

        # Create a Combobox for the UWI with autocomplete functionality
        self.planned_uwi = ttk.Combobox(self.top)
        self.planned_uwi.place(relx=0.15, rely=0.8, relwidth=0.2)

        # Set the initial values to the sorted UWI list
        self.planned_uwi['values'] = self.sorted_uwi_list

        # Bind the key release event to filter values as the user types
        # Bind the key release event to filter values as the user types
        self.planned_uwi.bind("<KeyRelease>", self.filter_uwi_values)

        # Bind the Enter key event to call planned_uwi_select
        self.planned_uwi.bind("<Return>", self.planned_uwi_select)
        self.planned_uwi.bind("<<ComboboxSelected>>", self.planned_uwi_select)

                # Get the grids from the project
        self.grid_list = SeisWare.GridList()
        try:
            self.login_instance.GridManager().GetAll(self.grid_list)
        except RuntimeError as err:
            messagebox.showerror("Failed to get the grids from the project", err)
                # Create the Well Filter dropdown using OptionMenu and populate it with filter_list
        self.grids = [grid.Name() for grid in self.grid_list]
        self.grid_objects_with_names = [(grid, grid.Name()) for grid in self.grid_list]


        self.grid_selection = tk.StringVar(value="")
        self.grid_label = tk.Label(self.top, text="Top Grid:")
        self.grid_label.configure(**self.label_config)
        self.grid_label.place(relx=0.01, rely=0.7, relwidth=0.1)
        self.grid_combobox = ttk.Combobox(self.top, values=self.grids)
        self.grid_combobox.place(relx=0.15, rely=0.7, relwidth=0.2)  # Adjust rely to position the dropdown below the project dropdown
        self.grid_combobox.bind("<<ComboboxSelected>>", self.on_grid_select)
        self.grid_combobox.bind("<Return>", self.on_grid_select)

        self.grid_buttom_selection = tk.StringVar(value="")
        self.grid_bottom_label = tk.Label(self.top, text="Bottom Grid:")
        self.grid_bottom_label.configure(**self.label_config)
        self.grid_bottom_label.place(relx=0.01, rely=0.75, relwidth=0.1)
        self.grid_bottom_combobox = ttk.Combobox(self.top, values=self.grids)
        self.grid_bottom_combobox.place(relx=0.15, rely=0.75, relwidth=0.2)  # Adjust rely to position the dropdown below the project dropdown
        self.grid_bottom_combobox.bind("<<ComboboxSelected>>", self.on_grid_select_bottom)
        self.grid_bottom_combobox.bind("<Return>", self.on_grid_select_bottom)

        # Delete any existing selection
        if self.grid_bottom_combobox:
            self.grid_bottom_combobox.delete(0, tk.END)


    def on_filter_select(self, event):

        # Clear the content of the list selectors
        self.uwi_listbox.delete(0, 'end')
        self.selected_uwi_listbox.delete(0, 'end')

        selected_filter = self.filter_selection.get()
        # Do whatever you want to do with the selected filter
        # For example, you can print it:
        print(f"Selected filter: {selected_filter}")
    
        #Returns filtered wells in a SeisWare project as a list of well objects

        
        well_filter = SeisWare.FilterList()

        self.login_instance.FilterManager().GetAll(well_filter)

        well_filter = [i for i in well_filter if i.Name() == selected_filter]
      

        keys = SeisWare.IDSet()

        failed_keys = SeisWare.IDSet()

        well_list = SeisWare.WellList()
    
        try:
            self.login_instance.WellManager().GetKeysByFilter(well_filter[0],keys)
            self.login_instance.WellManager().GetByKeys(keys,well_list,failed_keys)
        except RuntimeError as err:
            messagebox.showerror("Failed to get all the wells from the project", err)
        
        self.well_list = [well.UWI() for well in well_list]
        self.well_id = [well for well in well_list]
        

        self.uwi_to_well_dict = {}

# Populate the dictionary with well objects and UWIs
        for well in well_list:
            uwi = well.UWI()
            self.uwi_to_well_dict[uwi] = well
        for uwi, well in self.uwi_to_well_dict.items():
            print(f"UWI: {uwi}, Well: {well}")
        
    

        self.load_uwi_list()
        

    def load_uwi_list(self):
        # Assuming uwi_list contains your data
        uwi_list = self.well_list
        sorted_uwi_list = sorted(uwi_list, reverse=False)

        for uwi in sorted_uwi_list:
            self.uwi_listbox.insert(tk.END, uwi)
    def on_uwi_select(self, event):
        selected_indices = self.uwi_listbox.curselection()
        selected_uwis = [self.uwi_listbox.get(idx) for idx in selected_indices]
        # Add the selected UWIs to the selected listbox
        for uwi in selected_uwis:
            self.selected_uwi_listbox.insert(tk.END, uwi)
        # Remove the selected UWIs from the original listbox
        for idx in reversed(selected_indices):
            self.uwi_listbox.delete(idx)

    def on_selected_uwi_select(self, event):
        selected_indices = self.selected_uwi_listbox.curselection()
        selected_uwis = [self.selected_uwi_listbox.get(idx) for idx in selected_indices]
        # Add the selected UWIs back to the original listbox
        for uwi in selected_uwis:
            self.uwi_listbox.insert(tk.END, uwi)
        # Remove the selected UWIs from the selected listbox
        for idx in reversed(selected_indices):
            self.selected_uwi_listbox.delete(idx)
    def on_grid_select(self,event):
        
        grid_name = self.grid_combobox.get()
        selected_grid_object = None
        for grid, name in self.grid_objects_with_names:
            if name == grid_name:
                selected_grid_object = grid
                break
        print(selected_grid_object)
     
        try:
            self.login_instance.GridManager().PopulateValues(selected_grid_object)
        except RuntimeError as err:
            messagebox.showerror("Failed to populate the values of grid %s from the project" % (grid), err)
    
        grid_values = SeisWare.GridValues()
        grid.Values(grid_values)
        
        # Fill a DF with X, Y, Z values
        self.grid_xyz_top = []
        grid_values_list = list(grid_values.Data())
        print(grid_values_list)
        counter = 0
        for i in range(grid_values.Height()):
            for j in range(grid_values.Width()):
                self.grid_xyz_top.append((grid.Definition().RangeY().start + i * grid.Definition().RangeY().delta,
                                grid.Definition().RangeX().start + j * grid.Definition().RangeX().delta,
                                grid_values_list[counter]))
                counter += 1
                print(counter)
        # Create DataFrame
        print(self.grid_xyz_top)
        self.grid_df = pd.DataFrame(self.grid_xyz_top, columns=["Y", "X", f"{grid.Name()}"])

    def on_grid_select_bottom(self,event):
        
        grid_name = self.grid_bottom_combobox.get()
        selected_grid_object = None
        for grid, name in self.grid_objects_with_names:
            if name == grid_name:
                selected_grid_object = grid
                break
        print(selected_grid_object)
     

        try:
            self.login_instance.GridManager().PopulateValues(selected_grid_object)
        except RuntimeError as err:
            messagebox.showerror("Failed to populate the values of grid %s from the project" % (grid), err)
    
            

        grid_values = SeisWare.GridValues()
        grid.Values(grid_values)
        
        # Fill a DF with X, Y, Z values
        self.grid_xyz_bottom = []
        grid_values_list = list(grid_values.Data())
        print(grid_values_list)
        counter = 0
        for i in range(grid_values.Height()):
            for j in range(grid_values.Width()):
                self.grid_xyz_bottom.append((grid.Definition().RangeY().start + i * grid.Definition().RangeY().delta,
                                grid.Definition().RangeX().start + j * grid.Definition().RangeX().delta,
                                grid_values_list[counter]))
                counter += 1
                print(counter)
        # Create DataFrame
        print(self.grid_xyz_bottom)
        self.grid_df = pd.DataFrame(self.grid_xyz_bottom, columns=["Y", "X", f"{grid.Name()}"])



    def planned_uwi_select(self, event):
        # Get the selected UWI from the planned_uwi Combobox
        selected_uwi = self.planned_uwi.get()

        # Check if a UWI is selected
        if not selected_uwi:
            return  # No UWI selected, do nothing

        # Find the corresponding well for the selected UWI
        well = self.uwi_to_well_dict.get(selected_uwi)
        print(well)

        if well:
            # Now you have the well, you can retrieve its directional survey as you did in the export method
            dirsrvylist = SeisWare.DirectionalSurveyList()
            self.login_instance.DirectionalSurveyManager().GetAllForWell(well.ID(), dirsrvylist)

            # Select the directional survey if it exists
            dirsrvy = [i for i in dirsrvylist if i.OffsetNorthType() > 0]
            
            depth_unit = SeisWare.Unit.Meter

            surfaceX = well.TopHole().x.Value(depth_unit)
            surfaceY = well.TopHole().y.Value(depth_unit)
            surfaceDatum = well.DatumElevation().Value(depth_unit)

            if dirsrvy:
                self.login_instance.DirectionalSurveyManager().PopulateValues(dirsrvy[0])
                srvypoints = SeisWare.DirectionalSurveyPointList()
                dirsrvy[0].Values(srvypoints)

                # Now you can work with the survey points for the selected well
                self.directional_survey_values = []
                for i in srvypoints:
                    # Process survey data here as needed
                    # Append the relevant values to the directional_survey_values list
                    well_uwi = well.UWI()
                    x_offset = surfaceX + i.xOffset.Value(depth_unit)
                    y_offset = surfaceY + i.yOffset.Value(depth_unit)
                    tvd = surfaceDatum - i.tvd.Value(depth_unit)
                    md = i.md.Value(depth_unit)

                    self.directional_survey_values.append([well_uwi, x_offset, y_offset, tvd, md])
                print(self.directional_survey_values)

            else:
                # No directional survey found for the selected well
                messagebox.showinfo("Info", "No directional survey found for the selected well.")
        else:
            # Well not found for the selected UWI
            messagebox.showinfo("Info", "Well not found for the selected UWI.")

        self.Grid_intersec_top = []

        for survey_point in self.directional_survey_values:
            well_uwi = survey_point[0]
            x_offset = survey_point[1]
            y_offset = survey_point[2]
            md = survey_point[4]
    
            closest_point = min(self.grid_xyz_top, key=lambda point: np.sqrt((x_offset - point[0])**2 + (y_offset - point[1])**2))
            closest_z = closest_point[2]
            self.Grid_intersec_top.append((md, closest_z))

        self.Grid_intersec_bottom = []
        print(self.Grid_intersec_bottom)

        for survey_point in self.directional_survey_values:
            well_uwi = survey_point[0]
            x_offset = survey_point[1]
            y_offset = survey_point[2]
            md = survey_point[4]

            closest_point = min(self.grid_xyz_bottom, key=lambda point: np.sqrt((x_offset - point[0])**2 + (y_offset - point[1])**2))
            closest_z = closest_point[2]
            self.Grid_intersec_bottom.append((md, closest_z))



    def export(self):
        # Get the selected well UWIs from the selected_uwi_listbox
        selected_uwis = self.selected_uwi_listbox.get(0, tk.END)
        print(selected_uwis)

        if not selected_uwis:
            messagebox.showinfo("Info", "No wells selected for export.")
            return

        # Create a directory to store the Excel file
        output_directory = r'C:\SeisWare'
        os.makedirs(output_directory, exist_ok=True)

        # Create a new Excel workbook
        workbook = openpyxl.Workbook()

        for uwi in selected_uwis:
            well = self.uwi_to_well_dict.get(uwi)
            if well:
                # Create a new worksheet for each well
                worksheet = workbook.create_sheet(title=uwi)  # Set the sheet name to the well's UWI

                # Write the header row to the worksheet
                worksheet.append(['UWI', 'X', 'Y', 'TVDSS', 'MD'])

                depth_unit = SeisWare.Unit.Meter

                surfaceX = well.TopHole().x.Value(depth_unit)
                surfaceY = well.TopHole().y.Value(depth_unit)
                surfaceDatum = well.DatumElevation().Value(depth_unit)

                dirsrvylist = SeisWare.DirectionalSurveyList()
                self.login_instance.DirectionalSurveyManager().GetAllForWell(well.ID(), dirsrvylist)

                # Select the directional survey if it exists
                dirsrvy = [i for i in dirsrvylist if i.OffsetNorthType() > 0]

                if dirsrvy:
                    self.login_instance.DirectionalSurveyManager().PopulateValues(dirsrvy[0])
                    srvypoints = SeisWare.DirectionalSurveyPointList()
                    dirsrvy[0].Values(srvypoints)


                    for i in srvypoints:
                        # Write survey data to the worksheet
                        worksheet.append([
                            well.UWI(),
                            surfaceX + i.xOffset.Value(depth_unit),
                            surfaceY + i.yOffset.Value(depth_unit),
                            surfaceDatum - i.tvd.Value(depth_unit),
                            i.md.Value(depth_unit)
                        ])


        # Remove the default "Sheet" created by openpyxl
        default_sheet = workbook['Sheet']
        workbook.remove(default_sheet)

        # Save the Excel file
        excel_file_path = os.path.join(output_directory, 'exported_wells.xlsx')
        workbook.save(excel_file_path)

        return excel_file_path
    def plot_data(self):
        if self.planned_uwi.get():
            self.planned_uwi_select(None)
   
        
        # Get the selected well UWIs from the selected_uwi_listbox
        selected_uwis = self.selected_uwi_listbox.get(0, tk.END)

        if not selected_uwis:
            messagebox.showinfo("Info", "No wells selected for plotting.")
            return

        # Create a color map to assign different colors to each well
        colors = plt.cm.viridis(np.linspace(0, 1, len(selected_uwis)))

        plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

        for i, uwi in enumerate(selected_uwis):
            well = self.uwi_to_well_dict.get(uwi)
            if well:
                depth_unit = SeisWare.Unit.Meter
                surfaceDatum = well.DatumElevation().Value(depth_unit)

                dirsrvylist = SeisWare.DirectionalSurveyList()
                self.login_instance.DirectionalSurveyManager().GetAllForWell(well.ID(), dirsrvylist)

                # Select the directional survey if it exists
                dirsrvy = [i for i in dirsrvylist if i.OffsetNorthType() > 0]

                if dirsrvy:
                    self.login_instance.DirectionalSurveyManager().PopulateValues(dirsrvy[0])
                    srvypoints = SeisWare.DirectionalSurveyPointList()
                    dirsrvy[0].Values(srvypoints)

                    md_values = [i.md.Value(depth_unit) for i in srvypoints]
                    tvdss_values = [surfaceDatum - i.tvd.Value(depth_unit) for i in srvypoints]

                    plt.plot(md_values, tvdss_values, label=f'UWI: {uwi}', color=colors[i])

            # Plot the z values from self.Grid_intersec_top and self.Grid_intersec_bottom
        if self.Grid_intersec_top:
            md_top = [item[0] for item in self.Grid_intersec_top]
            z_top = [item[1] for item in self.Grid_intersec_top]
            plt.plot(md_top, z_top, linestyle='--', color='red', label='Grid Intersec Top')

        if self.Grid_intersec_bottom:
            md_bottom = [item[0] for item in self.Grid_intersec_bottom]
            z_bottom = [item[1] for item in self.Grid_intersec_bottom]
            plt.plot(md_bottom, z_bottom, linestyle='--', color='blue', label='Grid Intersec Bottom')
        plt.xlabel('MD')
        plt.ylabel('TVDSS')
        plt.legend()
        plt.grid()
        plt.title('MD vs. TVDSS for Selected Wells')
        plt.show()


    def store_uwis_and_offsets(self):
        selected_uwis = self.selected_uwi_listbox.get(0, tk.END)
        print(selected_uwis)

        if not selected_uwis:
            messagebox.showinfo("Info", "No wells selected for export.")
            return

        for uwi in selected_uwis:
            well = self.uwi_to_well_dict.get(uwi)
            if well:
                depth_unit = SeisWare.Unit.Meter

                x_offsets = []
                y_offsets = []

                surfaceX = well.TopHole().x.Value(depth_unit)
                surfaceY = well.TopHole().y.Value(depth_unit)

                dirsrvylist = SeisWare.DirectionalSurveyList()
                self.login_instance.DirectionalSurveyManager().GetAllForWell(well.ID(), dirsrvylist)

                # Select the directional survey if it exists
                dirsrvy = [i for i in dirsrvylist if i.OffsetNorthType() > 0]

                if dirsrvy:
                    self.login_instance.DirectionalSurveyManager().PopulateValues(dirsrvy[0])
                    srvypoints = SeisWare.DirectionalSurveyPointList()
                    dirsrvy[0].Values(srvypoints)

                    for i in srvypoints:
                        # Calculate X and Y coordinates based on offsets
                        x_offset = surfaceX + i.xOffset.Value(depth_unit)
                        y_offset = surfaceY + i.yOffset.Value(depth_unit)

                        x_offsets.append(x_offset)
                        y_offsets.append(y_offset)

                    # Append UWIs and their offsets to the global list
                    self.uwis_and_offsets.append((uwi, x_offsets, y_offsets))
                    print(f"UWI: {uwi}, X Offsets: {x_offsets}, Y Offsets: {y_offsets}")
   

        print(self.uwis_and_offsets)
    def map_data(self):
        map_window = Map.MapWindow(self.uwis_and_offsets)  # Pass the data to the constructor
        map_window.run()
        


    def subscribe_to_seisware_messages(self):
        # Create a thread to handle messages
        message_thread = threading.Thread(target=self.message_handler)
        message_thread.daemon = True  # Allow the thread to exit when the main program exits
        message_thread.start()

    def message_handler(self):
        # Create the login_instance and then subscribe to well selection messages
        message_manager = self.login_instance.MessageManager()
        message_manager.Subscribe("Well", "Add")
        messages = SeisWare.MessageList()
        message_manager.GetMessages(messages)
        
                
     
    def filter_uwi_values(self, event):
        typed_text = event.widget.get().lower()
        
        # Filter the values based on the typed text
        matching_items = [item for item in self.sorted_uwi_list if typed_text in item.lower()]

        # Update the Combobox values to show the filtered items
        event.widget['values'] = matching_items






if __name__ == '__main__':
    root = tk.Tk()
    app = ImageGUI(root)
    root.mainloop()