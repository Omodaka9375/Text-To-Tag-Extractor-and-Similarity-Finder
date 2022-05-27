import spacy
import subprocess
from string import punctuation
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from fuzzywuzzy import process
from fuzzywuzzy.fuzz import ratio

# download the small model 
subprocess.call("python -m spacy download en_core_web_sm", shell=True) # english language pack
subprocess.call("python -m spacy download de_core_news_sm", shell=True) # german language pack
subprocess.call("python -m spacy download es_core_news_sm", shell=True) # spanish language pack

app = Flask(__name__)
CORS(app)

@app.route('/api/get-tags', methods=['POST'])
def get_keywords():
    query_string = request.json.get("text")
    lang = request.json.get("lang")
    if(lang=="en"):
        lang_pack = "en_core_web_sm"
    elif(lang=="es"):
        lang_pack = "es_core_news_sm"
    elif(lang=="de"):
        lang_pack = "de_core_news_sm"
    else:
        lang_pack = "en_core_web_sm"
    nlp_pack = spacy.load(lang_pack)
    keywords = extract_keywords(nlp_pack,query_string)
    return jsonify(keywords = keywords)

@app.route('/api/find-matches', methods=['POST'])
def get_fuzzy_matches():
    token = request.json.get("phrase")
    dictionary = request.json.get("tags")
    similar_words = get_fuzzy_similarity(token,dictionary)
    return jsonify(similar_words = similar_words)

def get_fuzzy_similarity(token = None, dictionary = None):
    """Returns similar words and similarity scores for a given token
    from a provided dictionary of words
    
    Keyword Arguments:
        token {str} -- the reference word (default: {None})
        dictionary {list} -- the list of target words (default: {None})
    
    Returns:
        [list] -- a list of tuples in the form `(matched_word, similarity score)`
    """    

    if token and dictionary:
        return process.extractBests(token, dictionary, scorer= ratio, score_cutoff=70)
    else:
        return []

def extract_keywords(nlp, sequence):
    """ Takes a Spacy core language model,
    string sequence of text and optional
    list of special tags as arguments.
    
    If any of the words in the string are 
    in the list of special tags they are immediately 
    added to the result.  
    
    Arguments:
        sequence {str} -- string sequence to have keywords extracted from
    
    Keyword Arguments:
        tags {list} --  list of tags to be automatically added (default: {None})
    
    Returns:
        {list} -- list of the unique keywords extracted from a string
    """    
    result = []

    # custom list of part of speech tags we are interested in
    # we are interested in proper nouns, nouns, and adjectives
    # edit this list of POS tags according to your needs. 
    pos_tag = ['PROPN','NOUN']

    # create a spacy doc object by calling the nlp object on the input sequence
    doc = nlp(sequence.lower())
    
    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if (token.pos_ in pos_tag):
                final_chunk =  final_chunk + token.text + " "
        if final_chunk:
            result.append(final_chunk.strip())


    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return list(set(result))


if __name__ == '__main__':
	app.run(debug=False)