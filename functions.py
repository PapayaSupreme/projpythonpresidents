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
    """This function associates all the president's first names with their last names.
     Parameters:
         files_names (list): The list of the non_duplicated files.
    Returns:
        names (list): The new list of the non-duplicated files with the last and first names of the presidents."""
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
        directory (str): The directory where the text files are stored.
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
    files_names = []
    for filename in listdir(directory + "\clean"):
        files_names.append(filename)
    idfTotWordCount = {}
    for filename in files_names:
        wordCount = count_words(filename, directory)
        #print(wordCount)
        for word in wordCount:
            if word in idfTotWordCount:
                idfTotWordCount[word] += 1
            else:
                idfTotWordCount[word] = 1
    #print(idfTotWordCount)
    for word in idfTotWordCount:
        temp = idfTotWordCount[word]
        idfTotWordCount[word] = log(8 / temp, 10)
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


def td_idf_matrix(directory, countIdf):
    """Creates a matrix with as many columns as files and as many rows as unique words,
        containing the tf-idf score of each word in each file.
        Parameters:
            directory (str): the directory where the text files are stored
        Returns:
            td_idf_matrix (list): the tf-idf score of each word in each file"""

    tdIdfMatrix = [[0.0]*8] * 1685      #works
    files_names,words = [],[]
    tdidf = [0]*8
    temp = []
    for filename in listdir(directory + "\clean"):
        files_names.append(filename)        #['refinedNomination_Chirac1.txt', 'refinedNomination_Chirac2.txt',
    for i in range(8):
        tdidf[i] = (td_idf(directory, countIdf, files_names[i]))   #8 dict ina list for each tdidf
        words.append(count_words(files_names[i], directory))        #8 dict ina list for each wordcount
    for e in tdidf:
        print(e)
    listepitie = count_words_total(directory)              #dict of total wordcount
    #print(tdidf[2])
    #print("TDIDF")
    #print(listepitie["messieurs"], "LISTEPITIE")
    #print(len(listepitie), "LEN LISTEPITIE")
    #print("messieurs" in words[0], "VERIF")
    #print(tdidf[2]["messieurs"], "TDIDF AHHH")
    k =0        #going 0-1684
    for j in listepitie:       #going through the whole corpus of words
        for i in range(8):  #nb of speeches
            #print("i=", i)
            #print("j = ", j)
            #print(j in words[i])
            if j in words[i]:   #if the word is in the speech
                tdIdfMatrix[k][i] = round(tdidf[i][j],2)
                #print(round(tdidf[i][j],2), "tdidf[i][j]")
        #print(tdIdfMatrix[k-1],"tdIdfMatrix[k], i & k= ", i, k)
        print(tdIdfMatrix[k],"tdIdfMatrix[k], i & k= ", k)       #[0.25, 1.81, 0.3, 0.3, 0.3, 0.9, 0.3, 0.2] tdIdfMatrix[k], i & k=  7 489
        temp.append(tdIdfMatrix[k])
        k += 1
    return temp

def tokenQuestion(question):
    """Transforms the question into a list of words.
        Parameters:
            question (str): the question asked by the user
        Returns:
            question (list): the question asked by the user"""
    question = question.lower()
    question = question.replace("?", "")
    question = question.replace("!", "")
    question = question.replace(".", "")
    question = question.replace(",", "")
    question = question.replace("'", " ")
    question = question.replace("-", " ")
    question = question.replace("’", " ")
    question = question.split()
    return question

def wordinQ(directory,question):
    """Returns the words that are in the question and in the corpus.
        Parameters:
            directory (str): the directory where the text files are stored
            question (list): the question asked by the user
        Returns:
            commun (list): the words that are in the question and in the corpus"""
    words = count_words_total(directory)
    commun = []
    Tquestion = tokenQuestion(question)
    for cell in Tquestion:
        if cell in words:
            commun.append(cell)
    return commun

def tfidfQuestion(question, countIdf):
    question = tokenQuestion(question)
    tfQ = {}
    for cell in question:
        if cell in tfQ:
            tfQ[cell] += 1
        else:
            tfQ[cell] = 1

    for cell in tfQ:
        if cell in countIdf:
            tfQ[cell] = tfQ[cell]/len(question) * countIdf[cell]
        else:
            tfQ[cell] = 0
    return tfQ

def similarity(directory, question, countIdf):
    """Calculates the cosine similarity between the question and each speech.
        Parameters:
            directory (str): the directory where the text files are stored
            question (list): the question asked by the user
            countIdf (dict): log of the inverse of the number of each word in each file
        Returns:
            similarity (list): the cosine similarity between the question and each speech"""
    tfidfQ= tfidfQuestion(question, countIdf)
    tdidfC=[0]*8
    files_names = []
    for filename in listdir(directory + "\clean"):
        files_names.append(filename)
    for i in range(8):
        tdidfC[i] = (td_idf(directory, countIdf, files_names[i]))
    """for e in tdidfC:
        print(e)"""
    matrix =
    similarity = {}
    for i in range(8):
        similarity[files_names[i]] = cosine_similarity
    return similarity

def scalar_product(vectorA,vectorB):
    """Returns the scalar product of the two vectors.
        Parameters:
            vectorA, vectorB (list): the two vectors
        Returns:
            scalar (float): the scalar product of the two vectors"""
    scalar = 0
    for i in range(len(vectorA)):
        scalar += vectorA[i]*vectorB[i]
    return scalar

def norm(vector):
    """Returns the norm of the vector.
        Parameters:
            vector (list): the vector
        Returns:
            norm (float): the norm of the vector"""
    norm = 0
    for i in range(len(vector)):
        norm += vector[i]**2
    return norm**(1/2)

def cosine_similarity(vectorA, vectorB):
    """Returns the cosine similarity between the two vectors.
        Parameters:
            vectorA, vectorB (list): the two vectors
        Returns:
            cosine (float): the cosine similarity between the two vectors"""
    cosine = scalar_product(vectorA,vectorB)/(norm(vectorA)*norm(vectorB))
    return cosine
