from flask import Flask,render_template,url_for,request
import re
import pandas as pd
import spacy
from spacy import displacy
import en_core_web_sm
nlp = spacy.load('en_core_web_md')

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/process',methods=["POST"])
def process():
	if request.method == 'POST':
		choice = request.form['taskoption']
		rawtext = request.form['rawtext']
		doc = nlp(rawtext)
		d = []
		for ent in doc.ents:
			d.append((ent.label_, ent.text))
			df = pd.DataFrame(d, columns=('named entity', 'output'))
			ORG_named_entity = df.loc[df['named entity'] == 'ORG']['output']
			PERSON_named_entity = df.loc[df['named entity'] == 'PERSON']['output']
			GPE_named_entity = df.loc[df['named entity'] == 'GPE']['output']
			MONEY_named_entity = df.loc[df['named entity'] == 'MONEY']['output']
		if choice == 'organization':
			results = ORG_named_entity
			num_of_results = len(results)
		elif choice == 'person':
			results = PERSON_named_entity
			num_of_results = len(results)
		elif choice == 'geopolitical':
			results = GPE_named_entity
			num_of_results = len(results)
		elif choice == 'money':
			results = MONEY_named_entity
			num_of_results = len(results)
		
	
	return render_template("index.html",results=results,num_of_results = num_of_results)


if __name__ == '__main__':
	app.run(debug=True)