# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import json
import time
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"
births = []
startyear = 1900
endyear = 2021
sitelinks = 20
basefname = "novel_"

# modify query and amount time advances per loop to avoid time out
def getQuery(start, end):
	return '''SELECT DISTINCT ?s ?sLabel ?sDescription ?sitelinks
	(MIN(?date) AS ?datePublication) #earliest date = first publication
	(SAMPLE(?image) AS ?image)
	(GROUP_CONCAT(DISTINCT ?countryOriginLabel;separator="|") AS ?country)
	WHERE {
		  #{wd:Q11424 ^wdt:P279*/^wdt:P31 ?s.} #UNION #film, slow
		  #{wd:Q7725634 ^wdt:P279*/^wdt:P31 ?s.} #UNION 
		  {wd:Q8261 ^wdt:P279*/^wdt:P31 ?s.} #UNION #literary work and novel
		  #{wd:Q5398426 ^wdt:P279*/^wdt:P31 ?s.} UNION #tv series
		  #{wd:Q7889 ^wdt:P279*/^wdt:P31 ?s.} UNION #video game
		  #{wd:Q482994 ^wdt:P279*/^wdt:P31 ?s.} #album
		  ?s p:P577/psv:P577 ?dateNode.
	      ?dateNode wikibase:timeValue ?date.
		  hint:Prior hint:rangeSafe "true"^^xsd:boolean.
	      ?dateNode wikibase:timePrecision ?datePrecision.
		  FILTER((?date >= "''' + str(start) + '''T00:00:00Z"^^xsd:dateTime) && (?date < "''' + str(end) + '''T00:00:00Z"^^xsd:dateTime))
		  #FILTER((?date >= "1980-01-01T00:00:00Z"^^xsd:dateTime) && (?date < "1981-01-01T00:00:00Z"^^xsd:dateTime))
		  ?s wikibase:sitelinks ?sitelinks.
	 	  FILTER(?sitelinks >= ''' + str(sitelinks) + ''' )
	      #FILTER(?sitelinks >= 20 )
	      FILTER(?datePrecision >= 11 ) #precise to the day
	      OPTIONAL{ ?s (wdt:P18|wdt:P154)+ ?image }
	      OPTIONAL{ ?s wdt:P495 ?countryOrigin }
		  SERVICE wikibase:label { 
	        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". 
	        ?s rdfs:label ?sLabel .
	        ?s schema:description ?sDescription .
	        ?countryOrigin rdfs:label ?countryOriginLabel .
	      }
		}
	GROUP BY ?s ?sLabel ?sDescription ?sitelinks'''

