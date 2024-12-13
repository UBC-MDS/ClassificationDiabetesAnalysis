import os
import zipfile
import shutil

# Create a directory named 'subdir'
os.makedirs('subdir', exist_ok=True)

# Create 'test1.txt' and write "test data" to it
with open('test1.txt', 'w') as file:
    file.write('test data')

# Create 'test2.csv' and write "test data" to it
with open('test2.csv', 'w') as file:
    file.write('test,data')

# Create 'test3.txt' inside 'subdir' and write "test data" to it
with open('subdir/test3.txt', 'w') as file:
    file.write('test data')

# Case 1 - Create a zip file containing 'test1.txt' and 'test2.csv'
with zipfile.ZipFile('files_txt_csv.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('test1.txt')
    zipf.write('test2.csv')

# Case 2 - Create a zip file containing 'test1.txt', test2.csv and 'subdir/test2.txt'
with zipfile.ZipFile('files_txt_subdir.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('test1.txt')
    zipf.write('test2.csv')
    zipf.write('subdir/test3.txt')

# Case 3 - Create an empty zip file
with zipfile.ZipFile('empty.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    pass

# Clean up the files and directories created
test_files = ['test1.txt', 'test2.csv']
for file in test_files:
    if os.path.exists(file):
        os.remove(file)
if os.path.exists("subdir"):
    shutil.rmtree("subdir")
