import utilities
import pandas as pd

print("Start 5.15")
utilities.concatinate_files(csv1='models/mainFile', csv2='models/songData_5.15')

temp = pd.read_csv('models/mainFile').dropna()
print(temp.shape)
print("Done")

print("Start 5.3")
utilities.concatinate_files(csv1='models/mainFile', csv2='models/songData_5.3')

temp = pd.read_csv('models/mainFile').dropna()
print(temp.shape)
print("Done")

print("Start 5.45")
utilities.concatinate_files(csv1='models/mainFile', csv2='models/songData_5.45')

temp = pd.read_csv('models/mainFile').dropna()
print(temp.shape)
print("Done")