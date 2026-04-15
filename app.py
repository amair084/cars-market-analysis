# Car Listing Analysis App using Cars.com - Amair084 on GitHub
from asyncio import wait

import customtkinter as ctk
from PIL import Image

from scrapers.scraper import Scrape
from cleaner.data_clean import Clean
from analysis.plot import Plot
from analysis.viewer import CSVViewer
from pathlib import Path
import os, sys

def get_data_dir():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = Path(__file__).parent
    data_dir = Path(base) / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir

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
        self.brandname = ctk.CTkLabel(self.mainframe, text="Make:", height=8)
        self.trim = ctk.CTkEntry(self.mainframe)
        self.trimname = ctk.CTkLabel(self.mainframe, text="Model:", height=8)
        self.startbutton = ctk.CTkButton(self.mainframe, command=self.scrape, text="Analyse Listings", fg_color="#8136B2", hover_color="#AB74CF", width=150, height=30)
        self.brand.place(x=325, y=185)
        self.brandname.place(x=375, y=166)
        self.trim.place(x=325,y=235)
        self.trimname.place(x=375, y=216)
        self.startbutton.place(x=320,y=345)

        self.pagenumberentry = ctk.CTkOptionMenu(self.mainframe, values=["1","2","3","4","5"], width=120,height=20,fg_color="#3b3b3b", button_color="#8136B2", button_hover_color="#AB74CF")
        self.pagenumberentry.place(x=335, y=298)

        self.pagenumbetext = ctk.CTkLabel(self.mainframe, text="Choose # of pages to scrape")
        self.pagenumbetext.place(x=317, y=270)

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
        self.trimname.destroy()
        self.brandname.destroy()

        self.text = ctk.CTkLabel(self.mainframe, text="Completed Scraping and Cleaning..")
        self.text.place(x=309, y=160)

        self.backbutton = ctk.CTkButton(self.mainframe, command=self.reset, text="Back", fg_color="#8B0000", hover_color="#FF0000")
        self.backbutton.place(x=25, y=35)

        self.pvmbutton = ctk.CTkButton(self.mainframe, command=self.priceplot, text="Price vs Model", fg_color="#8136B2", hover_color="#AB74CF")
        self.pvmbutton.place(x=325, y=215)

        self.pvabutton = ctk.CTkButton(self.mainframe, command=self.ageplot, text="Price vs Age", fg_color="#8136B2", hover_color="#AB74CF")
        self.pvabutton.place(x=325, y=260)

        self.viewbutton = ctk.CTkButton(self.mainframe, command=self.viewcsv,
                                        text="View Data", fg_color="#8136B2", hover_color="#AB74CF")
        self.viewbutton.place(x=325, y=310)

    # Scrape Function ----------

    def scrape(self):
        self.text = ctk.CTkLabel(self.mainframe, text="Scraping has started..")
        self.text.place(x=310, y=150)

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
        self.viewbutton.destroy()
        self.text.destroy()

        self.brand = ctk.CTkEntry(self.mainframe)
        self.brandname = ctk.CTkLabel(self.mainframe, text="Make:", height=8)
        self.trim = ctk.CTkEntry(self.mainframe)
        self.trimname = ctk.CTkLabel(self.mainframe, text="Model:", height=8)
        self.startbutton = ctk.CTkButton(self.mainframe, command=self.scrape, text="Analyse Listings",
                                         fg_color="#8136B2", hover_color="#AB74CF", width=150, height=30)
        self.brand.place(x=325, y=185)
        self.brandname.place(x=375, y=166)
        self.trim.place(x=325, y=235)
        self.trimname.place(x=375, y=216)
        self.startbutton.place(x=320, y=345)

        self.pagenumberentry = ctk.CTkOptionMenu(self.mainframe, values=["1", "2", "3", "4", "5"], width=120, height=20,
                                                 fg_color="#3b3b3b", button_color="#8136B2",
                                                 button_hover_color="#AB74CF")
        self.pagenumberentry.place(x=335, y=298)

        self.pagenumbetext = ctk.CTkLabel(self.mainframe, text="Choose # of pages to scrape")
        self.pagenumbetext.place(x=317, y=270)

    def priceplot(self):
        plot = Plot(self.name)
        plot.python_plot()
        print(self.name)

    def ageplot(self):
        plot = Plot(self.name)
        plot.age_plot()
        print(self.name)

    def viewcsv(self):
        path = get_data_dir() / f"{self.name.lower()}_market_data.csv"
        CSVViewer(path)


if __name__ == "__main__":
    app = App()
    app.mainloop()