from functions import *

if __name__ == "__main__":
    directory = os.getcwd()
    directorysp = directory + "/speeches"
    files_names = pres_names(directorysp,"2.txt")     #raw list of speeches names
    names = names(files_names)                #list of presidents names
    #print(pres_names(directorysp,"2.txt"))
    #print(names)
    #clean_files(directory)
    #refine_files(directory)
    #print(count_words("refinedNomination_Giscard dEstaing.txt", directory))
    print(count_words_total(directory))
