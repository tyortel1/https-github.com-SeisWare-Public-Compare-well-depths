import tkinter as tk
from collections import defaultdict

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)

class MapWindow:
    def __init__(self, uwis_and_offsets):
        self.root = tk.Tk()
        self.root.title("Map")
        self.root.geometry("936x797+590+257") 
        self.root.minsize(120, 1)
        self.root.maxsize(6500, 1181)
        self.root.resizable(1, 1)
        self.canvas = None

        self.canvas = tk.Canvas(self.root, bg="white", bd=2, relief="ridge")
        self.canvas.place(relx=0.250, rely=0.113, relheight=0.882, relwidth=0.718)
        self.canvas.configure(background="white")
        self.canvas.configure(borderwidth="2")
        self.canvas.configure(insertbackground="black")
        self.canvas.configure(relief="ridge")
        self.canvas.configure(selectbackground="#c4c4c4")
        self.canvas.configure(selectforeground="black")

        # Create a canvas with a fixed size
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.vsb = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.vsb.place(relx=0.958, rely=0.113, relheight=0.882)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.hsb = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.hsb.place(relx=0.250, rely=0.975, relwidth=0.718)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.hsb.set(0, 1)
        self.canvas.xview_moveto(0)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.line_drawing = LineDrawing(self.canvas)

        # Add a button for saving the drawn lines
        self.save_button = tk.Button(self.root, text="Save Lines", command=self.save_lines)
        self.save_button.place(relx=0.05, rely=0.05)

        # Bind canvas events for line drawing
        self.canvas.bind("<Button-1>", self.line_drawing.start_line)
        self.canvas.bind("<Button-3>", self.line_drawing.finish_line)
        
        self.data = []
        self.data = uwis_and_offsets
        self.get_canvas_size()

    def save_lines(self):
        # Save the drawn lines for later use
        saved_lines = {}
        for line_id, points in self.line_drawing.points.items():
            saved_lines[line_id] = points
        print("Saved Lines:", saved_lines)

    def get_canvas_size(self):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        print(canvas_width, canvas_height)
        self.display_wells()

    def display_wells(self):
        # Clear the canvas before drawing
        self.canvas.delete("all")
        print("tst")
        uwis_and_offsets = self.data

        # Define the canvas size (width and height)
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        print(canvas_width)

        # Define the data range (maximum and minimum X and Y values)
        data_x_max = max(x for _, x_offsets, _ in uwis_and_offsets for x in x_offsets)
        data_x_min = min(x for _, x_offsets, _ in uwis_and_offsets for x in x_offsets)
        data_y_max = max(y for _, _, y_offsets in uwis_and_offsets for y in y_offsets)
        data_y_min = min(y for _, _, y_offsets in uwis_and_offsets for y in y_offsets)

        # Calculate the scaling factors for X and Y
        scale_x = canvas_width / (data_x_max - data_x_min) if data_x_max != data_x_min else 1
        scale_y = canvas_height / (data_y_max - data_y_min) if data_y_max != data_y_min else 1

        # Iterate through the wells and draw dots
        for uwi, x_offsets, y_offsets in uwis_and_offsets:
            for x_offset, y_offset in zip(x_offsets, y_offsets):
                # Calculate the canvas coordinates based on scaling
                canvas_x = (x_offset - data_x_min) * scale_x
                canvas_y = (y_offset - data_y_min) * scale_y
                print(canvas_x)

                # Draw a dot (circle) for each well
                dot_size = 5  # Adjust the size of the dots as needed
                self.canvas.create_oval(
                    canvas_x - dot_size,
                    canvas_y - dot_size,
                    canvas_x + dot_size,
                    canvas_y + dot_size,
                    fill="blue",  # You can set the color of the dots
                    outline="blue"  # You can set the outline color (same as fill for solid dots)
                )

        # Set the scroll region based on the drawn content
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Refresh the canvas
        self.canvas.update()

    def run(self):
        # Start the main event loop
        self.root.update_idletasks()  # Update the display and event handling
        self.get_canvas_size()
        self.root.mainloop()



class LineDrawing:
    def __init__(self, canvas):
        self.canvas = canvas
        self.points = []  # Store the points as tuples (x, y)
        self.current_line = None
        self.current_ovals = []
        self.finish = False
        self.lines = []  # Store the line objects

    def start_line(self, event):
        if self.finish:
            self.clear_current_line()
            self.finish = False
            self.points = []  # Clear the current line and ovals


        x, y = event.x, event.y
        self.points.append((x, y))

        # Create a dot at the clicked position
        oval = self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red")
        self.current_ovals.append(oval)

        # Connect the dots with lines if there are at least two points
        if len(self.points) >= 2:
            x1, y1 = self.points[-2]  # Previous point
            x2, y2 = self.points[-1]  # Current point
            line = self.canvas.create_line(x1, y1, x2, y2, fill="red")
            self.current_line = line
            self.lines.append(line)  # Store the line object

    def clear_current_line(self):
        # Clear the current line, ovals, and points if they exist
        if self.current_line:
            self.canvas.delete(self.current_line)
            self.current_line = None

        if self.current_ovals:
            for oval in self.current_ovals:
                self.canvas.delete(oval)
            self.current_ovals = []

        for line in self.lines:
            self.canvas.delete(line)
            self.lines = []

        self.points = []  # Clear the points of the current line

    def finish_line(self, event):
        self.finish = True


     


# Rest of the code remains unchanged


if __name__ == "__main__":
    main()
