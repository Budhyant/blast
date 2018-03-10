print('Blast Load Calculator is loading ...')

from eval_param import Evaluate
import numpy as np
import math

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

path = './dimension.png'
LARGE_FONT = ("Verdana", 12)
MID_FONT = ("Courier", 8)

class Window(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.frame = tk.Frame(self)
        self.frame.pack(side="right", fill="y")
        tk.Tk.wm_title(self, "Blast Load Calculator")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=10)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        main = Main(container, self)
        main.pack()


class Main(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Blast Load Calculator", font=LARGE_FONT, fg="blue")
        label.config(font=('Courier', 25))
        label.grid(row=0, column=0, columnspan=3, padx=10)

        canvas = tk.Canvas(self, width = 250, height = 150)
        canvas.grid(row=4, rowspan=3, column=0, pady=5)
        self.img = Image.open(path)
        self.img = self.img.resize((250, 150), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        canvas.create_image(20, 0, anchor="nw", image=self.img)

        label_input = tk.Label(self, text="INPUTS", fg="blue")
        label_1 = tk.Label(self, text="Actual Stand-off Distance (D)[m]")
        label_2 = tk.Label(self, text="Net Explosive Quantity (Q)[kg]")
        label_3 = tk.Label(self, text="Dimension B [m]")
        label_4 = tk.Label(self, text="Dimension L [m]")
        label_5 = tk.Label(self, text="Dimension H [m]")
        label_6 = tk.Label(self, text="select your bomb type")
        label_7 = tk.Label(self, text="select your calc type")

        label_input.grid(row=1, column=0, columnspan=1, pady=10)
        label_1.grid(row=2, column=0, pady=10)
        label_2.grid(row=3, column=0, pady=10)
        label_3.grid(row=7, column=0, pady=10)
        label_4.grid(row=8, column=0, pady=10)
        label_5.grid(row=9, column=0, pady=10)
        label_6.grid(row=10, column=0, pady=10)
        label_7.grid(row=11, column=0, pady=10)

        e1 = ttk.Entry(self, width=3)
        e2 = ttk.Entry(self, width=3)
        e3 = ttk.Entry(self, width=3)
        e4 = ttk.Entry(self, width=3)
        e5 = ttk.Entry(self, width=3)
        e1.grid(row=2, column=1, padx=10, pady=10)
        e2.grid(row=3, column=1, padx=10, pady=10)
        e3.grid(row=7, column=1, padx=10, pady=10)
        e4.grid(row=8, column=1, padx=10, pady=10)
        e5.grid(row=9, column=1, padx=10, pady=10)
        e1.focus_set()
        e2.focus_set()
        e3.focus_set()
        e4.focus_set()
        e5.focus_set()

        label_copyright = tk.Label(self, text="The calculation is based on \n\"Airblast Parameters from TNT Spherical Air Burst & Hemispherical Surface Burst\"\nby Charles N Kingerey & Gerald Bulmash, Tech Report ARBRL-TR-02555 dated April 1984.\nIt is equivalent to UFC 3-340-02 Copyrights Ⓒ 2018 All rights reserved\n")
        label_copyright.grid(row=13, column=0, columnspan=4, pady=20)


        bomb_options = ["TNT", "RDX", "HMX", "Nitroglycerin", "CompoundB", "Semtex", "60% Nitroglycerin dynamite"]
        bomb_type = tk.StringVar(self)

        cal_options = ["air", "surface"]
        cal_type = tk.StringVar(self)

        output_type = tk.StringVar()
        output_type.set('type: none')

        option_1 = ttk.OptionMenu(self, bomb_type, bomb_options[0], *bomb_options)
        option_1.grid(row=10, column=1, padx=10, pady=10)
        option_2 = ttk.OptionMenu(self, cal_type, cal_options[0], *cal_options)
        option_2.grid(row=11, column=1, padx=10, pady=10)

        self.show_output_template();
        self.b = 2;
        self.time = np.arange(0, 100, 0.25)
        self.x_air = []
        self.x_sfc = []
        self.x_air_inc = []
        self.x_air_ref = []
        self.x_sfc_inc = []
        self.x_sfc_ref = []

        so_dist = None
        ne_qty = None

        def set_TNT_EQ_FIG(val):
            if val == 'TNT':
                return 1
            elif val == 'RDX':
                return 1.185
            elif val == 'HMX':
                return 1.256
            elif val == 'Nitroglycerin':
                return 1.481
            elif val == 'CompoundB':
                return 1.148
            elif val == 'Semtex':
                return 1.25
            elif val == '60% Nitroglycerin dynamite':
                return 0.6
            return

        def callback():
            if e1.get() == '' or e2.get() == '':
                label_err = tk.Label(self, text="please type input values", fg="red")
                label_err.grid(row=12, column=1)
            # elif type(int(e1.get())) == int and type(int(e2.get())) == int:
            elif self.validateFloat(e1.get()) and self.validateFloat(e2.get()) and self.validateFloat(e3.get()) and self.validateFloat(e4.get()) and self.validateFloat(e5.get()):
                label_ok = tk.Label(self, text="     all input values are valid     ", fg="green")
                label_ok.grid(row=12, column=1)
                so_dist = float(e1.get())
                ne_qty = float(e2.get())
                dim_b = float(e3.get())
                dim_l = float(e4.get())
                dim_h = float(e5.get())
                TNT_EQ_FIG = set_TNT_EQ_FIG(bomb_type.get())
                cal_type_val = cal_type.get()
                print('bomb type', bomb_type.get())
                print('cal_type', cal_type_val)
                # compute param using Evaluate Class
                if cal_type_val == 'air':
                    self.plot_air(so_dist, ne_qty, TNT_EQ_FIG, dim_b, dim_l, dim_h)
                else:
                    self.plot_sfc(so_dist, ne_qty, TNT_EQ_FIG, dim_b, dim_l, dim_h)

            else:
                label_err = tk.Label(self, text="please type integer input only", fg="red")
                label_err.grid(row=12, column=1)
                print('e1.get type', type(e1.get()), 'e2.get type', type(e2.get()))
            return
        ttk.Style().configure('black/gray.TButton', foreground='black', background='blue', height=5, width=15)
        btn_calc = ttk.Button(self, text="calculate", style='black/gray.TButton', command=callback)
        btn_calc.grid(row=12, column=0, padx=10, pady=20)
        btn_calc.grid_columnconfigure(12, weight=2)


    def validateFloat(self, value):
        ENTRY = value.strip()
        if ENTRY == "": return # do noting if we don't have a value
        try:
            NUMENTRY = float(ENTRY)
            if NUMENTRY: return True
        except ValueError:
            print('the input value is not integer or float')
            return

    def plot_air(self, so_dist, ne_qty, TNT_EQ_FIG, dim_b, dim_l, dim_h):
        param_result = Evaluate(so_dist, ne_qty, TNT_EQ_FIG, dim_b, dim_l, dim_h)
        points = param_result.get_points()
        pt_air = points['air']
        pt_air_fr = pt_air['front-wall']
        pt_air_fr_pr = pt_air_fr['pr']
        pt_air_fr_ps = pt_air_fr['ps']
        pt_air_eq = pt_air['equivalent']

        ps_air = pt_air['outputs']['ps']
        pr_air = pt_air['outputs']['pr']
        ta_air = pt_air['outputs']['ta']
        tp_air = pt_air['outputs']['td']

        self.x_air = self.get_graph_x(ta_air)
        self.x_air_inc = self.get_graph_x_final(ps_air, ta_air, tp_air, self.x_air)
        self.x_air_ref = self.get_graph_x_final(pr_air, ta_air, tp_air, self.x_air)

        pr_annotate = points['air']['outputs']['pr']
        ps_annotate = points['air']['outputs']['ps']
        td_annotate = points['air']['outputs']['td']
        tc_annotate = points['air']['outputs']['tc']
        te_annotate = points['air']['outputs']['te']

        f1 = Figure(figsize=(4,4), dpi=100)
        a = f1.add_subplot(111)
        a.set_title('Front-Wall Loading')
        a.plot(pt_air_fr_pr['x'], pt_air_fr_pr['y'])
        a.plot(pt_air_fr_ps['x'], pt_air_fr_ps['y'])
        a.plot([pt_air_fr_pr['x'][1], pt_air_fr_pr['x'][1]], [0, pt_air_fr_pr['y'][1]], '--')
        a.set_xlabel('time (ms)')
        a.set_ylabel('pressure (kPa)')

        a.annotate('Pr: ' + str(pr_annotate), xy=(td_annotate*0.05, pr_annotate*0.95))
        a.annotate('Ps: ' + str(ps_annotate), xy=(td_annotate*0.02, ps_annotate*0.9))
        a.annotate('td: ' + str(td_annotate), xy=(td_annotate*0.8, pr_annotate*0.05))
        a.annotate('tc: ' + str(tc_annotate), xy=(tc_annotate*1.1, pr_annotate*0.02))

        a.grid(linestyle='-')

        win_ftwall_load = tk.Toplevel(self)
        win_ftwall_load.wm_title("Air")
        l = tk.Label(win_ftwall_load, text="Air")
        l.pack()

        canvas1 = FigureCanvasTkAgg(f1, win_ftwall_load)

        f2 = Figure(figsize=(4,4), dpi=100)
        b = f2.add_subplot(111)
        b.set_title('Equivalent Loading')
        b.plot(pt_air_eq['x'], pt_air_eq['y'])
        b.set_xlabel('time (ms)')
        b.set_ylabel('pressure (kPa)')

        b.annotate('Pr: ' + str(pr_annotate), xy=(te_annotate*0.05, pr_annotate*0.97))
        b.annotate('te: ' + str(te_annotate), xy=(te_annotate*0.8, pr_annotate*0.03))


        b.grid(linestyle='-')

        win_eq_load = tk.Toplevel(self)
        win_eq_load.wm_title("Air")
        l = tk.Label(win_eq_load, text="Air")
        l.pack()

        canvas2 = FigureCanvasTkAgg(f2, win_eq_load)

        f3 = Figure(figsize=(4,4), dpi=100)
        c = f3.add_subplot(111)
        c.set_title('Friedlander Equation')
        c.plot(self.time, self.x_air_inc)
        c.plot(self.time, self.x_air_ref)

        c.grid(linestyle='-')

        graph = tk.Toplevel(self)
        graph.wm_title("Air")
        label_graph = tk.Label(graph, text="Air")
        label_graph.pack()

        canvas3 = FigureCanvasTkAgg(f3, graph)

        canvas1.show()
        canvas2.show()
        canvas3.show()

        canvas1._tkcanvas.pack()
        canvas2._tkcanvas.pack()
        canvas3._tkcanvas.pack()

        self.show_outputs('Air', points)


    def plot_sfc(self, so_dist, ne_qty, TNT_EQ_FIG, dim_b, dim_l, dim_h):
        param_result = Evaluate(so_dist, ne_qty, TNT_EQ_FIG, dim_b, dim_l, dim_h)
        points = param_result.get_points()

        pt_sfc = points['surface']
        pt_sfc_fr = pt_sfc['front-wall']
        pt_sfc_fr_pr = pt_sfc_fr['pr']
        pt_sfc_fr_ps = pt_sfc_fr['ps']
        pt_sfc_eq = pt_sfc['equivalent']

        ps_sfc = pt_sfc['outputs']['ps']
        pr_sfc = pt_sfc['outputs']['pr']
        ta_sfc = pt_sfc['outputs']['ta']
        tp_sfc = pt_sfc['outputs']['td']

        self.x_sfc = self.get_graph_x(ta_sfc)
        self.x_sfc_inc = self.get_graph_x_final(ps_sfc, ta_sfc, tp_sfc, self.x_sfc)
        self.x_sfc_ref = self.get_graph_x_final(pr_sfc, ta_sfc, tp_sfc, self.x_sfc)

        pr_annotate = points['surface']['outputs']['pr']
        ps_annotate = points['surface']['outputs']['ps']
        td_annotate = points['surface']['outputs']['td']
        tc_annotate = points['surface']['outputs']['tc']
        te_annotate = points['surface']['outputs']['te']

        f1 = Figure(figsize=(4,4), dpi=100)
        a = f1.add_subplot(111)
        a.plot(pt_sfc_fr_pr['x'], pt_sfc_fr_pr['y'])
        a.plot(pt_sfc_fr_ps['x'], pt_sfc_fr_ps['y'])
        a.plot([pt_sfc_fr_pr['x'][1], pt_sfc_fr_pr['x'][1]], [0, pt_sfc_fr_pr['y'][1]], '--')
        a.set_xlabel('time (ms)')
        a.set_ylabel('pressure (kPa)')

        a.annotate('Pr: ' + str(pr_annotate), xy=(td_annotate*0.05, pr_annotate*0.95))
        a.annotate('Ps: ' + str(ps_annotate), xy=(td_annotate*0.02, ps_annotate*0.9))
        a.annotate('td: ' + str(td_annotate), xy=(td_annotate*0.8, pr_annotate*0.05))
        a.annotate('tc: ' + str(tc_annotate), xy=(tc_annotate*1.1, pr_annotate*0.02))

        a.grid(linestyle='-')

        win_front_wall = tk.Toplevel(self)
        win_front_wall.wm_title("Surface")
        l = tk.Label(win_front_wall, text="Surface")
        l.pack()

        canvas1 = FigureCanvasTkAgg(f1, win_front_wall)

        f2 = Figure(figsize=(4,4), dpi=100)
        b = f2.add_subplot(111)
        b.plot(pt_sfc_eq['x'], pt_sfc_eq['y'])
        b.set_xlabel('time (ms)')
        b.set_ylabel('pressure (kPa)')

        b.annotate('Pr: ' + str(pr_annotate), xy=(te_annotate*0.05, pr_annotate*0.97))
        b.annotate('te: ' + str(te_annotate), xy=(te_annotate*0.8, pr_annotate*0.03))

        b.grid(linestyle='-')

        win_eq_loading = tk.Toplevel(self)
        win_eq_loading.wm_title("Surface")
        l = tk.Label(win_eq_loading, text="Surface")
        l.pack()

        canvas2 = FigureCanvasTkAgg(f2, win_eq_loading)

        f3 = Figure(figsize=(4,4), dpi=100)
        c = f3.add_subplot(111)
        c.set_title('Friedlander Equation')
        c.plot(self.time, self.x_sfc_inc)
        c.plot(self.time, self.x_sfc_ref)

        c.grid(linestyle='-')

        graph = tk.Toplevel(self)
        graph.wm_title("Surface")
        label_graph = tk.Label(graph, text="Surface")
        label_graph.pack()

        canvas3 = FigureCanvasTkAgg(f3, graph)

        canvas1.show()
        canvas2.show()
        canvas3.show()

        canvas1._tkcanvas.pack()
        canvas2._tkcanvas.pack()
        canvas3._tkcanvas.pack()

        self.show_outputs('Surface', points)

    def show_outputs(self, type_txt, points):
        label_output_type = tk.Label(self, text="output type: " + type_txt)
        label_output_type.grid(row=2, column=3, columnspan=4, pady=5)

        if type_txt == 'Air':
            outputs = points['air']['outputs']
        else:
            outputs = points['surface']['outputs']

        label_output_val_1 = tk.Label(self, text=outputs['ps'])
        label_output_val_2 = tk.Label(self, text=outputs['is'])
        label_output_val_3 = tk.Label(self, text=outputs['pr'])
        label_output_val_4 = tk.Label(self, text=outputs['ir'])
        label_output_val_5 = tk.Label(self, text=outputs['u'])
        label_output_val_6 = tk.Label(self, text=outputs['ta'])
        label_output_val_7 = tk.Label(self, text=outputs['td'])
        label_output_val_1.grid(row=3, column=4, padx=5, pady=5)
        label_output_val_2.grid(row=4, column=4, padx=5, pady=5)
        label_output_val_3.grid(row=5, column=4, padx=5, pady=5)
        label_output_val_4.grid(row=6, column=4, padx=5, pady=5)
        label_output_val_5.grid(row=7, column=4, padx=5, pady=5)
        label_output_val_6.grid(row=8, column=4, padx=5, pady=5)
        label_output_val_7.grid(row=9, column=4, padx=5, pady=5)

    def show_output_template(self):
        label_output = tk.Label(self, text="OUTPUTS", fg="blue")
        label_output_1 = tk.Label(self, text="Peak Incident Pressure(Ps) [kPa]")
        label_output_2 = tk.Label(self, text="Incident Impulse(Is) [kPa.msec]")
        label_output_3 = tk.Label(self, text="Peak Reflected Pressure(Pr) [kPa]")
        label_output_4 = tk.Label(self, text="Reflected Impulse(Ir) [kPa.msec]")
        label_output_5 = tk.Label(self, text="Shock Front Velocity(U) [m/msec]")
        label_output_6 = tk.Label(self, text="Arrival Time(Ta) [msec]")
        label_output_7 = tk.Label(self, text="Positive Phase Duration(T+) [msec]")

        label_output.grid(row=1, column=3, columnspan=4, pady=10)
        label_output_1.grid(row=3, column=3, pady=5)
        label_output_2.grid(row=4, column=3, pady=5)
        label_output_3.grid(row=5, column=3, pady=5)
        label_output_4.grid(row=6, column=3, pady=5)
        label_output_5.grid(row=7, column=3, pady=5)
        label_output_6.grid(row=8, column=3, pady=5)
        label_output_7.grid(row=9, column=3, pady=5)

        label_output_val_1 = tk.Label(self, text="    ")
        label_output_val_2 = tk.Label(self, text="    ")
        label_output_val_3 = tk.Label(self, text="    ")
        label_output_val_4 = tk.Label(self, text="    ")
        label_output_val_5 = tk.Label(self, text="    ")
        label_output_val_6 = tk.Label(self, text="    ")
        label_output_val_7 = tk.Label(self, text="    ")
        label_output_val_1.grid(row=3, column=4, padx=5, pady=5)
        label_output_val_2.grid(row=4, column=4, padx=5, pady=5)
        label_output_val_3.grid(row=5, column=4, padx=5, pady=5)
        label_output_val_4.grid(row=6, column=4, padx=5, pady=5)
        label_output_val_5.grid(row=7, column=4, padx=5, pady=5)
        label_output_val_6.grid(row=8, column=4, padx=5, pady=5)
        label_output_val_7.grid(row=9, column=4, padx=5, pady=5)

        label_output_val1_unit = tk.Label(self, text="kPa")
        label_output_val2_unit = tk.Label(self, text="kPa.msec")
        label_output_val3_unit = tk.Label(self, text="kPa")
        label_output_val4_unit = tk.Label(self, text="kPa.msec")
        label_output_val5_unit = tk.Label(self, text="m/msec")
        label_output_val6_unit = tk.Label(self, text="msec")
        label_output_val7_unit = tk.Label(self, text="msec")
        label_output_val1_unit.grid(row=3, column=5, padx=5, pady=5)
        label_output_val2_unit.grid(row=4, column=5, padx=5, pady=5)
        label_output_val3_unit.grid(row=5, column=5, padx=5, pady=5)
        label_output_val4_unit.grid(row=6, column=5, padx=5, pady=5)
        label_output_val5_unit.grid(row=7, column=5, padx=5, pady=5)
        label_output_val6_unit.grid(row=8, column=5, padx=5, pady=5)
        label_output_val7_unit.grid(row=9, column=5, padx=5, pady=5)

    def get_graph_x(self, ta):
        result = []
        no_data = None

        for t in self.time:
            if (t - ta) > 0:
                result.append(t - ta)
            else:
                if (t - ta) < - 0.25:
                    result.append(no_data)
                else:
                    result.append(0)
        return result


    def get_graph_x_final(self, p, ta, tp, x):
        storage = []
        for idx, item in enumerate(x):
            if self.time[idx] - ta > - 0.25:
                x = p * ( 1 - item / tp) * math.exp(-self.b * item / tp)
                storage.append(x)
            else:
                storage.append(0)
        return storage



if __name__ == "__main__":
    app = Window()
    app.mainloop()
