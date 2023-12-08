from Image_Manipulation import Operation


def title(string: str):
    ''' Provides a consistent way of displaying the title of a mode'''
    print(f"\n~~~~~~~~~~ {string} ~~~~~~~~~~\n")

def request_index(target_set):
    '''Gives the user the chance to choose which item out of a list of items'''
    index = 0
    for item in target_set:
        if type(item) == dict:
            print(str(index) + ": " + item["Name"])
        elif type(item) == Operation:
            print(str(index) + ": " + item.to_string())
        elif type(item) == str:
            print(str(index) + ": " + item)
        index += 1
    print(f"{index}: Cancel\n")
    choice = -1
    while choice < 0 or choice >= target_set.__len__() + 1:
        try:
            choice = int(input("Choice: "))
            if choice < 0 or choice >= target_set.__len__():
                print("Invalid index")
        except:
            print("Choice must be a number")
            choice = -2
    return None if choice == len(target_set) else choice
