import tkinter as tk
import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._create_frames()

        self.looping = False

        



    def _create_frames(self):
        self.constants_frame = ctk.CTkScrollableFrame(self, scrollbar_button_color='#2b2b2b')
        self.inputs_frame = ctk.CTkFrame(self)
        self.outputs_frame = ctk.CTkScrollableFrame(self, scrollbar_button_color='#2b2b2b')

        self.loop_toggle_btn = ctk.CTkButton(self, text='Loop Toggle', command=lambda: self._toggle_looping(1), height=24, fg_color='#1f538d')

        self.inputs_frame.grid(row=0, column=0,
                               padx=6, pady=6,
                               sticky='nsew')

        self.constants_frame.grid(row=1, column=0,
                                  padx=6, pady=6,
                                  sticky='nsew')
        
        self.outputs_frame.grid(row=0, column=1,
                                rowspan=4,
                                padx=6, pady=6,
                                sticky='nsew')
        
        self.loop_toggle_btn.grid(row=2, column=0,
                                  padx=6, pady=6,
                                  sticky='nsew')
        
        self.grid_rowconfigure(3, weight=1)
        
        self.grid_columnconfigure(1, weight=1)

        self._config_inputs_frame()
        self._config_constants_frame()
        self._config_outputs_frame()


    def _config_inputs_frame(self):
        frame = self.inputs_frame
        ctk.CTkLabel(frame, text='Inputs', font=('Roboto',20), text_color='#555').grid(row=0, column=0)

        self.inputs = Inputs()

        self.slider_vars = {}

        for num, item in enumerate(self.inputs.ranges):
            var = item
            range = self.inputs.ranges[item]
            

            label_var = tk.StringVar(value=f'{var}: {range['min']}')
            slider_var = tk.DoubleVar(value=range['min'])

            self.slider_vars[var] = {'slider_var':slider_var,'label_var':label_var}

            label = ctk.CTkLabel(frame, textvariable=label_var)
            slider = ctk.CTkSlider(frame, variable=slider_var, from_=range['min'], to=range['max'], command=self._update_label(var))

            label.grid(row=2*num+1, column=0)
            slider.grid(row=2*num+2, column=0,
                        padx=6, pady=6,
                        sticky='new')
            frame.grid_rowconfigure(2*num+2, weight=1)

        frame.grid_columnconfigure(0, weight=1) 


    def _update_label(self, var):
        def update(value):
            label_var = self.slider_vars[var]['label_var']
            label_var.set(f'{var}: {float(value):.3f}')
        return update


    def _config_constants_frame(self):
        frame = self.constants_frame
        ctk.CTkLabel(frame, text='Constants', font=('Roboto',20), text_color='#555').grid(row=0, column=0, columnspan=2)

        self.constants = {'BPslope':100.0211,'NPs':0.313000842,'RPs':0.006261229,
                          'BPintercept':599.9683,'NPi':-1.26727813,'RPi':-0.025138,
                          'E':1.043,'V':0.00001222,'Gc':53.35,
                          'r':3206.18,'a':-27405.5,'b':54.1896,'c':-0.0451347,'d':0.0000215321,'e':-0.00000000462927,'f':2.41613,'g':0.00121547,
                          }
        for num, item in enumerate(self.constants):
            const = item
            val = self.constants[item]
            left = ctk.CTkLabel(frame, text=f'{const}', height=14)
            right = ctk.CTkLabel(frame, text=f'{val}', height=14)

            left.grid(row=num+1, column=0, sticky='w')
            right.grid(row=num+1, column=1, sticky='e')
        
        frame.grid_columnconfigure(0, weight=1)

    
    def _config_outputs_frame(self):
        frame = self.outputs_frame
        ctk.CTkLabel(frame, text='Outputs', font=('Roboto',20), text_color='#555').grid(row=0, column=0)
        
        frame.grid_columnconfigure(0, weight=1)


    def _toggle_looping(self, sec):
        self.looping = not self.looping
        if self.looping:
            self._loop(sec)
            self.loop_toggle_btn.configure(fg_color='#393')
            self.loop_toggle_btn.configure(hover_color='#272')
        else:
            self.loop_toggle_btn.configure(fg_color='#1f538d')
            self.loop_toggle_btn.configure(hover_color='#14375e')
    

    def _loop(self, sec):

        if self.looping:
            #
            #insert looping behavior here
            #
            print('test')
            self.after(1000*sec, lambda: self._loop(sec))


class Inputs:
    def __init__(self):
        self.ranges = {'TempD':{'min':0.004,'max':0.02},'TempR':{'min':0.004,'max':0.02},
                       'RHD':{'min':0.004,'max':0.02},'RHR':{'min':0.004,'max':0.02},
                       'NPc':{'min':0.004,'max':0.02},'RPc':{'min':0.004,'max':0.02},
                       'BP':{'min':0,'max':5}}
        
        for name, range in self.ranges.items():
            setattr(self, name, CustomVar(value=range['min']))

    def get_input(self, name):
        return getattr(self, name).get()
    
    def set_input(self, name, value):
        if value < self.ranges[name]['min']:
            value = self.ranges[name]['min']
        if value > self.ranges[name]['max']:
            value = self.ranges[name]['max']

        getattr(self, name).set(value)
    
    
class CustomVar:
    def __init__(self, value=None):
        self.value = value

    def set(self, new_value):
        self.value = new_value
    
    def get(self):
        return self.value

        






if __name__ == '__main__':
    app = App()
    app.geometry('+830+300')
    app.minsize(1200,693)

    # inputs = Inputs()
    # #for key, value in inputs.__dict__.items():
    #     #print(key, value.get())
    # print(inputs.TempD.get())
    # print(inputs.get_input('TempD'))
    # inputs.set_input('TempD', .01)
    # print(inputs.get_input('TempD'))
    app.mainloop()

    
