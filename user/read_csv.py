import csv, os

f_csv = open(os.getcwd()+"\\songdir\\tmp\\1.csv")
read = f_csv.read()
new  = read.split("\n")[1].split(",")
print(new)