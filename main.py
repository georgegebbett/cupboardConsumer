import time
import tkinter as tk
import configparser
import json
import os
import requests

# open and read the config file
config = configparser.ConfigParser()
config.read('./config.ini')

# set Grocy variables
grocyApiUrl = config['grocy']['apiBaseURL']
grocyApiKey = config['grocy']['apiKey']

runFullscreen = config.getboolean('general', 'fullscreen')
LARGE_FONT = ("Verdana", 25)

headers = {'GROCY-API-KEY': grocyApiKey}
itemRes = requests.get(grocyApiUrl + "objects/products?query%5B%5D=location_id%3D6", headers=headers)

items = json.loads(itemRes.content)

print(items)


class HomeController(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        if runFullscreen:
            self.attributes('-fullscreen', True)
            self.config(cursor="none")

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry('320x480')

        self.frames = {}

        for F in (
                SplashScreen, ItemsPage, QuantityPage, ConsumeResultPage):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SplashScreen)

        self.show_frame(ItemsPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class SplashScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(2, weight=1)

        label = tk.Label(self, text="Cupboard Consumer\nLoading...", font=LARGE_FONT)
        label.grid(column=0, row=0, sticky='NSEW')

        # controller.show_frame(StartPage)


class ItemsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Items", font=LARGE_FONT)
        label.grid(column=0, row=0, sticky='EW', columnspan=2)

        i = 0
        for item in items:
            button = tk.Button(self, text=item['name'], font=LARGE_FONT, wraplength='140',
                               command=lambda itemRef=item: openQuantityPage(itemRef, controller))
            setattr(button, 'id', item['id'])
            button.grid(column=i % 2, row=int(i / 2) + 1, sticky="NSEW")
            self.grid_columnconfigure(i % 2, weight=1)
            self.grid_rowconfigure(int(i / 2) + 1, weight=1)

            i += 1



class QuantityPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.quantity = tk.StringVar()
        self.itemId = tk.StringVar()
        self.itemName = tk.StringVar()

        label = tk.Label(self, textvariable=self.quantity, font=LARGE_FONT)
        label.grid(column=0, row=0, sticky='EW', columnspan=3)

        button = tk.Button(self, text="1", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.appendToQuantity("1"))
        button.grid(column=0, row=1, sticky="NSEW")

        button = tk.Button(self, text="2", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.appendToQuantity("2"))
        button.grid(column=1, row=1, sticky="NSEW")

        button = tk.Button(self, text="3", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.appendToQuantity("3"))
        button.grid(column=2, row=1, sticky="NSEW")

        button = tk.Button(self, text="4", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.appendToQuantity("4"))
        button.grid(column=0, row=2, sticky="NSEW")

        button = tk.Button(self, text="5", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.appendToQuantity("5"))
        button.grid(column=1, row=2, sticky="NSEW")

        button = tk.Button(self, text="6", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.appendToQuantity("6"))
        button.grid(column=2, row=2, sticky="NSEW")

        button = tk.Button(self, text="7", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.appendToQuantity("7"))
        button.grid(column=0, row=3, sticky="NSEW")

        button = tk.Button(self, text="8", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.appendToQuantity("8"))
        button.grid(column=1, row=3, sticky="NSEW")

        button = tk.Button(self, text="9", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.appendToQuantity("9"))
        button.grid(column=2, row=3, sticky="NSEW")

        button = tk.Button(self, text="0", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.appendToQuantity("0"))
        button.grid(column=0, row=4, sticky="NSEW")

        button = tk.Button(self, text="<", wraplength='140', font=LARGE_FONT,
                           command=lambda: self.backspaceQuantity())
        button.grid(column=1, row=4, sticky="NSEW", columnspan=2)

        button = tk.Button(self, text="Consume", wraplength='320', font=LARGE_FONT,
                           command=lambda: self.doConsume(self.itemId.get(), self.itemName.get()))
        button.grid(column=0, row=5, sticky="NSEW", columnspan=3)

    def appendToQuantity(self, quant):
        if self.quantity.get() == "1":
            self.quantity.set(quant)
        else:
            self.quantity.set(self.quantity.get() + quant)

    def backspaceQuantity(self):
        if self.quantity.get() == "":
            self.controller.show_frame(ItemsPage)
        self.quantity.set(self.quantity.get()[0:-1])

    def doConsume(self, itemId, itemName):
        consumeHeaders = {
            'GROCY-API-KEY': grocyApiKey,
            'Content-Type': 'application/json'
        }

        data = json.dumps({
            "amount": self.quantity.get(),
            "transaction_type": "consume",
            "spoiled": False
        })
        print(data);
        consumeRes = requests.post(grocyApiUrl + "stock/products/" + itemId + "/consume", headers=consumeHeaders, data=data)
        if consumeRes.status_code == 200:
            openResultPage(itemName, self.quantity.get(), True, self.controller)
        else:
            openResultPage(json.loads(consumeRes.text)["error_message"], self.quantity.get(), False, self.controller)


class ConsumeResultPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.success = tk.BooleanVar()
        self.message = tk.StringVar()

        label = tk.Label(self, textvariable=self.message, font=LARGE_FONT, wraplength='320')
        label.grid(column=0, row=0, sticky='NSEW')

        button = tk.Button(self, text="OK", wraplength='320', font=LARGE_FONT,
                           command=lambda: controller.show_frame(ItemsPage))
        button.grid(column=0, row=1, sticky="NSEW")


def openQuantityPage(item, controller):
    print("quantity for", item['name'])
    app.frames[QuantityPage].quantity.set(item["quick_consume_amount"])
    app.frames[QuantityPage].itemId.set(item["id"])
    app.frames[QuantityPage].itemName.set(item["name"])
    controller.show_frame(QuantityPage)


def openResultPage(item, quantity, success, controller):
    app.frames[ConsumeResultPage].success.set(success)
    if success:
        app.frames[ConsumeResultPage].message.set("Successfully consumed " + quantity + " of " + item)
    else:
        app.frames[ConsumeResultPage].message.set("Error during consumption\n" + item)

    controller.show_frame(ConsumeResultPage)


app = HomeController()

app.mainloop()
