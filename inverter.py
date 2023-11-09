# To invert given string

def invert(input_string):
    """
    To invert the given string
    Keyword arguments:
    -----------------
    input_string : string format.
    Returns:
    --------
    inverted_string : string format.
        Returns "" if given string is None else it will return the reverse string 
    """
    inverted_string = ""   
    if input_string:
       inverted_string = input_string[::-1]
    return inverted_string

# print("Inverted String :-  invert('Jenkins using Python Script')")
print('Given String    :-  Jenkins using Python Script \nInverted String :- ' , invert('Jenkins using Python Script'))