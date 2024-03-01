import tkinter as tk
import customtkinter as ctk
import numpy as np


class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.constants = {'BPslope':100.0211,'NPs':0.313000842,'RPs':0.006261229,
                          'BPintercept':599.9683,'NPi':-1.26727813,'RPi':-0.025138,
                          'E':1.043,'V':0.00001222,'Gc':53.35,
                          'r':3206.18,'a':-27405.5,'b':54.1896,'c':-0.0451347,'d':0.0000215321,'e':-0.00000000462927,'f':2.41613,'g':0.00121547,
                          }
        self.inputs = Inputs()
        self.outputs = Output(self.constants, self.inputs.get())
        
        
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

        

        self.input_label_vars = {}
        self.input_slider_vars = {}

        for num, item in enumerate(self.inputs.ranges):
            var = item
            range = self.inputs.ranges[item]
            

            label_var = tk.StringVar(value=f'{var}: {range["min"]}')
            slider_var = tk.DoubleVar(value=range['min'])

            self.input_slider_vars[var] = slider_var
            self.input_label_vars[var] = label_var

            label = ctk.CTkLabel(frame, textvariable=label_var)
            slider = ctk.CTkSlider(frame, variable=slider_var, from_=range['min'], to=range['max'], command=self._update_inputs(var))

            label.grid(row=2*num+1, column=0)
            slider.grid(row=2*num+2, column=0,
                        padx=6, pady=6,
                        sticky='new')
            frame.grid_rowconfigure(2*num+2, weight=1)

        frame.grid_columnconfigure(0, weight=1) 


    def _update_inputs(self, var):
        
        def update(value):
            label_var = self.input_label_vars[var]
            label_var.set(f'{var}: {float(value):.3f}')
            self.inputs.set(var, value)
            
        return update


    def _config_constants_frame(self):
        frame = self.constants_frame
        ctk.CTkLabel(frame, text='Constants', font=('Roboto',20), text_color='#555').grid(row=0, column=0, columnspan=2)

        
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

        self.output_label_vars = {}
            
        
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
            self.outputs.update(self.inputs.get())
            print(self.outputs.get())
            
            #print('test')
            self.after(1000*sec, lambda: self._loop(sec))

class Output:
    def __init__(self, constants, inputs):
        self.constants = constants
        for name, val in constants.items():
            setattr(self, name, val)
        self.outputs = {}
        
        self.update(inputs)

    def update(self, inputs):
        #print(inputs)
        #Temp in F
        TD = (inputs['TempD']*1000 + 32)*11.25 + 32
        TR = (inputs['TempR']*1000 + 32)*11.25 + 32

        #RH in %
        RD = (inputs['RHD']*1000-4)/0.16
        RR = (inputs['RHR']*1000-4)/0.16

        # #saturation pressure psi, unsure of source
        PsD = self.r * np.exp((self.a + self.b*(TD + 460) + self.c*(TD + 460)**2 + self.d*(TD + 460)**3 + self.e*(TD + 460)**4)/(self.f*(TD + 460) - self.g*(TD + 460)**2))
        PsR = self.r * np.exp((self.a + self.b*(TR + 460) + self.c*(TR + 460)**2 + self.d*(TR + 460)**3 + self.e*(TR + 460)**4)/(self.f*(TR + 460) - self.g*(TR + 460)**2))

        # #barometric pressure psi, mbar to psi conversion
        B = (self.BPslope*inputs['BP'] + self.BPintercept)*0.01450377

        # #air density lb/ft3, unsure of source
        DD = ((B - PsD*(RD/100))/(0.37*(460+TD)))+((PsD*(RD/100))/(0.596*(460+TD)))
        DR = ((B - PsR*(RR/100))/(0.37*(460+TR)))+((PsR*(RR/100))/(0.596*(460+TR)))

        # #nozzle pressure
        NPcu = inputs['NPc']*1000
        NP = self.NPs*NPcu + self.NPi
        if NP < 0:
            NP = 0

        # #room pressure
        RPcu = inputs['RPc']*1000
        RP = self.RPs*RPcu + self.RPi
        RPA = -1 * RP

        #grabbing assigned vars from within this scope and creating dict
        self.var_list = {name:val for name, val in locals().items() if name not in {'inputs','self','__class__'}}
        
    def get(self, name=None):
        if name is None:
            return self.var_list
        else:
            return self.var_list[name]

    
        
            



    
        
        


class Inputs:
    def __init__(self):
        self.ranges = {'TempD':{'min':0.004,'max':0.02},'TempR':{'min':0.004,'max':0.02},
                       'RHD':{'min':0.004,'max':0.02},'RHR':{'min':0.004,'max':0.02},
                       'NPc':{'min':0.004,'max':0.02},'RPc':{'min':0.004,'max':0.02},
                       'BP':{'min':0,'max':5}}
        
        self.inputs = {}
        
        for name, range in self.ranges.items():
            self.inputs[name] = range['min']
            setattr(self, name, range['min'])

    def get(self, name=None):
        if name is not None:
            return getattr(self, name)
        else:
            return self.inputs
    
    def set(self, name, value):
        if value < self.ranges[name]['min']:
            value = self.ranges[name]['min']
        if value > self.ranges[name]['max']:
            value = self.ranges[name]['max']

        #getattr(self, name).set(value)
        self.inputs[name] = value
        setattr(self, name, value)
    

        






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

    
