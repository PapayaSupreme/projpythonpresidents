# Importing libraries

import os

# Functions
def pres_names(directory, extension):
    """Returns a list of the non duplicated names of text files.
    Parameters:
        directory (str): the directory where the text files are stored
        extension (str): the extension of the text files and the number to exclude.
    Returns:
        files_names (list): a list of the non duplicated names of text files.
    """
    files_names = []
    for filename in os.listdir(directory):
        if not filename.endswith(extension):
            files_names.append(filename)
    return files_names

def names(files_names):
    """Associates the president's last names to the first names.
     Parameters:
         files_names (list): a list of the non duplicated names of text files.
    Returns:
        names (list): a new list of the non duplicated names with the first names."""
    names = []
    for name in files_names:
        names.append(name[11:-4])
        if "1" in names[-1]:
            names[-1] = names[-1][:-1]
    for i in range(len(names)):
        if "Chirac" in names[i]:
            names[i] = "Jacques " + names[i]
        if "Giscard dEstaing" in names[i]:
            names[i] = "Valéry " + names[i]
        if "Hollande" in names[i]:
            names[i] = "François " + names[i]
        if "Macron" in names[i]:
            names[i] = "Emmanuel " + names[i]
        if "Mitterrand" in names[i]:
            names[i] = "François " + names[i]
        if "Sarkozy" in names[i]:
            names[i] = "Nicolas " + names[i]
    return names


def clean_files(directory):
    """Opens a folder, opens each file of the folder, and substitutes all the capital letters with lower case letters.
    Parameters:
        directory (str): the directory where the text files are stored
    Returns:
        None"""
    if not os.path.isdir(directory + "\clean"):
        os.mkdir(directory + "\clean")
    for filename in os.listdir(directory + "\speeches"):
        f = open(directory + "\speeches" + "\\" + filename, "r")
        fw = open(directory + "\clean" + "\\" + filename, "w")
        for line in f:
            for letter in line:
                if 65 <= ord(letter) <= 90:
                    fw.write(chr(ord(letter) + 32))
                else:
                    fw.write(letter)
    f.close()
    fw.close()


def refine_files(directory):
    """Removes all the characters that contains accents in clean files.
    Parameters:
        directory (str): the directory where the text files are stored
    Returns:
        None"""
    for filename in os.listdir(directory + "\clean"):
        f = open(directory + "\clean" + "\\" + filename, "r")
        f2 = open(directory + "\clean" + "\\" + "refined" + filename, "w")
        for line in f:
            for letter in line:
                if ord(letter) == 339 or ord(letter) == 338:                    #oeOE
                    f2.write("oe")
                elif 192<= ord(letter) <= 197 or 224 <= ord(letter) <= 229:     #Aa
                    f2.write("a")
                elif ord(letter) == 199 or ord(letter) == 231:                  #Cc
                    f2.write("c")
                elif 200<=ord(letter) <= 203 or 232 <= ord(letter) <= 235:      #Ee
                    f2.write("e")
                elif 204<=ord(letter) <= 207 or 236 <= ord(letter) <= 239:      #Ii
                    f2.write("i")
                elif 210<=ord(letter) <= 214 or 242 <= ord(letter) <= 246:      #Oo
                    f2.write("o")
                elif 217<=ord(letter) <= 220 or 249 <= ord(letter) <= 252:      #Uu
                    f2.write("u")
                if letter == "'" or letter == "’" or letter == "-" or letter == ".":
                    f2.write(" ")
                elif 97 <= ord(letter) <= 122 or ord(letter) == 32 or 48 <= ord(letter) <= 57:
                    f2.write(letter)
    f.close()
    f2.close()
