# -*- coding: utf-8 -*-

import csv
import os

def rename():
    with open('result.csv', encoding='utf-8') as f:
        fileList = os.listdir()
        reader = csv.reader(f)

        for row in reader:
            if row[0] in fileList:    
                try:
                    print(row)
                    os.rename(row[0], row[1]+row[2]+".pdf")
                except IOError as error:
                    print("error = ", error)


if __name__ == "__main__":
    rename()