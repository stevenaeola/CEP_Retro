"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("conference")
args = parser.parse_args()

conference = args.conference


## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
#client.inst_token = config['insttoken']


searches = {
    "CEP": "CONFNAME(Computing Education Practice)",
    "Koli": 'CONF ( "Koli" ) AND AFFILCOUNTRY ( "United kingdom" )  AND ( PUBYEAR > 2018 )'
}

if not (conference in searches):
    raise Exception("unknown conference " + conference)

#  "85219189082" is a CEP poster, no abstract

uri_excludes = [

    "85123040964",  # full proceedings listings for CEP
    "85219170733",
    "85182755414",
    "85145836845",
    "85122628388",
    "85099461088",
    "85123042521"
]


def uri_excluded(fname):
    for uri_exclude in uri_excludes:
        if uri_exclude in fname:
            return True
    return False

## Initialize doc search object using Scopus and execute search, retrieving 
#   all results
for source in searches:
    doc_srch = ElsSearch(searches[source],'scopus')
    doc_srch.execute(client, get_all = True)
    print ("doc_srch has", len(doc_srch.results), "results.")

    doc_uris = []
    for doc in doc_srch.results:
        doc_uri = doc["prism:url"]
        if(uri_excluded(doc_uri)):
            print ("Excluding " + doc_uri + " from " + source)
            continue
        scp_doc = AbsDoc(uri = doc_uri)
        doc_uris.append(doc_uri)
        if scp_doc.read(client):
            print ("scp_doc.title: ", scp_doc.title)
            scp_doc.write()   
        else:
            print ("Read document failed.")

    with open(source+'_papers.json', 'w') as fp:
        json.dump(doc_uris, fp)





    
