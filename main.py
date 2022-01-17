# Import package
from tkinter import *
from tkinter import messagebox
import joblib
import numpy as np


class App(Tk):
    def __init__(self, model, std_scaler):
        super().__init__()
        self.model = model
        self.std_scaler = std_scaler

        # configure the root window
        self.title('House Price Prediction')
        self.resizable(width=False, height=False)
        self.geometry('850x750')

        # label
        self.lbl1 = Label(self, text='Welcome!!!', font=('Consolas Bold', 25), pady=20)
        self.lbl2 = Label(self, text="""       
        You can predict the house price in Paris by selecting the desired features below,
        the software will predict the price for you.
        """.strip(), pady=10, font=('Consolas Italic', 10))
        self.lbl3 = Label(self, text='--------------------------------------------------------------------------------------------------------------------------------')
        self.lbl_squaremeter = Label(self, text='Square Meters (square meters)', font=('Consolas', 10))
        self.lbl_yard = Label(self, text='Has Yard', font=('Consolas', 10))
        self.lbl_pool = Label(self, text='Has Pool', font=('Consolas', 10))
        self.lbl_floors = Label(self, text='Floors', font=('Consolas', 10))
        self.lbl_citypartrange = Label(self, text='City Part Range', font=('Consolas', 10))
        self.lbl_prevowners = Label(self, text='Num Prev Owners', font=('Consolas', 10))
        self.lbl_newbuild = Label(self, text='Is New Build', font=('Consolas', 10))
        self.lbl_stormprotector = Label(self, text='Has Storm Protector', font=('Consolas', 10))
        self.lbl_basement = Label(self, text='Basement (square meters)', font=('Consolas', 10))
        self.lbl_garage = Label(self, text='Garage (square meters)', font=('Consolas', 10))
        self.lbl_storageroom = Label(self, text='Has Storage Room', font=('Consolas', 10))
        self.lbl_totalroom = Label(self, text='Total Room', font=('Consolas', 10))

        # set location for label
        self.lbl1.pack()
        self.lbl2.pack()
        self.lbl3.pack()
        self.lbl_squaremeter.place(x=150, y=200)
        self.lbl_yard.place(x=150, y=240)
        self.lbl_pool.place(x=150, y=280)
        self.lbl_floors.place(x=150, y=320)
        self.lbl_citypartrange.place(x=150, y=360)
        self.lbl_prevowners.place(x=150, y=400)
        self.lbl_newbuild.place(x=150, y=440)
        self.lbl_stormprotector.place(x=150, y=480)
        self.lbl_basement.place(x=150, y=520)
        self.lbl_garage.place(x=150, y=560)
        self.lbl_storageroom.place(x=150, y=600)
        self.lbl_totalroom.place(x=150, y=640)

        # entry
        self.txt_squaremeters = Entry(self, width=20)
        self.txt_basement = Entry(self, width=20)
        self.txt_garage = Entry(self, width=20)
        self.txt_totalroom = Entry(self, width=20)

        # set location for entry
        self.txt_squaremeters.place(x=550, y=200)
        self.txt_basement.place(x=550, y=520)
        self.txt_garage.place(x=550, y=560)
        self.txt_totalroom.place(x=550, y=640)

        # radiobutton
        self.selected_yard = IntVar()
        self.rad_yard_yes = Radiobutton(self, text='Yes', value=1, variable=self.selected_yard)
        self.rad_yard_no = Radiobutton(self, text='No', value=0, variable=self.selected_yard)

        self.selected_pool = IntVar()
        self.rad_pool_yes = Radiobutton(self, text='Yes', value=1, variable=self.selected_pool)
        self.rad_pool_no = Radiobutton(self, text='No', value=0, variable=self.selected_pool)

        self.selected_built = IntVar()
        self.rad_built_yes = Radiobutton(self, text='Yes', value=1, variable=self.selected_built)
        self.rad_built_no = Radiobutton(self, text='No', value=0, variable=self.selected_built)

        self.selected_stormprotector = IntVar()
        self.rad_protector_yes = Radiobutton(self, text='Yes', value=1, variable=self.selected_stormprotector)
        self.rad_protector_no = Radiobutton(self, text='No', value=0, variable=self.selected_stormprotector)

        self.selected_storageroom = IntVar()
        self.rad_storage_yes = Radiobutton(self, text='Yes', value=1, variable=self.selected_storageroom)
        self.rad_storage_no = Radiobutton(self, text='No', value=0, variable=self.selected_storageroom)

        # set location for radiobutton
        self.rad_yard_yes.place(x=550, y=240)
        self.rad_yard_no.place(x=640, y=240)
        self.rad_pool_yes.place(x=550, y=280)
        self.rad_pool_no.place(x=640, y=280)
        self.rad_built_yes.place(x=550, y=440)
        self.rad_built_no.place(x=640, y=440)
        self.rad_protector_yes.place(x=550, y=480)
        self.rad_protector_no.place(x=640, y=480)
        self.rad_storage_yes.place(x=550, y=600)
        self.rad_storage_no.place(x=640, y=600)

        # spinbox
        self.spin_floors = Spinbox(self, from_=1, to=100, width=20)
        self.spin_citypart = Spinbox(self, from_=1, to=10, width=20)
        self.spin_prevowner = Spinbox(self, from_=1, to=100, width=20)

        # set location for spinbox
        self.spin_floors.place(x=550, y=320)
        self.spin_citypart.place(x=550, y=360)
        self.spin_prevowner.place(x=550, y=400)

        # button "predict"
        self.btn_predict = Button(self, text='Predict', font=('Consolas', 10), bd=5, bg='snow', command=self.check)

        # set location for button
        self.btn_predict.place(x=380, y=700)

        # explain button
        self.btn_explain = Button(self, text="?", font=('Consolas', 7), bd=3, command=self.explain)
        self.btn_explain.place(x=50, y=200)

    def check(self):
        if (self.txt_squaremeters.get().isnumeric() and self.txt_basement.get().isnumeric()) and (self.txt_totalroom.get().isnumeric() and self.txt_garage.get().isnumeric())\
                and (self.spin_floors.get().isnumeric()) and (self.spin_prevowner.get().isnumeric()) and (self.spin_citypart.get().isnumeric()):
            self.predict()
        else:
            messagebox.showerror("Error!!!", """
            The value in 'Square Meters' | 'Basement' | 'Garage' | 'Total Room' | 'Floors' | 'City Part Range' | 'Num Prev Owners' must be a numeric.
            """.strip())

    def predict(self):
        # Feature['squareMeters', 'hasYard', 'hasPool', 'floors', 'cityPartRange',
        #        'numPrevOwners', 'isNewBuilt', 'hasStormProtector', 'basement',
        #        'garage', 'hasStorageRoom', 'price', 'totalRoom']

        result = np.array([[int(self.txt_squaremeters.get()), self.selected_yard.get(), self.selected_pool.get(),
                  int(self.spin_floors.get()), int(self.spin_citypart.get()),int(self.spin_prevowner.get()),
                  int(self.selected_built.get()), self.selected_stormprotector.get(), int(self.txt_basement.get()),
                  int(self.txt_garage.get()), self.selected_storageroom.get(), int(self.txt_totalroom.get())]])

        result_scaled =  (self.std_scaler.transform(result)).reshape(1, -1)
        predict = self.model.predict(result_scaled)
        messagebox.showinfo("Predict", "Predict house price is: " + str("{:.1f}".format(predict[0])) + " $")

    def explain(self):
        window_mini = Tk()
        window_mini.title("Explain")
        window_mini.geometry("550x450")

        # Set label
        lbl_1 = Label(window_mini, text="Square Meters: is size of house in square meters", font=('Consolas Italic', 10), pady=10)
        lbl_2 = Label(window_mini, text="Has Yard: does house include yard?", font=('Consolas Italic', 10))
        lbl_3 = Label(window_mini, text="Has Pool: does house include pool?", font=('Consolas Italic', 10), pady=10)
        lbl_4 = Label(window_mini, text="Floors: how many floors are there?", font=('Consolas Italic', 10))
        lbl_5 = Label(window_mini, text="City Part Range: range -0- cheapest, 10 - the mose expensive", font=('Consolas Italic', 10), pady=10)
        lbl_6 = Label(window_mini, text="Num Prev Owners: number of previous owners", font=('Consolas Italic', 10))
        lbl_7 = Label(window_mini, text="Is New Built: is it new or renovated?", font=('Consolas Italic', 10), pady=10)
        lbl_8 = Label(window_mini, text="Has Storm Protector: is that house storm protector?", font=('Consolas Italic', 10))
        lbl_9 = Label(window_mini, text="Basement: basement square meters", font=('Consolas Italic', 10), pady=10)
        lbl_10 = Label(window_mini, text="Garage: garage size", font=('Consolas Italic', 10))
        lbl_11 = Label(window_mini, text="Storage room: does house include storage room?", font=('Consolas Italic', 10), pady=10)
        lbl_12 = Label(window_mini, text="Total room: how many rooms are there in the house?", font=('Consolas Italic', 10))

        # Set location
        lbl_1.grid(sticky=W)
        lbl_2.grid(sticky=W)
        lbl_3.grid(sticky=W)
        lbl_4.grid(sticky=W)
        lbl_5.grid(sticky=W)
        lbl_6.grid(sticky=W)
        lbl_7.grid(sticky=W)
        lbl_8.grid(sticky=W)
        lbl_9.grid(sticky=W)
        lbl_10.grid(sticky=W)
        lbl_11.grid(sticky=W)
        lbl_12.grid(sticky=W)

        window_mini.mainloop()

if __name__ == "__main__":
    lin_reg = joblib.load('model/my_lin_reg_model.pkl')
    std = joblib.load('model/standard_scaler.pkl')
    app = App(lin_reg, std)
    app.mainloop()