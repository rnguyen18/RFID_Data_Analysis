import HnM_Module
import Delta_Module
import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as filedialog
from functools import partial


def HnM_Main():
    def parseGroup(title, path, typ, amount):
        group = []
        for i in range(1, amount+1):
            group.append(HnM_Module.HnM_Dataframe(title.format(i), path.format(i), typ))
        return group

    Master_Floor = HnM_Module.HnM_Dataframe("HNM_SalesFloor_CSV",
                                            "../files/HnM/read/MASTERFILE_Complete.xlsx",
                                            HnM_Module.File_Type.Expected_SalesFloor)
    Master_Floor.writeCSV()

    Master_Stock = HnM_Module.HnM_Dataframe("HNM_StockRoom_CSV",
                                            "../files/HnM/read/MASTERFILE_Complete.xlsx",
                                            HnM_Module.File_Type.Expected_StockRoom)
    Master_Stock.writeCSV()


def Delta_Main():
    date = [12, 10, 2019]
    String = "../Delta Files/read/2019{0}{1}_BSM_PIER2.csv".format(str(date[0]).zfill(2), str(date[1]).zfill(2))
    deltaCSV = Delta_Module.Delta_Dataframe("Delta CSV", String,
                                 Delta_Module.File_Type.DELTA)

    attCSV = Delta_Module.Delta_Dataframe("ATT CSV", "../Delta Files/read/Delta_AU_EBT Data_BR_AT_{0}{1}19__PT_0259.csv".format(
                               str(date[0]).zfill(2), str(date[1]+1).zfill(2)),
                               Delta_Module.File_Type.ATT)

    print("Analysis for {0}/{1}/{2}\n".format(date[0], date[1], date[2]))
    delta_analysis = Delta_Module.Delta_Analysis("Delta based Accuracy {0}-{1}-{2}".format(date[0], date[1], date[2]),
                                                 deltaCSV, attCSV)
    delta_analysis.printStatistics()
    print()
    att_analysis = Delta_Module.Delta_Analysis("AT&T based Accuracy {0}-{1}-{2}".format(date[0], date[1], date[2]),
                                               attCSV, deltaCSV)
    att_analysis.printStatistics()
    print()

    delta_analysis.exportStatistics("../Delta Files/write/{0}.xlsx".format(delta_analysis.title))


def Delta_Analysis(entry1, entry2):
    path1 = entry1.get()
    path2 = entry2.get()


def openFileDialog(entry):
    path = filedialog.askopenfilename(initialdir = "/RFID_Lab/Delta Files/read",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    entry.delete(0, tk.END)
    entry.insert(0, path)
    return path


def initGUI():
    root = tk.Tk()
    root.title("Delta Analysis Software")
    var1 = tk.IntVar()
    titleFont = tkFont.Font(size=15)
    buttonFont = tkFont.Font(size=12)

    tk.Label(root, text="Delta Analysis Software", font=titleFont).pack()

    frame_file1 = tk.Frame(root, padx=5, pady=5)
    frame_file1.pack(fill=tk.X)
    tk.Label(frame_file1, text="Primary File", font=buttonFont, width=12).pack(side=tk.LEFT)
    entry1 = tk.Entry(frame_file1, width=30)
    entry1.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)
    tk.Button(frame_file1, text="Select File", command=partial(openFileDialog, entry1)).pack(side=tk.LEFT)

    frame_settings1 = tk.Frame(root, padx=5, pady=5)
    frame_settings1.pack()
    radio1_delta = tk.Radiobutton(frame_settings1, text="Delta", variable=var1, value=1)
    radio1_att = tk.Radiobutton(frame_settings1, text="ATT", variable=var1, value=2)
    radio1_delta.pack(side=tk.LEFT, fill=tk.X)
    radio1_att.pack(side=tk.RIGHT, fill=tk.X)

    frame_file2 = tk.Frame(root, padx=5, pady=5)
    frame_file2.pack(fill=tk.X)
    tk.Label(frame_file2, text="Secondary File", font=buttonFont, width=12).pack(side=tk.LEFT)
    entry2 = tk.Entry(frame_file2, width=30)
    entry2.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)
    tk.Button(frame_file2, text="Select File", command=partial(openFileDialog, entry2)).pack(side=tk.LEFT)

    frame_settings2 = tk.Frame(root, padx=5, pady=5)
    frame_settings2.pack()
    radio2_delta = tk.Radiobutton(frame_settings2, text="Delta", variable=var1, value=2)
    radio2_att = tk.Radiobutton(frame_settings2, text="ATT", variable=var1, value=1)
    radio2_delta.pack(side=tk.LEFT, fill=tk.X)
    radio2_att.pack(side=tk.RIGHT, fill=tk.X)

    tk.Button(root, text="Perform Analysis", command=partial(Delta_Analysis, entry1, entry2)).pack(side=tk.BOTTOM, pady=5)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()


initGUI()


