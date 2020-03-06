import HnM_Module


def parseGroup(title, path, type, amount):
    group = []
    for i in range(1, amount+1):
        group.append(CSV.HNM_CSV_File(title.format(i), path.format(i), type))
    return group


Master_Floor = HnM_Module.HnM_Dataframe("HNM_SalesFloor_CSV",
                                        "../files/HnM/read/MASTERFILE_Complete.xlsx",
                                        HnM_Module.File_Type.Expected_SalesFloor)
Master_Floor.writeCSV()

Master_Stock = HnM_Module.HnM_Dataframe("HNM_StockRoom_CSV",
                                        "../files/HnM/read/MASTERFILE_Complete.xlsx",
                                        HnM_Module.File_Type.Expected_StockRoom)
Master_Stock.writeCSV()

