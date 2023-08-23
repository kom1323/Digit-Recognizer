import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import numpy as np
from tkinter.colorchooser import askcolor

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Paint App")
        self.root.geometry("800x600")

        self.color = "black"
        self.line_width = 5
        self.drawing = False
        self.old_x = None
        self.old_y = None

        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear Canvas", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        color_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Color", menu=color_menu)
        color_menu.add_command(label="Choose Color", command=self.choose_color)

        predict_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Predict", menu=predict_menu)
        predict_menu.add_command(label="Predict Digit", command=self.predict_digit)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.pil_image = Image.new("RGB", (800, 600), "white")
        self.pil_draw = ImageDraw.Draw(self.pil_image)
        self.photo = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.canvas.bind("<Configure>", self.resize_canvas)

    def start_drawing(self, event):
        self.drawing = True
        self.old_x = event.x
        self.old_y = event.y

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            if self.old_x and self.old_y:
                self.pil_draw.line(
                    [(self.old_x, self.old_y), (x, y)],
                    fill=self.color, width=self.line_width
                )
                self.canvas.delete("all")
                self.photo = ImageTk.PhotoImage(self.pil_image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.old_x = x
            self.old_y = y

    def stop_drawing(self, event):
        self.drawing = False
        self.old_x = None
        self.old_y = None

    def clear_canvas(self):
        self.pil_image = Image.new("RGB", (800, 600), "white")
        self.pil_draw = ImageDraw.Draw(self.pil_image)
        self.canvas.delete("all")
        self.photo = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def predict_digit(self):
        pixel_arr = np.array(self.pil_image)
        print(pixel_arr)

    def choose_color(self):
        color = askcolor()[1]
        if color:
            self.color = color

    def resize_canvas(self, event):
        self.pil_image = self.pil_image.resize((event.width, event.height), Image.ANTIALIAS)
        self.pil_draw = ImageDraw.Draw(self.pil_image)
        self.canvas.delete("all")
        self.photo = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

def main():
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
