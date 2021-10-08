# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import json
import time
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"
births = []
startyear = 1700
endyear = 2021
step = 10

def getQuery(year):
	return '''SELECT DISTINCT ?qid ?label ?desc ?sitelinks
	(GROUP_CONCAT(DISTINCT ?dateValue;separator="|") AS ?date) #get all dates
	(GROUP_CONCAT(DISTINCT ?dateSource;separator="|") AS ?dateInfo)
	(SAMPLE(?image) AS ?image)
	(GROUP_CONCAT(DISTINCT ?pLabel;separator="|") as ?place)
	(GROUP_CONCAT(DISTINCT ?tLabel;separator="|") as ?territory)
	(GROUP_CONCAT(DISTINCT ?cLabel;separator="|") AS ?country)
	(GROUP_CONCAT(DISTINCT ?coordPlace;separator="|") as ?coordinates)
	WHERE {
	  ?s wdt:P31 wd:Q5. #human
	  ?s p:P569/psv:P569 ?dateNode.  
	  ?dateNode wikibase:timeValue ?dateValue. hint:Prior hint:rangeSafe "true"^^xsd:boolean.
	  FILTER((?dateValue >= "''' + str(year) + '''-01-01T00:00:00Z"^^xsd:dateTime) && (?dateValue < "''' + str(year + step) + '''-01-01T00:00:00Z"^^xsd:dateTime))
	  #FILTER((?dateValue >= "1980-01-01T00:00:00Z"^^xsd:dateTime) && (?dateValue < "1981-01-01T00:00:00Z"^^xsd:dateTime))
	  ?s wikibase:sitelinks ?sitelinks. FILTER( ?sitelinks >= 20 ) #the more sitelinks, the more likely you know it, the more "universal"
	  ?dateNode wikibase:timePrecision "11"^^xsd:integer. #precise to the day
	  BIND(SUBSTR(STR(?s),STRLEN("http://www.wikidata.org/entity/Q")) AS ?qid).
	  ?s p:P19/ps:P19 ?p. #required place of birth #return all places of birth, ignore preferred rank
	  OPTIONAL { ?s p:P569/pq:P1480 ?ds. ?ds rdfs:label ?dateSource. FILTER((LANG(?dateSource)) = "en") }
	  OPTIONAL { ?p rdfs:label ?pLabel. FILTER((LANG(?pLabel)) = "en") }
	  OPTIONAL { ?s wdt:P18 ?image. }
	  OPTIONAL { ?p wdt:P17 ?c. ?c rdfs:label ?cLabel. FILTER((LANG(?cLabel)) = "en") }
	  OPTIONAL { ?p wdt:P625 ?coordPlace. }
	  OPTIONAL { ?p wdt:P131 ?t. ?t rdfs:label ?tLabel. FILTER((LANG(?tLabel)) = "en") }
	  OPTIONAL { ?s rdfs:label ?label. FILTER((LANG(?label)) = "en") }
	  OPTIONAL { ?s schema:description ?desc. FILTER((LANG(?desc)) = "en") }
	}
	GROUP BY ?qid ?label ?desc ?sitelinks 
	ORDER BY DESC(?sitelinks)'''

