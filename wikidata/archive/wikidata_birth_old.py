# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import json
import time
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"
births = []
startyear = 1901
endyear = 2021
sitelinks = 30

def getQuery(year):
	return '''SELECT ?person ?personLabel ?personDescription ?born ?sitelinks ?image ?enwiki WHERE {
	  ?person wdt:P31 wd:Q5;
	    wikibase:sitelinks ?sitelinks;
	    wdt:P569 ?born.
	  hint:Prior hint:rangeSafe "true"^^xsd:boolean.
	  FILTER(?sitelinks >= ''' + str(sitelinks) + ''' )
	  FILTER((?born >= "''' + str(year) + '''-01-01T00:00:00Z"^^xsd:dateTime) && (?born < "''' + str(year + 1) + '''-01-01T00:00:00Z"^^xsd:dateTime))
	  OPTIONAL { ?person wdt:P18 ?image. }
	  OPTIONAL {
	    ?enwiki schema:isPartOf <https://en.wikipedia.org/>;
	      schema:about ?person.
	  }
	  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
	}
	'''

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def simple_data(l):
	obj = {}
	# obj["type"] = "person";
	obj["qid"] = l["person"]["value"].split("http://www.wikidata.org/entity/")[1]
	obj["born"] = l["born"]["value"]
	obj["sitelinks"] = l["sitelinks"]["value"]
	obj["label"] = l["personLabel"]["value"]
	if "personDescription" in l:
		obj["desc"] = l["personDescription"]["value"]
	else:
		obj["desc"] = ""
	if "image" in l:
		obj["image"] = l["image"]["value"]
	else:
		obj["image"] = ""
	if "enwiki" in l:
		obj["enwiki"] = l["enwiki"]["value"].split("https://en.wikipedia.org/wiki/")[1]
	else:
		obj["enwiki"] = ""
	return obj

def save_results(year):
	query = getQuery(year)
	results = get_results(endpoint_url, query)
	bindings = results["results"]["bindings"]
	index = 0
	if len(bindings) > 0:
		# for result in bindings:
		# 	index += 1
		# 	print(year, index)
		print(year, len(bindings))
		mapped = map(simple_data, bindings)
		births.append(mapped)
		print(len(births))

def save_csv_file(res):
	flat_res = [item for sublist in res for item in sublist]
	df = pd.DataFrame(flat_res)
	df.to_csv('births_' + str(sitelinks) + '_' + str(startyear) + '-' + str(endyear) + '.csv', index=False)

def save_json_file(res):
	flat_res = [item for sublist in res for item in sublist]
	with open('births_' + str(sitelinks) + '_' + str(startyear) + '-' + str(endyear) + '.json', 'w') as json_file:
		json.dump(flat_res, json_file)

for y in range(startyear,endyear):
	save_results(y);
	time.sleep(2)

save_csv_file(births)