import abc
import pandas as pd


def prefixFilter(word, prefixes_array):
    for i, prefix_array in enumerate(prefixes_array):
        if prefix_array:
            if not (word[i] in prefix_array):
                return False

    return True


class RFID_Dataframe:
    column_labels = []
    column_table = {}

    def __init__(self, title, path, file_type):
        self.title = title
        self.path = path
        self.file_type = file_type
        self.data_frame = self.parse()
        self.filterData()

    def print(self):
        print(self.data_frame)

    def printCount(self):
        print(self.data_frame.count())

    def printValues(self):
        for i, v in self.data_frame.iterrows():
            print(v.values[0])

    def dropDuplicates(self,column):
        return self.data_frame.drop_duplicates(column, keep='first', inplace=True)

    def writeCSV(self, path=""):
        if path != "":
            self.data_frame.to_csv(path)
        else:
            print("Invalid Path")
        # Path = path if path != "" else "../files/HnM/write/{0}.csv".format(self.title)


    def filterWithPrefix(self, column, char_array):
        self.data_frame = self.data_frame[self.data_frame.apply(
            lambda x: prefixFilter(str(x[column]), char_array), axis=1
        )]

    def filterToInts(self, column):
        self.data_frame[column] = pd.to_numeric(self.data_frame[column], errors="coerce")
        self.data_frame.dropna(subset=[column], inplace=True)
        self.data_frame = self.data_frame.astype({column: "int64"})

    @abc.abstractmethod
    def parse(self):
        raise NotImplementedError

    @abc.abstractmethod
    def filterData(self):
        raise NotImplementedError


class RFID_Analysis:

    def __init__(self, title, primary_dataframe, secondary_dataframe, column=0):
        self.title = title

        self.primary_dataframe = primary_dataframe
        self.primary_total = len(primary_dataframe.data_frame.index)

        self.secondary_dataframe = secondary_dataframe
        self.secondary_total = len(secondary_dataframe.data_frame.index)

        self.primary_ids = self.primary_dataframe.data_frame[self.primary_dataframe.data_frame.columns[column]]
        self.secondary_ids = self.secondary_dataframe.data_frame[self.secondary_dataframe.data_frame.columns[column]]

    def calc_Accurate(self):
        accurate_count = 0
        for _, v in self.primary_ids.iteritems():
            if v in set(self.secondary_ids):
                accurate_count = accurate_count + 1

        return accurate_count

    def calc_Underread(self):
        underread_count = 0
        for _, v in self.primary_ids.iteritems():
            if not (v in set(self.secondary_ids)):
                underread_count = underread_count + 1

        return underread_count

    def calc_Overread(self):
        overread_count = 0
        for _, v in self.secondary_ids.iteritems():
            if not (v in set(self.primary_ids)):
                overread_count = overread_count + 1

        return overread_count

    def calcStatistics(self):
        accurate = self.calc_Accurate()
        underread = self.calc_Underread()
        overread = self.calc_Overread()

        accurate_percentage = round(100*accurate/self.primary_total)
        underread_percentage = round(100*underread/self.primary_total)
        overread_percentage = round(100*overread/self.primary_total)

        return [self.primary_total, self.secondary_total, accurate, accurate_percentage, underread, underread_percentage, overread, overread_percentage]

    def printStatistics(self):
        stats = self.calcStatistics()
        print("Total Primary: " + str(stats[0]))
        print("Total Secondary: " + str(stats[1]))

        print("Accurate: {0}".format(stats[2]))
        print("\tPercentage: {0}%".format(stats[3]))

        print("Underread: {0}".format(stats[4]))
        print("\tPercentage: {0}%".format(stats[5]))

        print("Overread: {0}".format(stats[6]))
        print("\tPercentage: {0}%".format(stats[7]))

    @abc.abstractmethod
    def exportStatistics(self):
        raise NotImplementedError

