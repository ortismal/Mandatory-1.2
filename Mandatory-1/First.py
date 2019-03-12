import sys
import os
import subprocess
from urllib.request import Request, urlopen
import urllib.response
import glob

# To start with, we will indicate where we will collect our data from, save it in a variable, and make sure we can read it
url = ('https://api.github.com/orgs/python-elective-2-spring-2019/repos?per_page=100')
res = urlopen(url)
html = res.read().decode('utf-8')

# Here we split the string up by the ',' token - we will need that later.
lines = html.split(',')

# We want to place all cloned repositorys in the same folder, so if the folder does not exist, we create a new one.
if not os.path.exists('clones'):
    os.mkdir('clones')
os.chdir('clones')

# If a repository does not exist, clone it from git.
# DOES NOT WORK
currentUrls = []

for folder_name in lines:
    if 'clone_url' in folder_name:
        clone_url = folder_name[13:-1]
        folder_name = folder_name[62:-5]
        if not os.path.exists(folder_name):
                currentUrls.append(clone_url)
                subprocess.run(['git', 'clone', clone_url])


# Pull method that checks, if the folder exists, and pulls instead of clones
for folder_name in lines:
    if 'name' in folder_name:
        folder_name = folder_name[8:-1]
    if os.path.exists(folder_name):
        os.chdir(folder_name)
        subprocess.run(['git', 'pull', 'origin', 'master'])
        os.chdir('..')
        # When a loop is completed, go one dir up and repeat


# This function loops through the path given in the glob module
readmeFiles = []
for readme in glob.glob('C:/Users/Callo/OneDrive/Skrivebord/GitHub/4.Semester/Python/Casper/Mandatory-1/clones/*/readme.md'):

    # read the readme file and save it in a variable readmeContent
    readmeContend = open(readme).read()
    # first delimiter, starting at 'required reading'
    start = readmeContend.find('## Required reading')
    # last delimiter, starting at 'supplementary reading
    end = readmeContend.find('### Supplementary reading')

    if start == -1:  # an if-statement, saying that if the readme file does not contain the first delimiter, skip the file
        continue

    # save the content of the required reading using delimiters
    requiredReading = readmeContend[start+19:end]

    # place the content of the required reading in the readmeFiles list
    readmeFiles.append(requiredReading)


os.chdir('..')  # go one dir up

# if the curriculum dir does not exist, create the folder
if not os.path.exists('curriculum'):
    os.mkdir('curriculum')
os.chdir('curriculum')

# Now we will trim and format the readme outputs, so it looks readable in the required_reading file
output_list = []
# Put 'required reading' in the top of the file
output_list.append("## Required reading:")
for long_string in readmeFiles:
    for single_line in long_string.split("*"):
        single_line = '*' + single_line[0:].strip()

        if single_line in output_list:
            print(single_line + '     :Exists!')
            continue

        if len(single_line) < 5:
            continue

        # Tries to capitalize the first letter
        # DOES NOT WORK
        for i, c in enumerate(single_line):
            if not c.isdigit():
                break
        single_line[:i] + single_line[i:].capitalize()

        output_list.append(single_line)

file = open('Required_reading.md', 'w')
large_string = "\n".join(sorted(output_list))
file.write(large_string)
file.close()

os.chdir('..')
pushChoice = input('\nWould you like to push to git? write "Y" to push: ')

if pushChoice == 'Y':
    comment = input('\nComment your push: ')
    subprocess.run(['git', 'remote','add', 'origin', 'https://github.com/ortismal/Mandatory-1.2.git'])
    subprocess.run(['git', 'add', '*'])
    subprocess.run(['git', 'commit', '-am', comment])
    subprocess.run(['git', 'push', 'origin', 'master'])
    
else:
    pass

print('\nThank you for downloading or updating the required reading curriculum. See you again next time!')