#https://query.wikidata.org/#%23cultural%20artefacts%20-%20selection%0ASELECT%20DISTINCT%20%3Fs%20%3FsLabel%20%3FsDescription%20%3Fsitelinks%0A%28MIN%28%3Fdate%29%20AS%20%3FdatePublication%29%20%23earliest%20date%20%3D%20first%20publication%0A%28SAMPLE%28%3Fimage%29%20AS%20%3Fimage%29%0A%28GROUP_CONCAT%28DISTINCT%20%3FcountryOriginLabel%3Bseparator%3D%22%7C%22%29%20AS%20%3Fcountry%29%0AWHERE%20%7B%0A%20%20%20%20%20%20%23%7B%3Fs%20wdt%3AP31%2Fwdt%3AP279%2a%20wd%3AQ11424.%7D%20UNION%20%23film%2C%20slow%0A%20%20%20%20%20%20%7Bwd%3AQ11424%20%5Ewdt%3AP279%2a%2F%5Ewdt%3AP31%20%3Fs.%7D%20UNION%20%23film%2C%20slow%0A%20%20%20%20%20%20%7Bwd%3AQ7725634%20%5Ewdt%3AP279%2a%2F%5Ewdt%3AP31%20%3Fs.%7D%20UNION%20%7Bwd%3AQ8261%20%5Ewdt%3AP279%2a%2F%5Ewdt%3AP31%20%3Fs.%7D%20UNION%20%23literary%20work%20and%20novel%0A%20%20%20%20%20%20%7Bwd%3AQ5398426%20%5Ewdt%3AP279%2a%2F%5Ewdt%3AP31%20%3Fs.%7D%20UNION%20%23tv%20series%0A%20%20%20%20%20%20%7Bwd%3AQ7889%20%5Ewdt%3AP279%2a%2F%5Ewdt%3AP31%20%3Fs.%7D%20UNION%20%23video%20game%0A%20%20%20%20%20%20%7Bwd%3AQ482994%20%5Ewdt%3AP279%2a%2F%5Ewdt%3AP31%20%3Fs.%7D%20%23album%0A%09%20%20%3Fs%20p%3AP577%2Fpsv%3AP577%20%3FdateNode.%0A%20%20%20%20%20%20%3FdateNode%20wikibase%3AtimeValue%20%3Fdate.%0A%09%20%20hint%3APrior%20hint%3ArangeSafe%20%22true%22%5E%5Exsd%3Aboolean.%0A%20%20%20%20%20%20%3FdateNode%20wikibase%3AtimePrecision%20%3FdatePrecision.%0A%09%20%20FILTER%28%28%3Fdate%20%3E%3D%20%221967-01-01T00%3A00%3A00Z%22%5E%5Exsd%3AdateTime%29%20%26%26%20%28%3Fdate%20%3C%20%221968-01-01T00%3A00%3A00Z%22%5E%5Exsd%3AdateTime%29%29%0A%09%20%20%3Fs%20wikibase%3Asitelinks%20%3Fsitelinks.%0A%20%20%20%20%20%20FILTER%28%3Fsitelinks%20%3E%3D%2020%20%29%0A%20%20%20%20%20%20FILTER%28%3FdatePrecision%20%3E%3D%2011%20%29%20%23precise%20to%20the%20day%0A%20%20%20%20%20%20OPTIONAL%7B%20%3Fs%20%28wdt%3AP18%7Cwdt%3AP154%29%2B%20%3Fimage%20%7D%0A%20%20%20%20%20%20OPTIONAL%7B%20%3Fs%20wdt%3AP495%20%3FcountryOrigin%20%7D%0A%09%20%20SERVICE%20wikibase%3Alabel%20%7B%20%0A%20%20%20%20%20%20%20%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%0A%20%20%20%20%20%20%20%20%3Fs%20rdfs%3Alabel%20%3FsLabel%20.%0A%20%20%20%20%20%20%20%20%3Fs%20schema%3Adescription%20%3FsDescription%20.%0A%20%20%20%20%20%20%20%20%3FcountryOrigin%20rdfs%3Alabel%20%3FcountryOriginLabel%20.%0A%20%20%20%20%20%20%7D%0A%09%7D%0AGROUP%20BY%20%3Fs%20%3FsLabel%20%3FsDescription%20%3Fsitelinks%0AORDER%20BY%20DESC%28%3Fsitelinks%29%0A%23https%3A%2F%2Fen.wikibooks.org%2Fwiki%2FSPARQL%2FWIKIDATA_Precision%2C_Units_and_Coordinates%23Time%0A%230%3A%20billion%20years%2C%201%3A%20hundred%20million%20years%2C%203%3A%20million%20years%2C%204%3A%20hundred%20thousand%20years%2C%205%3A%20ten%20thousand%20years%2C%206%3A%20millennium%2C%207%3A%20century%2C%208%3A%20decade%2C%209%3A%20year%2C%2010%3A%20month%2C%2011%3A%20day%2C%2012%3A%20hour%2C%2013%3A%20minute%2C%2014%3A%20second.
#0: billion years, 1: hundred million years, 3: million years, 4: hundred thousand years, 5: ten thousand years, 6: millennium, 7: century, 8: decade, 9: year, 10: month, 11: day, 12: hour, 13: minute, 14: second.

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def simple_data(l):
	obj = {}
	obj["type"] = "work";
	obj["qid"] = l["s"]["value"].split("http://www.wikidata.org/entity/")[1]
	obj["date"] = l["datePublication"]["value"]
	obj["sitelinks"] = l["sitelinks"]["value"]
	obj["label"] = l["sLabel"]["value"]
	obj["desc"] = l["sDescription"]["value"] if "sDescription" in l else ""
	obj["image"] = l["image"]["value"] if "image" in l else ""
	obj["country"] = l["country"]["value"] if "country" in l else ""
	return obj

def save_results(start, end):
	query = getQuery(start, end)
	results = get_results(endpoint_url, query)
	bindings = results["results"]["bindings"]
	index = 0
	if len(bindings) > 0:
		# for result in bindings:
		# 	index += 1
		# 	print(year, index)
		print(start, end, len(bindings))
		mapped = map(simple_data, bindings)
		births.append(mapped)
		print(len(births))

def save_csv_file(res):
	flat_res = [item for sublist in res for item in sublist]
	df = pd.DataFrame(flat_res)
	df.to_csv(basefname + str(sitelinks) + '_' + str(startyear) + '-' + str(endyear) + '.csv', index=False)

def save_json_file(res):
	flat_res = [item for sublist in res for item in sublist]
	with open(basefname + str(sitelinks) + '_' + str(startyear) + '-' + str(endyear) + '.json', 'w') as json_file:
		json.dump(flat_res, json_file)

startDate = pd.to_datetime(str(startyear) + "-01-01", format='%Y-%m-%d')
endDate = pd.to_datetime(str(endyear) + "-01-01", format='%Y-%m-%d')

while (endDate - startDate).days > 0:
	start = startDate
	end = startDate + pd.DateOffset(months=6)
	save_results(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'));
	time.sleep(2)
	startDate = end

save_csv_file(births)
