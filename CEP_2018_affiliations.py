"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
    
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
#client.inst_token = config['insttoken']

## Author example
# Initialize author with uri
my_auth = ElsAuthor(
        uri = 'https://api.elsevier.com/content/author/author_id/7203071981')
# Read author data, then write to disk
if my_auth.read(client):
    print ("my_auth.full_name: ", my_auth.full_name)
    my_auth.write()
else:
    print ("Read author failed.")



## Initialize doc search object using Scopus and execute search, retrieving 
#   all results
for source in searches:
    doc_srch = ElsSearch(searches[source],'scopus')
    doc_srch.execute(client, get_all = True)
    print ("doc_srch has", len(doc_srch.results), "results.")

    doc_uris = []
    for doc in doc_srch.results:
        doc_uri = doc["prism:url"]
        doc_uris.append(doc_uri)
        scp_doc = AbsDoc(uri = doc_uri)
        if scp_doc.read(client):
            print ("scp_doc.title: ", scp_doc.title)
            scp_doc.write()   
        else:
            print ("Read document failed.")

    with open(source+'_papers.json', 'w') as fp:
        json.dump(doc_uris, fp)





    
