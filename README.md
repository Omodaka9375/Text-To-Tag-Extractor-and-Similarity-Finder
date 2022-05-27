# Text-To-Tag Extractor and Similarity Finder 

## Usage

This is a lightweight REST API done with Python/Flask that is using SpaCy NLP library for tasks of extracting tags from text and finding similarity between them.

There are two endpoints:

- ```/api/get-tags``` - where verbs, phrases and important nouns are extracted as tags from given text
- ```/api/find-matches``` - where one phrase/word is matched by similarity within group of tags

## Requirements

```Python 3.x```

## Running the app

```pip install requirements.txt```

```python app.py```

## Language packs

There are 3 languages that are supported (more can be added) and they are download when the server starts:

Supported languages:  ```English, German and Spanish```

Parameter short names:  ```"en", "de", "es"```

## Endpoints

### Convert sentence to tags

```POST http://127.0.0.0:5000/api/get-tags```

You need to pass two parameters in JSON body - the source text and the language used:

If language parameter is ommited it will default to English.

```BODY {"text": "Enjoying nature outside, phishing and ocassional barbeque", "lang": "en"}```

#### Example result

```
{
	"keywords": [
		"barbeque",
		"phishing",
		"nature"
	]
}
```

### Find similar terms amongs tags

```POST http://127.0.0.0:5000/api/find-matches```

```BODY {"phrase": "wrestle", "tags": ["wrestling", "swimming"]}```

#### Example result

```
{
	"similar_words": [
		[
			"wrestling",
			75
		]
	]
}
```