# https://query.wikidata.org/#SELECT%20DISTINCT%20%3Fqid%20%3Flabel%20%3Fdesc%20%3Fsitelinks%0A%28GROUP_CONCAT%28DISTINCT%20%3FdateValue%3Bseparator%3D%22%7C%22%29%20AS%20%3Fdate%29%20%23get%20all%20dates%0A%28GROUP_CONCAT%28DISTINCT%20%3FdateSource%3Bseparator%3D%22%7C%22%29%20AS%20%3FdateInfo%29%0A%28SAMPLE%28%3Fimage%29%20AS%20%3Fimage%29%0A%28GROUP_CONCAT%28DISTINCT%20%3FpLabel%3Bseparator%3D%22%7C%22%29%20as%20%3Fplace%29%0A%28GROUP_CONCAT%28DISTINCT%20%3FtLabel%3Bseparator%3D%22%7C%22%29%20as%20%3Fterritory%29%0A%28GROUP_CONCAT%28DISTINCT%20%3FcLabel%3Bseparator%3D%22%7C%22%29%20AS%20%3Fcountry%29%0A%28GROUP_CONCAT%28DISTINCT%20%3FcoordPlace%3Bseparator%3D%22%7C%22%29%20as%20%3Fcoordinates%29%0AWHERE%20%7B%0A%20%20%3Fs%20wdt%3AP31%20wd%3AQ5.%20%23human%0A%20%20%3Fs%20p%3AP569%2Fpsv%3AP569%20%3FdateNode.%20%20%0A%20%20%3FdateNode%20wikibase%3AtimeValue%20%3FdateValue.%20hint%3APrior%20hint%3ArangeSafe%20%22true%22%5E%5Exsd%3Aboolean.%0A%23%20%20%20FILTER%28%28%3FdateValue%20%3E%3D%20%22%27%27%27%20%2B%20str%28year%29%20%2B%20%27%27%27-01-01T00%3A00%3A00Z%22%5E%5Exsd%3AdateTime%29%20%26%26%20%28%3FdateValue%20%3C%20%22%27%27%27%20%2B%20str%28year%20%2B%20step%29%20%2B%20%27%27%27-01-01T00%3A00%3A00Z%22%5E%5Exsd%3AdateTime%29%29%0A%20%20FILTER%28%28%3FdateValue%20%3E%3D%20%221980-01-01T00%3A00%3A00Z%22%5E%5Exsd%3AdateTime%29%20%26%26%20%28%3FdateValue%20%3C%20%221981-01-01T00%3A00%3A00Z%22%5E%5Exsd%3AdateTime%29%29%0A%20%20%3Fs%20wikibase%3Asitelinks%20%3Fsitelinks.%20FILTER%28%20%3Fsitelinks%20%3E%3D%2020%20%29%20%23the%20more%20sitelinks%2C%20the%20more%20likely%20you%20know%20it%2C%20the%20more%20%22universal%22%0A%20%20%3FdateNode%20wikibase%3AtimePrecision%20%2211%22%5E%5Exsd%3Ainteger.%20%23precise%20to%20the%20day%0A%20%20BIND%28SUBSTR%28STR%28%3Fs%29%2CSTRLEN%28%22http%3A%2F%2Fwww.wikidata.org%2Fentity%2FQ%22%29%29%20AS%20%3Fqid%29.%0A%20%20%3Fs%20p%3AP19%2Fps%3AP19%20%3Fp.%20%23required%20place%20of%20birth%20%23return%20all%20places%20of%20birth%2C%20ignore%20preferred%20rank%0A%20%20OPTIONAL%20%7B%20%3Fs%20p%3AP569%2Fpq%3AP1480%20%3Fds.%20%3Fds%20rdfs%3Alabel%20%3FdateSource.%20FILTER%28%28LANG%28%3FdateSource%29%29%20%3D%20%22en%22%29%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fp%20rdfs%3Alabel%20%3FpLabel.%20FILTER%28%28LANG%28%3FpLabel%29%29%20%3D%20%22en%22%29%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fs%20wdt%3AP18%20%3Fimage.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fp%20wdt%3AP17%20%3Fc.%20%3Fc%20rdfs%3Alabel%20%3FcLabel.%20FILTER%28%28LANG%28%3FcLabel%29%29%20%3D%20%22en%22%29%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fp%20wdt%3AP625%20%3FcoordPlace.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fp%20wdt%3AP131%20%3Ft.%20%3Ft%20rdfs%3Alabel%20%3FtLabel.%20FILTER%28%28LANG%28%3FtLabel%29%29%20%3D%20%22en%22%29%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fs%20rdfs%3Alabel%20%3Flabel.%20FILTER%28%28LANG%28%3Flabel%29%29%20%3D%20%22en%22%29%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fs%20schema%3Adescription%20%3Fdesc.%20FILTER%28%28LANG%28%3Fdesc%29%29%20%3D%20%22en%22%29%20%7D%0A%7D%0AGROUP%20BY%20%3Fqid%20%3Flabel%20%3Fdesc%20%3Fsitelinks%20%0AORDER%20BY%20DESC%28%3Fsitelinks%29

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def simple_data(l):
	obj = {}
	keys = ["qid", "date", "dateInfo", "sitelinks", "label", "desc", "image", "place", "territory", "country", "coordinates" ]
	for key in keys:
		obj[key] = l[key]["value"] if key in l else ""
	return obj

def save_results(year):
	query = getQuery(year)
	results = get_results(endpoint_url, query)
	bindings = results["results"]["bindings"]
	index = 0
	print(year, len(bindings))
	if len(bindings) > 0:
		# for result in bindings:
		# 	index += 1
		# 	print(year, index)
		mapped = map(simple_data, bindings)
		births.append(mapped)
		print(">>> total", len(births))

def save_csv_file(res):
	flat_res = [item for sublist in res for item in sublist]
	df = pd.DataFrame(flat_res)
	df.to_csv('births_' + str(startyear) + '-' + str(endyear) + '.csv', index=False)

for y in range(startyear, endyear, step):
	save_results(y);
	time.sleep(2)

save_csv_file(births)
