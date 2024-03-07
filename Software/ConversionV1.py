import tkinter as tk
import customtkinter as ctk

class AnimationWindow(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_canvas()

    def _create_canvas(self):
        canvas = tk.Canvas(self)
        canvas.pack(fill='both', expand=True)
    















if __name__ == '__main__':
    animate = AnimationWindow()
    animate.geometry('600x600')
    animate.title('Animation')

    animate.mainloop()

