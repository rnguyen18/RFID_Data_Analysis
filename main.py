import HnM_Module
import Delta_Module


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
    date = [12, 19, 2019]
    deltaCSV = Delta_Module.Delta_Dataframe("Delta CSV", "../Delta Files/read/2019{0}{1}_BSM_PIER2.csv".format(
                                 str(date[0]).zfill(2), str(date[1]).zfill(2)),
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


Delta_Main()

