# Car Listing Analysis App using Cars.com - Amair084 on GitHub

import customtkinter as ctk
from PIL import Image
from numpy.ma.core import size

from scrapers.scraper import Scrape
from cleaner.data_clean import Clean
from analysis.plot import Plot
import os, sys

def resource_path(path):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.dirname(__file__), path)

ctk.set_appearance_mode("dark")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        # Application Configuration ----------

        self.avggot = False
        self.title("Cars.com Market Analysis")
        self.geometry("800x465")
        self.resizable(False, False)
        self.iconbitmap(resource_path("resources/icon.ico"))

        self.mainframe = ctk.CTkFrame(self, width=765, height=430)
        self.mainframe.pack(padx=20, pady=20)

        self.brand = ctk.CTkEntry(self.mainframe)
        self.trim = ctk.CTkEntry(self.mainframe)
        self.startbutton = ctk.CTkButton(self.mainframe, command=self.scrape, text="Analyse Listings", fg_color="#8136B2", hover_color="#AB74CF", width=150, height=30)
        self.brand.place(x=325, y=175)
        self.trim.place(x=325,y=225)
        self.startbutton.place(x=320,y=335)

        self.pagenumberentry = ctk.CTkOptionMenu(self.mainframe, values=["1","2","3","4","5"], width=120,height=20,fg_color="#3b3b3b", button_color="#8136B2", button_hover_color="#AB74CF")
        self.pagenumberentry.place(x=335, y=288)

        self.pagenumbetext = ctk.CTkLabel(self.mainframe, text="Choose # of pages to scrape")
        self.pagenumbetext.place(x=317, y=260)

        logo = ctk.CTkImage(
            light_image=Image.open(resource_path("resources/logo.png")),
            dark_image=Image.open(resource_path("resources/logo.png")),
            size=(156, 173)
        )

        # Credits - Amair084 ----------

        gitlogo = ctk.CTkImage(
            light_image=Image.open(resource_path("resources/gitlgoo.png")),
            dark_image=Image.open(resource_path("resources/gitlgoo.png")),
            size=(40, 40)
        )

        logo_label = ctk.CTkLabel(self.mainframe, image=logo, text="")
        logo_label.image = logo
        logo_label.place(x=315, y=-15)

        gitlabel = ctk.CTkLabel(self.mainframe, image=gitlogo, text="")
        gitlabel.image = gitlogo
        gitlabel.place(x=5, y=380)

        gitaccount = ctk.CTkLabel(self.mainframe,text="amair084", font=("Arial", 15))
        gitaccount.place(x=50, y=386)

    # Plot Menu ----------

    def plotmenu(self):
        self.trim.destroy()
        self.startbutton.destroy()
        self.brand.destroy()
        self.pagenumbetext.destroy()
        self.pagenumberentry.destroy()

        self.text = ctk.CTkLabel(self.mainframe, text="Completed Scraping and Cleaning..")
        self.text.place(x=310, y=150)

        self.backbutton = ctk.CTkButton(self.mainframe, command=self.reset, text="Back", fg_color="#8B0000", hover_color="#FF0000")
        self.backbutton.place(x=25, y=35)

        self.pvmbutton = ctk.CTkButton(self.mainframe, command=self.priceplot, text="Price vs Model", fg_color="#8136B2", hover_color="#AB74CF")
        self.pvmbutton.place(x=325, y=195)

        self.pvabutton = ctk.CTkButton(self.mainframe, command=self.ageplot, text="Price vs Age", fg_color="#8136B2", hover_color="#AB74CF")
        self.pvabutton.place(x=325, y=240)

        self.avgbutton = ctk.CTkButton(self.mainframe, command=self.getavg, text="Average Price by Model", fg_color="#8136B2", hover_color="#AB74CF")
        self.avgbutton.place(x=321, y=295)

    # Scrape Function ----------

    def scrape(self):
        pages = int(self.pagenumberentry.get())
        name = self.trim.get()
        brand = self.brand.get()
        self.name = name
        print(brand)
        print(name)
        scraper = Scrape(pages, brand, name)
        clean = Clean(name)

        self.plotmenu()

    # Reset back to Original State ----------

    def reset(self):
        self.backbutton.destroy()
        self.pvmbutton.destroy()
        self.pvabutton.destroy()
        self.avgbutton.destroy()
        self.text.destroy()
        if self.avggot:
            self.text2.destroy()
            self.text3.destroy()

        self.brand = ctk.CTkEntry(self.mainframe)
        self.trim = ctk.CTkEntry(self.mainframe)
        self.startbutton = ctk.CTkButton(self.mainframe, command=self.scrape, text="Analyse Listings",
                                         fg_color="#8136B2", hover_color="#AB74CF", width=150, height=30)
        self.brand.place(x=325, y=175)
        self.trim.place(x=325, y=225)
        self.startbutton.place(x=320, y=335)

        self.pagenumberentry = ctk.CTkOptionMenu(self.mainframe, values=["1", "2", "3", "4", "5"], width=120, height=20,
                                                 fg_color="#3b3b3b", button_color="#8136B2", button_hover_color="#AB74CF")
        self.pagenumberentry.place(x=335, y=288)

        self.pagenumbetext = ctk.CTkLabel(self.mainframe, text="Choose # of pages to scrape")
        self.pagenumbetext.place(x=317, y=260)

    def priceplot(self):
        plot = Plot(self.name)
        plot.python_plot()
        print(self.name)

    def ageplot(self):
        plot = Plot(self.name)
        plot.age_plot()
        print(self.name)

    def getavg(self):
        plot = Plot(self.name)
        avg = plot.getavg()

        self.text2 = ctk.CTkLabel(self.mainframe, text="Average Price of Model:")
        self.text2.place(x=310, y=350)

        self.text3 = ctk.CTkLabel(self.mainframe, text=("$" + str(int(avg))))
        self.text3.place(x=310, y=375)

        self.avggot = True


if __name__ == "__main__":
    app = App()
    app.mainloop()