import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import xlsxwriter

## Next Steps: Run the whole process through with Lila's model

def hehe(percent_editing,constants,be2):
    # Main model, Takes an array as input and returns the concentrations
    arb_conc = []
    for x in range(0,len(percent_editing)):
        sum = 0
        if percent_editing[0] == 0:
            # No input signal (pH promoter)
            for y in range(0,len(percent_editing)):
                
                arb_conc.append(0)
            
            break
        sum = (percent_editing[0]) + (percent_editing[x])
        avg = sum/float(len(percent_editing))
        niPE = percent_editing[0] /constants[0]
        temp1 = (percent_editing[x]*sum) / niPE / float(constants[x]) #Normalize for competition
        temp = (temp1/niPE) # Normalize for time
        if percent_editing[x] == 0:
            temp = 0
        arb_conc.append(temp)
    arb_conc.pop(0)
    return arb_conc



if __name__ == '__main__':

    constants = [1,2,1,1]
    editing_constants = [1,1,1,1]

    total_editing = [[1,1,1,1],[5,5,5,5],[5,1,1,1],[10,1,1,1],[5,5,1,1],[5,0,0,5]]
    
    #[[8,0.5,0.5],[29,0,0],[2,1,1],[4,0,1],[12,5,0],[18,0,11.5],[0,8,11],[8.5,4,12],[10,5,5],[10,10,10],[5,0,10],[5,10,10],[10,20,20],[20,10,10],[5,5,5]]

    harr = []
    labels = []
    xlabels = []
    arr = []

    for x in range(0,len(total_editing)):
        harr.append(hehe(total_editing[x],constants,editing_constants))

    pdarray = []
    pdarray1 = []

    for y in range(0,len(total_editing[0])):
        temp = []
        for x in total_editing:
            temp.append(x[y])
        pdarray.append(temp)
    
    for y in range(0,len(harr[0])):
        temp = []
        for x in harr:
            temp.append(x[y])
        pdarray1.append(temp)

    # Create Graph

    for x in range(0,len(harr[0])):
        temp = []
        for y in range(0,len(harr)):
            temp.append(harr[y][x])
        arr.append(temp)

    for x in range(0,len(total_editing)):
        labels.append("Mb " + str(x+2))

    for x in range(0,len(arr[0])):
        xlabels.append("Cond. " + str((x+1)))

    # Export to Excel

    df = pd.DataFrame({'Metabolite 1':pdarray[0],'Metabolite 2':pdarray[1],'Metabolite 3':pdarray[2],'Metabolite 4':pdarray[3]},[pd.Index(xlabels)])
    df1 = pd.DataFrame({'Metabolite 2':pdarray1[0],'Metabolite 3':pdarray1[1],'Metabolite 4':pdarray1[2]},[pd.Index(xlabels)])
    
    print(df)
    print(df1)
    
    #print(arr)

    # set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))

    temp1 = np.arange(len(arr[0]))

    brarr = [temp1]

    for x in range(1,len(arr[0])):
        temp2 = [y + barWidth for y in brarr[x-1]]
        brarr.append(temp2)

    colorarr = ['r', 'g', 'b']

    print(arr[0])
    
    for x in range(0,len(arr)):
        plt.bar(brarr[x], arr[x], color =colorarr[x], width = barWidth,
            edgecolor ='grey', label =labels[x])
    
    # Adding Xticks
    plt.xlabel('Conditions', fontweight ='bold', fontsize = 15)
    plt.ylabel('Relative Values', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(arr[0]))],
            xlabels)
    
    plt.legend()
    plt.show()