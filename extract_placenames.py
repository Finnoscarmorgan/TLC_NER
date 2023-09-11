"""
This program takes in a csv file and extracts and extracts LOCATION entities from a specified column
using NLTK. It then adds a new column to the csv file with the extracted entities.
"""

import pandas as pd
import re
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import conlltags2tree, tree2conlltags

# Import the csv file
df = pd.read_csv('INSERT_FILENAME_HERE')

def get_placenames(text):

    placenames = []
    tokenized_text = word_tokenize(text)
    tagged_text = pos_tag(tokenized_text)
    ne_chunked_text = ne_chunk(tagged_text)
    iob_tagged = tree2conlltags(ne_chunked_text)
    
    current_place = []  # used to collect multi-word locations

    for word, pos, ne in iob_tagged:
        if ne in ['B-GPE', 'B-LOCATION', 'B-FACILITY']:
            if current_place:  # if there's already a location being collected
                placenames.append(' '.join(current_place))
                current_place = []  # reset the current place
            current_place.append(word)
        elif ne in ['I-GPE', 'I-LOCATION', 'I-FACILITY'] and current_place:  # continues a location entity
            current_place.append(word)
        else:
            if current_place:  # if there's a location to be added
                placenames.append(' '.join(current_place))
                current_place = []  # reset the current place

    # If there's still a location left unadded at the end
    if current_place:
        placenames.append(' '.join(current_place))

    print(placenames)
    return ', '.join(placenames) 


# Apply the function to the 'para' column to create the 'placenames' column
# Change the column name from 'para' to whatever the column name is in your csv file
df['placenames'] = df['para'].apply(get_placenames)

# Export the dataframe as a csv file
df.to_csv('INSERT_FILENAME_HERE', index=False)
