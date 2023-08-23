import os

files_list = list()
output = r"c:\users\sharad\pyora\csv_files\output.txt"
for (dirpath, dirnames, filenames) in os.walk(r'c:\users\sharad\pyora\csv_files'):
    files_list += [os.path.join(dirpath, file) for file in filenames]

for file in files_list:
    fin = open(file, "rt")
    data = fin.read()
    fin.close()
    fin = open(output, "a+")
    fin.write(data)
#    fin.write("\n ---------- \n")
    fin.close()