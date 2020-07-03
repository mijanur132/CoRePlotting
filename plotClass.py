import pandas as pd
class plotFig:
    """A class to create plot from text data"""
    data=""
    def __init__(self,dataSrc):
        self.dataSrc=dataSrc

    def processData(self, i):
        """A method to extract numerical data from text file"""
        print("dataSrc")
        df_temp = pd.read_csv(self.dataSrc, delimiter="\/", engine="python")
        self.data = df_temp.iloc[:,i]

    def getData(self):
        print(self.data)

def getChunkReqInfo():
    firstData=plotFig("C:/Users/MijanurPalash/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/CoRE_chunkRequested.txt")
    firstData.processData(-1)
    chunkList=[]
    chunkNumber=[]
    #firstData.getData()
    for i in range(len(firstData.data)):
        item=firstData.data[i]
        if item in chunkList:
            index=chunkList.index(item)
            chunkNumber[index]=chunkNumber[index]+1
        else:
            chunkList.append(item)
            chunkNumber.append(1)
    listNum=[]
    for i in range(len(chunkList)):
        listNum.append((chunkList[i],chunkNumber[i]))
        print(chunkList[i],chunkNumber[i])
    with open("chunkNum.txt","w") as new:
        new.write(str(listNum))


def main():
  getChunkReqInfo()


if __name__ == '__main__':
    main()

