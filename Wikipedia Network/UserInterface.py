## Simple terminal user interface
## The user inputs a string of fundamental steps for a process
## and the program finds similar articles in Wikipedia. These
## articles are then suggested to the user.

from HTML_2_Corpus import textractor
from wikiScript import find_similar

def menu():
    """Displays a menu to the user."""
    print('         MENU          ')
    print('-----------------------')
    print('-- 1. Manual Input   --')
    print('-- 2. Upload a file  --')
    print('-- 3. Use example    --')
    print('-- 4. Exit           --')
    print('-----------------------')
    choice = input()
    while choice not in ['1','2','3','4']:
        print('Invalid input.\nPlease enter a valid choice.')
        choice = input()
    if choice == '1':
        print('Please enter the fundamental steps and attributes '
              'of your process.'
              )
        print('For example, if you are building a chair, you could '
              'enter the following:\n'
              '"sit ergonomic comfortable natural productive energy"'
              )
        fundamentals = input()
        return fundamentals
    if choice == '2':
        file_name = input('Please enter the name of the file: ')
        texts = textractor(file_name)
        target = input('Which document would you like to process?'
                           '\nEnter the order in your document.'
                           '\nIf there is only one, enter "1".\n'
                           )
        while target not in range(len(texts)):
            target = input('Invalid input. Please enter a valid index.\n')
        return texts[target-1]
    if choice == '3':
        # Example query 
        coreString = ('optimization consumer input preferences filtering '
                      'evolutionary stopping criterion selection customized '
                      'aesthetics usability adaptation'
                      )
        return coreString
    

query = menu()
print(query)

# This will return a list. Right now it only returns the closest
#indeces = find_similar(query)

# Further work --> link the indeces with the titles of documents.
# Display the document titles.
# After we get that working, use Jason's program to display the
# title and short explanation of each.
# We can modify wikiScript.find_similar to have a parameter that
# lets you choose how many similar documents you want returned.


