import os
from PIL import Image
from Image_Manipulation import Operation, operation_identities
from Utils import title, request_index

# Defines a list of operations to be run sequentially on each picture
sequence = []

def run_sequence(input_dir, output_dir):
    '''Modifies the images'''
    # Uses the utility title function for a decorative mode indicator
    title("Run Sequence")
    # Iterates through all the files in the selected directory and checks if they are images
    for file in os.listdir(input_dir):
        if file[-4:].lower() in ['.jpg', '.png']:
            # Create variables for saving and loading
            in_file_path = os.path.join(input_dir, file)
            file_path = os.path.join(output_dir, file)
            # Prints the name of the current image
            print(file)
            # Loads the image
            with Image.open(in_file_path) as img:
                img.load()
            # Runs the sequence
            for operation in sequence:
                if operation.save:
                    img.save(os.path.join(output_dir ,operation.save_prefix + file))
                img = operation.function(img)
            # Saves the new image
            img.save(file_path)

# THIS FUNCTION IS THE VISUALIZATION OF DATA.
def run_preview_sequence(input_dir):
    '''Shows the user what the sequence will do'''
    # Uses the utility title function for a decorative mode indicator
    title("Run preview Sequence")
    # Iterates through all the files, and runs the sequence on the first image 
    for file in os.listdir(input_dir):
        if file[-4:].lower() in ['.jpg', '.png']:
            # Prints the current file name
            print(file)
            # Load the image
            with Image.open(os.path.join(input_dir, file)) as img:
                img.load()
            # Run the Sequence
            for operation in sequence:
                img = operation.function(img)
            # Shows the image
            img.show()
            # Returns
            return

def show_sequence():
    '''Displays the sequence to the user'''
    # Uses the utility title function for a decorative mode indicator
    title("Show Sequence")
    # Prints every operation in the sequence
    for operation in sequence:
        print(operation.to_string())

def create_operation():
    '''Creates an operation'''
    # Uses the utility title function for a decorative mode indicator
    title("Create Operation")
    # Gets the index of the operation the user wants to create
    choice = request_index(operation_identities) 
    # Exit the function if the user chose cancel
    if choice == None:
        return
    # Creates a list of parameters to use when creating the operation
    params = []
    # Iterates through every parameter for the operation and requests a value
    for param in operation_identities[choice]["Params"]:
        params.append(input(f"{param}: "))
    # Creates the user specified operation and returns it
    return Operation(choice, params)
    
def delete_operation():
    '''Removes an element from the sequence'''    
    # Uses the utility title function for a decorative mode indicator
    title("Delete Operation")
    # Notifies the user if there is nothing in the sequence to remove
    if len(sequence) == 0:
        print(f"Empty")
        return
    # Asks the user for the index of the operation to remove from the sequence
    choice = request_index(sequence)
    # Exit the function if the user chose cancel
    if choice == None:
        return
    # Removes the item at the user specified index
    sequence.pop(choice)

def replace_operation():
    '''Swaps an operation in the sequence for a new one'''
    # Uses the utility title function for a decorative mode indicator
    title("Replace Operation")
    # Notifies the user if there is nothing in the sequence to remove
    if len(sequence) == 0:
        print(f"Empty")
        return
    # Asks the user for the index of the operation to replace
    choice = request_index(sequence)
    # Exit the function if the user chose cancel
    if choice == None:
        return
    # Creates a new function to use in the sequence
    new = create_operation()
    # Exit the function if the user chose cancel
    if new == None:
        return
    # Swaps the old function for the new one
    sequence.pop(choice)
    sequence.insert(choice, new)

def modity_sequence():
    '''Provides a user interface for modifying the sequence'''
    # Uses the utility title function for a decorative mode indicator
    title("Modify Sequence")
    # Shows the user available options
    print("1: Show Sequence")
    print("2: Delete Operation")
    print("3: Replace Operation")
    print("4: Append Operation")
    print("5: Insert Operation")
    print("6: Cancel")
    print()
    # Takes the user input, and performs the corresponding action
    choice = input("Choice: ")
    match choice:
        case '1':
            show_sequence()
        case '2':
            delete_operation()
        case '3':
            replace_operation()
        case '4':
            new = create_operation()
            if new != None:
                sequence.append(new)
        case '5':
            new = create_operation()
            if new != None:
                sequence.insert(0, new)
        case '6':
            return
        case _:
            print("Invalid Choice")
    # If the user did not cancel, request user input again
    modity_sequence()

def file_browser(dir):
    '''Gives the user the ability to chose a directory'''
    # Uses the utility title function for a decorative mode indicator
    title("File Browser")
    while True:
        # Shows the directory the user is currently in
        print("Current Directory")
        print(dir)
        print("\n")

        # Saves a list of everything in the directory and filters for folders
        items = os.listdir(dir)
        directories = [item for item in items if os.path.isdir(os.path.join(dir, item))]

        # Adds an option to backtrack
        directories.append("..")
        
        # Asks the user for the index of the directory to enter
        choice = request_index(directories)

        # Exit the function if the user chose cancel
        if choice == None:
            return dir

        # Changes the directory to the one the user specified
        dir = os.path.join(dir, directories[choice])

# Set the default input and output directory to the current folder
input_dir = os.getcwd()
output_dir = os.getcwd()

# Core program loop
while True:
    # Uses the utility title function for a decorative mode indicator
    title("Choose Operation")
    # Shows the user available options
    print(f"Input Directory: {input_dir}")
    print(f"Output Directory: {output_dir}")
    print("1: Show sequence")
    print("2: Modify Sequence")
    print("3: Run Sequence")
    print("4: Preview Run Sequence")
    print("5: Change Input Directory")
    print("6: Change Output Directory")
    print("7: Quit")
    print()
    # Takes the user input, and performs the corresponding action
    choice = input("Choice: ")
    match choice:
        case '1':
            show_sequence()
        case '2':
            modity_sequence()
        case '3':
            run_sequence(input_dir, output_dir)
        case '4':
            run_preview_sequence(input_dir)
        case '5':
            input_dir = file_browser(input_dir)
        case '6':
            output_dir = file_browser(output_dir)
        case '7':
            exit()
        case _:
            print("Invalid Choice")

