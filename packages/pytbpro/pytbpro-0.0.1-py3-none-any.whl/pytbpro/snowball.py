import pandas as pd
import matplotlib.pyplot as plt

def display(data_date:list, data_price:list, idx:int):
    k_out = data_price[0] * 1.05
    k_in = data_price[0] * 0.7
    x = data_date[:idx + 1]
    plt.plot(x, data_price[:idx + 1], '-', color='r', label = 'price')
    plt.plot(x, [k_out for i in range(0, idx + 1)], '-', color='blue', label = 'knock out')
    plt.plot(x, [k_in for i in range(0, idx + 1)], '-', color='black', label = 'knock in')
    plt.xticks(rotation=45)
    plt.xlabel('date')
    plt.ylabel('price')
    plt.legend()
    plt.show()

def readFile(fileName:str):
    fileType = fileName.split('.')[-1]
    if fileType == 'xls':
        data = pd.read_excel(fileName).iloc[:, :].values.tolist()
    elif fileType == 'csv':
        data = pd.read_csv(fileName).iloc[:, :].values.tolist()
    else:
        raise
    return data

def hasKnockOut(data_date:list, data_price:list):
    k_out = data_price[0] * 1.05
    idx = 0
    while idx < len(data_date):
        if data_price[idx] >= k_out and (idx == len(data_date) - 1 or (data_date[idx].month < data_date[idx + 1].month or data_date[idx].year < data_date[idx + 1].year)):
            return True, idx
        idx += 1
    # idx == len(data_date)
    return False, idx - 1

def cal(fileName:str, showPic = True):
    try:
        data = readFile(fileName)
    except:
        print('File Error!\nPlease save file as .xls or .csv')
        return

    data_date = [d[0].date() for d in data]
    data_price = [d[1] for d in data]

    hko, show_idx = hasKnockOut(data_date, data_price)
    if hko or min(data_price) >= data_price[0] * 0.7: # +15%
        if showPic:
            display(data_date, data_price, show_idx)
        return data_price[0] * 1.15
    elif data_price[-1] >= data_price[0]:
        if showPic:
            display(data_date, data_price, show_idx)
        return 0.0
    else:
        if showPic:
            display(data_date, data_price, show_idx)
        return data_price[0] - data_price[-1]



