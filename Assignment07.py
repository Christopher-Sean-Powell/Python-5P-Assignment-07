__author__ = 'Chris'

# Christopher Powell

# cspowell@ucsc.edu

# Assignment07: Document Similarity


import sys

import math


# I got most of this next function from lecture on 5-15, and was also used in assignment 6.
def sorted_keys_by_value (d):
    ''' This function takes a dictionary as an input, and then orders that dictionary based on the values of each key.
    This reordered list is returned as a list of tuples.'''
    counts = []
    for k in d.keys():
        counts.append ((d[k], k))
    counts.sort()
    counts.reverse()
    sorted_keys = []
    for item in counts:
        sorted_keys.append ((item[1], item[0]))
    return sorted_keys


# I got this function from class on 5-20. I also got some help on the function from Professor Miller through Piazza.
def no_punct(s):
    '''Removes all punctuation from a given string. It is formatted to work for a text entry with more than one line
    of text.'''
    l = []
    for the_line in s:
        the_line = the_line.lower()
        words = the_line.split()
        for word in words:
            l.append(" ")
            for ltr in word:
                if "a" <= ltr <= "z":
                    l.append(ltr)
                elif ltr == " ":
                    l.append(ltr)
                elif ltr == "-":
                    l.append(" ")
            else:
                    l.append(" ")
    new_s = ''.join(l)
    return new_s


# I reused this function from assignment 06. It was originally given (partially) in class on 5-15.
def count_words (s):
    ''' This function takes a string as input, and then removes all punctuation from that string using the function
    no_punct(s), converts the whole string to lower case, and then splits the string up into a list of its individual
    words. Then the number of appearances of each word are counted and returned as a dictionary.'''
    S = no_punct(s)
    l = S.split()
    d = {}
    for word in l:
        if word in d:
            d[word] += 1
        else:
            d[word] = 1
    return d


def define_corpus(configuration):
    '''This function takes the list provided through sys.argv, which contains the configuration file (that reads the
    name of a document on each line) and opens each of the documents. It then processes the document using the
    count_words function, and adds this information to a dictionary of dictionaries, which is the output.'''
    corpus = {}
    configuration_1 = open (configuration, "r")
    for line in configuration_1:
        element = line.strip()
        handle = open (element, "r")
        handle_1 = count_words(handle)
        corpus[element] = handle_1
    return corpus

corpus = define_corpus(sys.argv[1])


def inverse_document_frequency (dict):
    ''' Takes a dictionary of dictionaries as input. Each key in the outer dictionary corresponds with a document,
    while the inner dictionary (for whom the name of the document is the key) holds the counts of each word that appear
    in that document. Then, this function calculates the IDF of each word in each of the documents. The output is
    returned as a dictionary with the words as the keys and the IDF as the values.'''
    new_dict = {}
    IDF_dict = {}
    keys = dict.keys()  # len(keys) = number of documents in corpus = N
    for element in keys:
        for key in dict[element]:
            if key in new_dict:
                new_dict[key] += 1
            else:
                new_dict[key] = 1
    for word in new_dict:
        if word not in IDF_dict:
            IDF = math.log(float(len(keys))/(float(new_dict[word] + 1.0)))
            IDF_dict[word] = IDF
    return IDF_dict

IDF = inverse_document_frequency(corpus)


def TF_IDF (words_dict, IDF):
    ''' This function multiplies the frequency of each term in a given document by the IDF of the term (from the
    IDF function). Thus, the function returns the TF-IDF, as a dictionary. '''
    TF_IDF = {}
    keys = words_dict.keys()
    for key in keys:
        TF_IDF[key] = IDF[key]
        TF_IDF[key] *= words_dict[key]
    return TF_IDF


def length (TF_IDF):
    '''This function takes  the TF-IDF of a document as input. It then uses the TF-IDF values to calculate the
    vector length of the document.'''
    length = 0.0
    for value in TF_IDF:
        length += ((TF_IDF[value]) ** 2)
    length = length ** .5
    return length


# I got some of this function from class on 5-20 (the dot product part). I edited it and added more code to complete
# the function.
def similarity (d1, d2, length_d1, length_d2):
    ''' Computes the cosine similarity of documents d1 and d2 (specified by dictionaries) using the lengths
    provided. Returns the "similarity value".'''
    DP = 0.0
    for term in d1:
        if term in d2:
           DP += d1[term] * d2[term]
    cos = DP / (length_d1 * length_d2)
    return cos


# I wrote this function because my other no_punct function was very complicated in order to account for different lines
# in a file, and as a result it was not working for just a regular string. So, I used the simpler no_punct function
# provided in class to remove punctuation from the query.
def query_no_punct(s):
    '''Removes punctuation from a string.'''
    l = []
    s= s.lower()
    for ltr in s:
        if 'a' <= ltr <= 'z':
            l.append (ltr)
        elif ltr == ' ':
            l.append(ltr)
    new_s = ''.join(l)
    return new_s


# Since I wrote another no_punct function, I had to rewrite the count_words function for the query. This wasn't a
# major change, just replacing the name of the no_punct function within.
def query_count_words (s):
    ''' This function takes a string as input, and then removes all punctuation from that string using the function
    no_punct(s), converts the whole string to lower case, and then splits the string up into a list of its
    individual words. Then the number of appearances of each word are counted and returned as a dictionary.'''
    S = query_no_punct(s)
    l = S.split()
    d = {}
    for word in l:
        if word in d:
            d[word] += 1
        else:
            d[word] = 1
    return d


def query_similarity (corpus, words_q):
    '''This function finds how relevant documents in a corpus are to a search query. This is mostly only useful for the
    program "Assignment07", as it requires information in that program to run properly. The output is a dictionary with
    the documents as the keys and the document similarity as the values.'''
    q_sim = {}
    IDF = inverse_document_frequency(corpus)
    corpus_keys = corpus.keys()
    for key in corpus_keys:
        new_dict = corpus[key]
        tf_idf_1 = TF_IDF(new_dict, IDF)
        tf_idf_q = TF_IDF(words_q, IDF)
        len_1 = length(tf_idf_1)
        len_q = length(tf_idf_q)
        q_sim[key] = similarity(tf_idf_q,tf_idf_1,len_q, len_1)
    return q_sim


Q = 0
while Q != "done":
    Q = str(raw_input("What is your search query?"))
    if Q != "done":
        q_words = query_count_words(Q)
        q_TF_IDF = TF_IDF(q_words, IDF)
        q_length = length(q_TF_IDF)
        query_sim = query_similarity(corpus, q_words)
        query_output = sorted_keys_by_value(query_sim)
        for k in range (20):
            print '{0:18s} : {1:.3f}%'.format (query_output[k][0],  query_output[k][1] * 100)
    elif Q == "done":
        print "Thank you for using the document search system!"

# Note: my similarity values seem to be coming out kind of high, but it may just be because I was testing it against
# only a couple documents...