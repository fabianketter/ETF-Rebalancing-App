import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

#creates the tkinter class and presets basics
class RebalancingApp(tk.Tk):
    """
    ETF Rebalancing Calculator GUI Application.

    Diese Tkinter-Anwendung ermöglicht es, ein ETF-Portfolio mit
    mehreren ETFs und Zielallokationen einzutragen und berechnet:
    - Die nötigen Käufe/Verkäufe für ein sofortiges Rebalancing.
    - Die Anpassung der Sparraten zur schrittweisen Angleichung der Zielallokation.
    
    Features:
    - Dynamisch hinzufügbare ETF-Zeilen (Name, aktueller Wert, Zielprozente).
    - Validierung der Eingaben (Summe der Zielallokationen muss 100% ergeben).
    - Visualisierung der aktuellen und Zielallokationen als Kuchendiagramme.
    - Anzeige der Handlungsempfehlungen in zwei Textfeldern.
    - Benutzerfreundliches, farbiges Layout mit einfachen Navigationen.

    Wichtige Methoden:
    - add_etf_row: Fügt eine neue Eingabezeile für einen ETF hinzu.
    - calculate_rebalancing: Führt die Berechnung des Rebalancings durch und zeigt Ergebnisse.
    - show_plots: Erstellt und zeigt die Kuchendiagramme im GUI.
    - show_frame: Wechselt zwischen Eingabe- und Ausgabeansicht.
    
    Nutzung:
    Starte die App und trage ETFs mit deren aktuellem Wert und gewünschter Zielallokation ein.
    Gib die monatliche Sparrate ein.
    Klicke "Calculate Rebalancing" für die Empfehlungen.
    """
    def __init__(self):
        super().__init__()
        self.title("ETF Rebalancing Calculator")
        self.color_palette=['#4F378B', '#58B19F', '#FD7272', '#FC427B', '#BDC581', '#2C3A47', '#6D214F', '#55E6C1', '#F8EFBA']
        self.color = 'lightblue'
        self.button_color = 'pink'
        self.text_font = ("Arial", 14)
        self.configure(bg=self.color)
        self.state("zoomed")  # Maximiert das Fenster direkt beim Start
        self.frames = {}
        self.hyphen_number = 90

        self.init_input_view()
        self.init_output_view()
        self.show_frame("input")

    #defines a function to insert colored and justified text
    def insert_colored(self, text_widget, content, color, weight="normal"):
        text_widget.insert(tk.END, content)
        start = text_widget.index("end - %dc" % (len(content)+1))
        end = text_widget.index("end - 1c")
        font_style = ("Arial", 14, weight)
        tag_name = f"tag_{color}_{weight}_center"
        if tag_name not in text_widget.tag_names():
            text_widget.tag_configure(tag_name, foreground=color, font=font_style, justify="center")
        text_widget.tag_add(tag_name, start, end)

    def add_etf_row(self, name="", worth=0.0, allocation=0.0):
        row_index = len(self.etf_rows) + 3
        name_var = tk.StringVar(value=name)
        worth_var = tk.DoubleVar(value=worth)
        alloc_var = tk.DoubleVar(value=allocation)

        tk.Entry(self.etf_container, textvariable=name_var).grid(row=row_index, column=0, sticky = 'ew', padx=50, pady=4)
        tk.Entry(self.etf_container, textvariable=worth_var).grid(row=row_index, column=1, sticky = 'ew', padx=50, pady=4)
        tk.Entry(self.etf_container, textvariable=alloc_var).grid(row=row_index, column=2, sticky = 'ew', padx=50, pady=4)

        self.name_entries.append(name_var)
        self.value_entries.append(worth_var)
        self.alloc_entries.append(alloc_var)
        self.etf_rows.append((name_var, worth_var, alloc_var))

    #initializes the input view
    def init_input_view(self):
        frame = tk.Frame(self, bg =self.color)
        self.frames["input"] = frame

        # inside __init__, after you've created input_frame
        self.etf_container = tk.Frame(frame, bg=self.color)
        self.etf_container.grid(row=10, column=0, columnspan=3, sticky="ew", pady=(8,8))


        #creates the saving rate label
        tk.Label(self.etf_container, text="Saving rate (€ per month):", font=('Arial', 10, 'bold'), bg=self.color
                 ).grid(row=0, column=1, columnspan=1, sticky="ew", pady=(8,8))

        #sets the saving rate to 100
        self.saving_rate_var = tk.DoubleVar(value=1000)
        #entry field in the next row
        tk.Entry(self.etf_container, textvariable=self.saving_rate_var).grid(row=1, column=1, columnspan=1, sticky="ew", padx=50, pady=(0,8))

        # headers
        tk.Label(self.etf_container, font=('Arial', 10, 'bold'), text="ETF Name", bg=self.color).grid(row=2, column=0, sticky = 'ew', padx=50)
        tk.Label(self.etf_container, font=('Arial', 10, 'bold'), text="Current ETF worth (€)", bg=self.color).grid(row=2, column=1, sticky = 'ew', padx=50)
        tk.Label(self.etf_container, font=('Arial', 10, 'bold'), text="Target Allocation (%)", bg=self.color).grid(row=2, column=2, sticky = 'ew', padx=50)

        # keep references to rows
        self.etf_rows = []
        self.name_entries = []
        self.value_entries = []
        self.alloc_entries = []
        self.add_etf_row("MSCI World", 0, 49)  
        self.add_etf_row("MSCI EM IMI", 0, 14)
        self.add_etf_row("MSCI Small Caps", 0, 8)
        self.add_etf_row("Europe Stoxx 600", 0, 8)
        self.add_etf_row("MSCI Information Technology", 0, 8)
        self.add_etf_row("MSCI Global Semiconductors", 0, 8)
        self.add_etf_row("Bitcoin", 0, 3.21)
        self.add_etf_row("Ethereum", 0, 1.15)
        self.add_etf_row("Ripple", 0, 0.64)

        # button to add more rows
        tk.Button(
            self.etf_container,
            text="+ Add ETF",
            font=('Arial', 14, 'bold'),
            bg=self.button_color,
            command=self.add_etf_row
        ).grid(row=30, column=0, columnspan = 1, pady=10)

        #calculate rebalancing button
        tk.Button(
            self.etf_container,
            text="⮞ Calculate Rebalancing",
            font=("Arial", 14, "bold"),
            bg = self.button_color,
            command=self.calculate_rebalancing
        ).grid(row=30, column=1, columnspan=1, pady=10)

        #configure columns
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        #configure columns
        self.etf_container.grid_columnconfigure(0, weight=1)
        self.etf_container.grid_columnconfigure(1, weight=1)
        self.etf_container.grid_columnconfigure(2, weight=1)

    #initializes the output view
    def init_output_view(self):
        #overall frame
        frame = tk.Frame(self, bg=self.color)
        self.frames["output"] = frame

        #top frame
        text_frame = tk.Frame(frame, bg=self.color)
        text_frame.pack(pady=0)

        #free space top left
        self.top_free_spc_left = tk.Frame(text_frame, width=1, bg=self.color)
        self.top_free_spc_left.pack(side="left", fill="both", expand=True)

        #text for rebalancing through trading
        self.trade_text = tk.Text(
            text_frame,
            width=50,
            height=17,
            font=self.text_font,
            highlightbackground='black',
            highlightcolor='black',
            highlightthickness=2,
            padx=5
        )
        self.trade_text.pack(side=tk.LEFT, padx=1, pady=(10,1))

        #text for rebalancing through saving rate adaptation
        self.adjust_text = tk.Text(
            text_frame,
            width=50,
            height=17,
            font=self.text_font,
            highlightbackground='black',
            highlightcolor='black',
            highlightthickness=2,
            padx=5
        )
        self.adjust_text.pack(side=tk.LEFT, padx=1, pady=(10,1))

        #free space top right
        self.top_free_spc_right = tk.Frame(text_frame, width=1, bg=self.color)
        self.top_free_spc_right.pack(side="left", fill="both", expand=True)
        
        #bottom frame
        bottom_frame = tk.Frame(frame, bg=self.color)
        bottom_frame.pack(fill="both", expand=True)
        fixed_width = 199

        #bottom left free space
        left_spacer = tk.Frame(bottom_frame, bg=self.color, width=fixed_width)
        left_spacer.pack(side="left", fill="y")

        #plot frame
        self.plot_frame = tk.Frame(
            bottom_frame,
            bg='white',
            highlightbackground='black',
            highlightcolor='black',
            highlightthickness=2,
            padx = 5
        )
        self.plot_frame.pack(side="left", fill="both", expand=True, padx=2, pady=(0,10))

        #bottom right free space
        right_frame = tk.Frame(bottom_frame, bg=self.color, width=fixed_width)
        right_frame.pack(side="left", fill="y")

        #back buttom on the bottom right
        self.back_btn = tk.Button(
            right_frame,
            text="⮜ Back",
            command=lambda: self.show_frame("input"),
            font=("Arial", 14, "bold"),
            padx=30, pady=15,
            bg=self.button_color,
        )
        self.back_btn.pack(side="bottom", anchor="center", padx=20, pady=20)

        #prevent spacer width changes
        left_spacer.pack_propagate(False)
        right_frame.pack_propagate(False)

    #shows all frames
    def show_frame(self, name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    #core-calculates the rebalancing
    def calculate_rebalancing(self):
        try:
            worths = [float(e.get()) for e in self.value_entries]
            if sum(worths) == 0:
                messagebox.showerror("Error", "You have nothing in your portfolio?! \nWhy are you using this application?")
                return
            allocations = [float(a.get()) for a in self.alloc_entries]
            if sum(allocations) != 100:
                messagebox.showerror("Error", "Allocations must add up to 100%.")
                return
            saving_rate = self.saving_rate_var.get()
        except ValueError:
            messagebox.showerror("Error", "Please fill in valid numbers.")
            return

        #prepare values
        total_worth = sum(worths)
        dicts = []
        #store all data in dictionaries
        for i, etf_name in enumerate(self.name_entries):
            d = {
                'name': etf_name.get(),
                'alloc': allocations[i],
                'worth': worths[i],
                'worth_soll' : total_worth*(allocations[i]/100)
            }
            dicts.append(d)

        # Trade-Rebalancing (Buy/Sell)
        self.trade_text.delete("1.0", tk.END) #clears widget
        self.trade_text.insert(tk.END, "-" * self.hyphen_number + "\n")
        self.trade_text.insert(tk.END, "Rebalancing through Buy/Sell:\n")
        self.trade_text.insert(tk.END, "-" * self.hyphen_number + "\n")
        print(self.name_entries)


        perc_diff_list = []
        for d in dicts:                                                                                         #calculate soll-values from the allocation and the portfolio worth
            if d['worth_soll'] == 0:
                perc_diff_list.append(0)                                                                        #if one allocation is set to 0, exclude it from the rebalancing calculation
            else:                                                 
                perc_diff_list.append(d['worth']/d['worth_soll'])                                               #calculate the extent of over/underallocation                                                                     
        
            if d['worth_soll'] == d['worth']:
                self.trade_text.insert(tk.END, f"Do not trade {d['name']}\n")                                   #if asset is as its soll-value, do not trade it
            elif d['worth_soll'] > d['worth']:
                self.trade_text.insert(tk.END, f"Buy {round(d['worth_soll']-d['worth'])}€ of {d['name']}\n")    #if it is underallocated, buy the difference
            elif d['worth_soll'] < d['worth']:
                self.trade_text.insert(tk.END, f"Sell {round(d['worth']-d['worth_soll'])}€ of {d['name']}\n")   #if it is overallocated, sell the difference

        #print portfolio value
        self.trade_text.insert(tk.END, "-" * self.hyphen_number + "\n")
        self.trade_text.insert(tk.END, "-" * self.hyphen_number + "\n")
        self.insert_colored(self.trade_text, f"⮞⮞⮞ Portfolio Value: {round(total_worth)}€ ⮜⮜⮜\n", self.color_palette[0], "bold")
        self.trade_text.insert(tk.END, "-" * self.hyphen_number + "\n")
        self.trade_text.insert(tk.END, "-" * self.hyphen_number + "\n")

        # Via saving rate adaptation
        self.adjust_text.delete("1.0", tk.END)
        self.adjust_text.insert(tk.END, "-" * self.hyphen_number + "\n")
        self.adjust_text.insert(tk.END, f"Rebalancing through saving rate adaptation:\n")
        self.adjust_text.insert(tk.END, "-" * self.hyphen_number + "\n")
        self.adjust_text.insert(tk.END, f"Adjusting rates on {dicts[perc_diff_list.index(max(perc_diff_list))]['name']}....\n")
        self.adjust_text.insert(tk.END, "-" * self.hyphen_number + "\n")

        #calculate the total difference in allocation to soll-allocation
        total_difference = 0
        for d in dicts:
            if d['worth_soll'] == 0:
                continue
            elif d == dicts[perc_diff_list.index(max(perc_diff_list))]:
                continue
            else:
                d['worth_soll_new'] = d['worth_soll']*max(perc_diff_list)
                total_difference+=d['worth_soll_new']-d['worth']

        #calculate new saving rates
        for d in dicts:
            if d['worth_soll'] == 0: 
               self.adjust_text.insert(tk.END, f"Allocation of {d['name']} is 0, excluded\n")                                                                       #if allocation is 0, exclude
            elif d == dicts[perc_diff_list.index(max(perc_diff_list))]:
                self.adjust_text.insert(tk.END, f"Adjust rate of {dicts[perc_diff_list.index(max(perc_diff_list))]['name']} to 0€\n")                               #do not invest into the most overallocated ETF for now
            elif round((saving_rate*(d['worth_soll_new']-d['worth']))/total_difference) == saving_rate*(d['alloc']/100):                                       #if the saving rate is the same rate as normal, keep it
                self.adjust_text.insert(tk.END, f"Keep rate of {d['name']} at {round((saving_rate*(d['worth_soll_new']-d['worth']))/total_difference)}€\n")
            else:
                self.adjust_text.insert(tk.END, f"Adjust rate of {d['name']} to {round((saving_rate*(d['worth_soll_new']-d['worth']))/total_difference)}€\n")  #if not, adjust the rate to the point that all ETFs reach their soll-allocation at the same time
        
        #print the time needed for soft rebalancing
        self.adjust_text.insert(tk.END, "-" * self.hyphen_number + "\n")
        self.adjust_text.insert(tk.END, f"Time to Adjust: {round(total_difference/saving_rate)} Months....\n")
        self.adjust_text.insert(tk.END, "-" * self.hyphen_number + "\n")

        #show the plots in the bottom frame
        self.show_plots(dicts, total_worth)
        #show the output frame
        self.show_frame("output")

    #function that creates the plots and shows them
    def show_plots(self, dicts, total_worth):
        # Remove all widgets except the back button
        for widget in self.plot_frame.winfo_children():
            if widget != self.back_btn:
                widget.destroy()

        fig, axs = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [1, 1], 'wspace': 0.4})
        actual = [d['worth'] / total_worth for d in dicts]      #actual allocation
        target = [d['alloc']/100 for d in dicts]                #soll-allocation
        labels = [d['name'] for d in dicts]                     #labels = names

        #1st plot: Actual allocation
        wedges1, _, autotexts1 = axs[0].pie(actual, labels=None, autopct='%1.1f%%', pctdistance=1.14,
                                            textprops={'fontsize': 10}, wedgeprops={'width': 0.4}, colors = self.color_palette[:len(labels)])
        axs[0].set_title("Current Allocation", font = 'Arial', fontsize = 12, fontweight = 'bold', pad = 10)
        #2nd plot: soll-allocation
        wedges2, _, autotexts2 = axs[1].pie(target, labels=None, autopct='%1.1f%%', pctdistance=1.14,
                                            textprops={'fontsize': 10}, wedgeprops={'width': 0.4}, colors = self.color_palette[:len(labels)])
        axs[1].set_title("Target-Allocation", font = 'Arial', fontsize = 12, fontweight = 'bold', pad = 10)

        # Legend between the plots
        fig.legend(wedges1, labels, loc='lower center', ncol=1, fontsize=10, frameon=False, bbox_to_anchor=(0.5, 0.25))
        fig.subplots_adjust(left=0.05, right=0.95)
        #draw plt figure into the frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, side="top")

#create instance of the class and run it
if __name__ == "__main__":
    app = RebalancingApp()
    app.mainloop()
