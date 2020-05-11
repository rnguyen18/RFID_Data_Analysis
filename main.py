import HnM_Module
import Delta_Module
import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as filedialog
from functools import partial


def openFileDialog(entry):
    path = filedialog.askopenfilename(initialdir = "/RFID_Lab/Delta Files/read",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    entry.delete(0, tk.END)
    entry.insert(0, path)
    return path


def saveFileDialog(entry):
    path = filedialog.asksaveasfilename(initialdir = "/RFID_Lab/Delta Files/write",title = "Create file",filetypes = (("excel files","*.xlsx"),("all files","*.*")))
    entry.delete(0, tk.END)
    entry.insert(0, path)
    return path


def exportAnalysis(root, analysis, entry):
    path = entry.get()

    if len(path) > 5:
        if path[-5:] != ".xlsx":
            path = path + ".xlsx"

    analysis.exportStatistics(entry.get())
    root.destroy()


def analysisGUI(analysis):
    stats = analysis.calcStatistics()
    root = tk.Tk()
    root.title("Delta Analysis Details")

    titleFont = tkFont.Font(size=15)
    dataFont = tkFont.Font(size=12)

    frame1 = tk.Frame(root, padx=5, pady=5)
    frame1.pack()
    tk.Label(frame1, text="Delta Analysis Details", font=titleFont).pack()

    frame2 = tk.Frame(frame1, padx=1, pady=5)
    frame2.pack()
    tk.Label(frame2, text="Total Primary: " + str(stats[0]), font=dataFont, anchor='w').pack(fill=tk.X)
    tk.Label(frame2, text="Total Secondary: " + str(stats[1]), font=dataFont, anchor='w').pack(fill=tk.X)
    tk.Label(frame2, text="Accurate: " + str(stats[2]), font=dataFont, anchor='w').pack(fill=tk.X)
    tk.Label(frame2, text="Percentage: " + str(stats[3]) + "%", font=dataFont, anchor='w').pack(fill=tk.X)
    tk.Label(frame2, text="Underread: " + str(stats[4]), font=dataFont, anchor='w').pack(fill=tk.X)
    tk.Label(frame2, text="Percentage: " + str(stats[5]) + "%", font=dataFont, anchor='w').pack(fill=tk.X)
    tk.Label(frame2, text="Overread: " + str(stats[6]), font=dataFont, anchor='w').pack(fill=tk.X)
    tk.Label(frame2, text="Percentage: " + str(stats[7]) + "%", font=dataFont, anchor='w').pack(fill=tk.X)

    tk.Label(root, text="File Path: ", font=dataFont, width=12).pack()
    frame_file = tk.Frame(root, padx=5, pady=5)
    frame_file.pack(fill=tk.X)
    entry = tk.Entry(frame_file, width=30)
    entry.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)
    tk.Button(frame_file, text="Choose Path", command=partial(saveFileDialog, entry)).pack(side=tk.LEFT)

    tk.Button(root, text="Export Data", font=dataFont, command=partial(exportAnalysis, root, analysis, entry)).pack(side=tk.BOTTOM, pady=5)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()
    print("Analysis")


def Delta_Analysis(root, entry1, entry2, var):
    path1 = entry1.get()
    path2 = entry2.get()
    type1 = Delta_Module.File_Type.ATT if (var.get() == 2) else Delta_Module.File_Type.DELTA
    type2 = Delta_Module.File_Type.DELTA if (var.get() == 2) else Delta_Module.File_Type.ATT

    primaryCSV = Delta_Module.Delta_Dataframe("Primary CSV", path1, type1)
    secondaryCSV = Delta_Module.Delta_Dataframe("Secondary CSV", path2, type2)
    print(secondaryCSV.data_frame)

    analysis = Delta_Module.Delta_Analysis("Analysis", primaryCSV, secondaryCSV)
    analysis.printStatistics()

    root.destroy()
    analysisGUI(analysis)


def fileGUI():
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

    tk.Button(root, text="Perform Analysis", command=partial(Delta_Analysis, root, entry1, entry2, var1)).pack(side=tk.BOTTOM, pady=5)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()


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

    # print("Analysis for {0}/{1}/{2}\n".format(date[0], date[1], date[2]))
    delta_analysis = Delta_Module.Delta_Analysis("Delta based Accuracy {0}-{1}-{2}".format(date[0], date[1], date[2]),
                                                 deltaCSV, attCSV)
    # delta_analysis.printStatistics()
    # print()
    att_analysis = Delta_Module.Delta_Analysis("AT&T based Accuracy {0}-{1}-{2}".format(date[0], date[1], date[2]),
                                               attCSV, deltaCSV)
    # att_analysis.printStatistics()
    # print()

    delta_analysis.exportStatistics("../Delta Files/write/{0}.xlsx".format(delta_analysis.title))

    analysisGUI(delta_analysis)


Delta_Main()