# Importing libraries

from os import listdir, path, mkdir, remove, getcwd
from math import log


# Functions
def pres_names(directory):
    """Returns a list of the non duplicated names of text files.
    Parameters:
        directory (str): the directory where the text files are stored
    Returns:
        files_names (list): a list of the non duplicated names of text files.
    """
    files_names = []
    for filename in listdir(directory):
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
        elif "2" in names[-1]:
            names.pop(-1)
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
    if not path.isdir(directory + "\clean"):
        mkdir(directory + "\clean")
    for filename in listdir(directory + "\speeches"):
        f = open(directory + "\speeches" + "\\" + filename, "r", encoding="utf-8")
        fw = open(directory + "\clean" + "\\" + filename, "w", encoding="utf-8")
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
    for filename in listdir(directory + "\clean"):
        f = open(directory + "\clean" + "\\" + filename, "r", encoding = "utf-8")
        f2 = open(directory + "\clean" + "\\" + "refined" + filename, "w", encoding = "utf-8")
        for line in f:
            for letter in line:
                if (letter == "à" or letter == "â" or letter == "ç" or letter == "é" or letter == "è" or
                        letter == "ê" or letter == "ë" or letter == "î" or letter == "ï" or letter == "ô" or
                        letter == "ö" or letter == "ù" or letter == "û" or letter == "ü" or letter == "œ"):
                    f2.write(letter)
                elif letter == "'" or letter == "’" or letter == "-" or letter == ".":
                    f2.write(" ")
                elif 97 <= ord(letter) <= 122 or ord(letter) == 32 or 48 <= ord(letter) <= 57:
                    f2.write(letter)
        f.close()
        f2.close()      #close the files
        remove(directory + "\clean" + "\\" + filename)


def count_words(filename, directory):
    """Counts in a dictionary the number of occurrences of every word in the file (tf).
    Parameters:
        directory (str): the directory where the text file is stored
        filename (str): the name of the file
    Returns:
        wordCount (dict): dictionary with the number of occurrences of every word in the file"""
    wordCount = {}
    f = open(directory + "\clean" + "\\" + filename, "r", encoding="utf-8")
    for line in f:
        for word in line.split():
            if word in wordCount:
                wordCount[word] += 1
            else:
                wordCount[word] = 1
    f.close()
    return wordCount


def count_words_total(directory):
    """Counts in a dictionary the number of words in all the files (tf).
        Parameters:
            directory (str): the directory where the text file folder "clean" is stored
        Returns:
            totWordCount (dict): number of occurrences of every word of each file"""
    files_names = []
    for filename in listdir(directory + "\clean"):
        files_names.append(filename)
    totWordCount = {}
    for filename in files_names:
        wordCount = count_words(filename, directory)
        for word in wordCount:
            if word in totWordCount:
                totWordCount[word] += wordCount[word]
            else:
                totWordCount[word] = wordCount[word]
    return totWordCount


def count_idf(directory):
    """Calculates the logarithm of the inverse of the number of speeches in which the words have been used.
        Parameters:
            directory (str): the directory where the programs and the text file folder "clean" is stored
        Returns:
            idfTotWordCount (dict): log of the inverse of the number of each word in each file"""
    idfTotWordCount = count_words_total(directory)
    occ = {}
    files_names = []
    for filename in listdir(directory + "\clean"):
        files_names.append(filename)
    for word in idfTotWordCount:
        for filename in files_names:
            if word in count_words(filename, directory):
                if word in occ:
                    occ[word] += 1
                else:
                    occ[word] = 1
        idfTotWordCount[word] = log(len(files_names)/occ[word])
    return idfTotWordCount


def highest_td_idf(directory, countIdf):
    """Indicates the words with the highest td_idf score.
        Parameters:
            directory (str): the directory where the text files are stored
        Returns:
            None"""
    files_names, highest = [], []
    for filename in listdir(directory + "\clean"):
        files_names.append(filename)
    for filename in files_names:
        tdIdf = td_idf(directory, countIdf, filename)
        temp = max(tdIdf.values())
        for i, j in tdIdf.items():
            if temp == j and i not in highest:
                highest.append(i)
    for i in highest:
        print(i)

def lowest_td_idf(directory, countIdf):
    """Indicates the words with the lowest td_idf score.
        Parameters:
            directory (str): the directory where the text files are stored
        Returns:
            None"""
    files_names, lowest = [], []
    for filename in listdir(directory + "\clean"):
        files_names.append(filename)
    for filename in files_names:
        tdIdf = td_idf(directory, countIdf, filename)
        for i, j in tdIdf.items():
            if j == 0.0 and i not in lowest:
                lowest.append(i)
    for i in lowest:
        print(i)


def td_idf(directory, countIdf, filename):
    """Calculates the tf-idf score of each word in a file.
        Parameters:
            directory (str): the directory where the text files are stored
            countIdf (dict): log of the inverse of the number of each word in each file
            filename (str): the name of the file
        Returns:
            tdIdf (dict): the td-idf score of each word in the file"""
    tdIdf = {}
    wordCount = count_words(filename, directory)
    for word in wordCount:
        tdIdf[word] = wordCount[word] * countIdf[word]
    return tdIdf

"""def td_idf_matrix(directory):
    Creates a matrix with as many columns as files and as many rows as unique words,
        containing the tf-idf score of each word in each file.
        Parameters:
            directory (str): the directory where the text files are stored
        Returns:
            td_idf_matrix (list): the tf-idf score of each word in each file
    totWordCount = count_words_total(directory)
    tdIdfMatrix = [[0]] * len(totWordCount)
    files_names = []
    for filename in listdir(directory + "\clean"):
        files_names.append(filename)
    n = len(files_names)
    i = 0
    for key in totWordCount.keys():
        tdIdfMatrix[i].append(key)
        i+=1
    return tdIdfMatri"""










#modifier pres names pour qu'elle renvoie tous les noms et que names() se charge d'enlever les doublons
#optimiser count_idf() c'est elle le probleme