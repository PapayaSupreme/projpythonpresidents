from functions import *

if __name__ == "__main__":
    directory = getcwd()
    if not path.isdir(directory + "\clean"):        # if clean folder doesn't exist, create it
        clean_files(directory)
        refine_files(directory)
    countIdf = count_idf(directory)
    files_names = pres_names(directory + "/speeches")  # raw list of speeches names
    pres_dict = {}  # list of presidents names linked with their speeches filenames
    for name in names(files_names):
        pres_dict[name] = []
    for filename in files_names:
        for name in pres_dict:
            temp = name
            for i in range(len(temp)):
                if temp[i] == " ":
                    temp = temp[i+1:]
                    break
            if temp in filename:
                pres_dict[name].append(filename)
    print("Welcome to the French Presidents' Speeches Analysis Program!")
    print("You can choose between the following options:")
    print("1. Display the names of the studied presidents")
    print("2. Display all the words used in speeches and their count")
    print("3. Display the idf score of the words used by presidents")
    print("4. Display the least important words in all speeches")
    print("5. Display the most important words in all speeches")
    print("6. Display the most used word in all speeches")
    print("7. Display the most used word in a specific speech")
    print("8. Display the speeches that contain a specific word")
    print("9. Display the first speeches to talk about a specific topic")
    print("10. Ask another question")
    print("11. Count how much a word is said")
    print("12. Exit the program")
    choice = input("Please enter the number of the option you want to choose: ")
    while choice != "12":
        if choice == "1":
            print("Sure ! Here are the names of the presidents:")
            temp = names(pres_names(directory + "/speeches"))
            for name in temp:
                print(name)
        elif choice == "2":
            print("Sure ! Here are all the words said by presidents:")
            e = count_words_total(directory)
            for i, j in e.items():
                print(i, ":", j)
        elif choice == "3":
            print("Sure ! Here are the idf of the words used by presidents:")
            for i, j in countIdf.items():
                print(i, ":", j)
        elif choice == "4":
            print("Sure ! Here are the least important words in all speeches:")
            lowest = lowest_td_idf(directory, countIdf)
            for i in lowest:
                print(i)
            print("These words are not important, meaning that their tf-idf "
                  "score is 0!")
        elif choice == "5":
            print("Sure ! Here are the most important words in all speeches:")
            highest_td_idf(directory, countIdf)
            print("These words are important because they are used in only one speech !")
        elif choice == "6":
            print("Sure ! Here are the most used words in all speeches:")
            temp = max(count_words_total(directory).values())
            for i, j in count_words_total(directory).items():
                if temp == j:
                    print(i, ":", j)
        elif choice == "7":
            print("Sure ! Here are the most used words in a specific speech:")
            print("Here are the names of the speeches:")
            for filename in listdir(directory + "\clean"):
                print(filename)
            filename = ""
            while filename not in listdir(directory + "\clean"):
                filename = input("Please enter the name of the speech you want to analyze: ")
                if filename not in listdir(directory + "\clean"):
                    print("Sorry, this is not a valid option.")
            print("Here are the most used words in the speech", filename, ":")
            temp = max(count_words(filename, directory).values())
            for i, j in count_words(filename, directory).items():
                if temp == j:
                    print(i, ":", j)
        elif choice == "8":
            print("Sure ! Here are the presidents who told a specific word:")
            word = input("Please enter the word you want to search: ")
            word = word.lower()
            print("Here are the president that told the word ", word, ":")
            temp, temp2 = [],[]
            for filename in listdir(directory + "\clean"):
                if word in count_words(filename, directory):
                    temp.append(filename)
            for i, j in pres_dict.items():
                for k in j:
                    for cell in temp:
                        if k in cell and i not in temp2:
                            temp2.append(i)
            for cell in temp2:
                print(cell)
            if not temp2:
                print("Sorry, no president told this word.")
        elif choice == "9":
            print("Sure ! Here is the first speech to talk about a specific topic:")
            word = input("Please enter the word you want to search: ")
            word = word.lower()
            print("Here is the president that talked about", word, "the first :")
            test = []
            for filename in listdir(directory + "\clean"):
                if word in count_words(filename, directory):
                    for i, j in pres_dict.items():
                        for k in j:
                            if k in filename:
                                test.append(i)
            if not test:
                print("Sorry, no president talked about this word.")
            else:
                print(test[-1])
        elif choice == "10":
            question = input("Sure ! Enter a question and i'll answer from the speeches !")
            choosefile(directory, question, countIdf)
        elif choice == "11":
            print("Sure ! Here is the number of times a word is said in all speeches:")
            word = input("Please enter the word you want to search: ")
            word = word.lower()
            print("Here is the number of times the word", word, "is said in all speeches :", end=" ")
            temp = count_words_total(directory)
            if temp[word] == 0:
                print()
                print("Sorry, no president talked about this word.")
            else:
                print(temp[word])
        else:
            print("Sorry, this is not a valid option.")
        choice = input("Please enter the number of the option you want to choose: ")


















