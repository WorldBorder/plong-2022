import json
import os
import unittest
import requete_bus
import requeteOverpass
from OSMPythonTools.overpass import Overpass
overpass = Overpass()

# check if you get an error or not
def testErrorSummary(error):
	if not requete_bus.ErrorSummary.getErrors(error):
		print("no problem\n") 
		return True
	else: 
		print(error)
		return False

# check if the json file has already been created
def createOrUpdateJsonFile(jsonFile, jsonData):
	if os.path.exists(jsonFile):
		with open(jsonFile, "r") as test:
			content = test.read()
			if content == json.dumps(jsonData):
				return	
	with open(jsonFile, "w") as test:
		json.dump(jsonData, test, indent=4)

# retrieves tab relations, ways, and nodes information
def createTab(res):
	elem = res["elements"]
	nodes= []
	ways=[]
	relations=[]
	for i in elem:
		if(i['type']=='node'):
				nodes.append(i)
		if(i['type']=='way'):
				ways.append(i)
		if(i['type']=='relation'):
				relations.append(i)	
	return relations, ways, nodes

# create relations, ways and nodes
def createRelation_Way_Node(jsonFile, res):
	createOrUpdateJsonFile(jsonFile, res)
	relations, ways, nodes = createTab(res)
	return relations, ways, nodes	

# open the Haut de France query and create the corresponding json with the query data 
def allNetworkHautDeFrance_Bus():
	resultat = overpass.query(requeteOverpass.query_allNetworkHautDeFrance, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkHautDeFrance_Bus.json"
	return createRelation_Way_Node(jsonFile, res)								

# open the RATP query and create the corresponding json with the query data 
def allNetwork_RATP():
	resultat = overpass.query(requeteOverpass.query_allNetwork_RATP)
	res = resultat.toJSON()
	jsonFile = "Json/allNetwork_RATP.json"
	return createRelation_Way_Node(jsonFile, res)

# open the line 60 (RATP) query and create the corresponding json with the query data 
def line60_RATP():
	resultat = overpass.query(requeteOverpass.query_line60_fromRATP)
	res = resultat.toJSON()
	jsonFile = "Json/line60_FromRATP.json"
	return createRelation_Way_Node(jsonFile, res)

# open the line 60 (RATP) json with false information
def line60_RATP_false():
    with open('Json/line60_FromRATP_false.json', 'r') as file:
        json_data = json.load(file)	
    res = createTab(json_data)
    return res

# open the Auvergne query and create the corresponding json with the query data 
def allNetworkAuvergne_Rhone_Alpes():
	resultat = overpass.query(requeteOverpass.query_allNetworkAuvergne_Rhone_Alpes, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkAuvergne_Rhone_Alpes.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Bourgogne query and create the corresponding json with the query data 
def allNetworkBourgogne_France_Comte():
	resultat = overpass.query(requeteOverpass.query_allNetworkBourgogne_Franche_Comte, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkBourgogne_France_Comte.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Bretagne query and create the corresponding json with the query data 	
def allNetworkBretagne():
	resultat = overpass.query(requeteOverpass.query_allNetworkBretagne, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkBretagne.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Centre Val de Loire query and create the corresponding json with the query data 
def allNetworkCentre_Val_de_Loire():
	resultat = overpass.query(requeteOverpass.query_allNetworkCentre_Val_de_Loire, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkCentre_Val_de_Loire.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Corse query and create the corresponding json with the query data 
def allNetworkCorse():
	resultat = overpass.query(requeteOverpass.query_allNetworkCorse, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkCorse.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Grand Est query and create the corresponding json with the query data 
def allNetworkGrand_Est():
	resultat = overpass.query(requeteOverpass.query_allNetworkGrand_Est, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkGrand_Est.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Ile de France query and create the corresponding json with the query data 
def allNetworkIle_de_France():
	resultat = overpass.query(requeteOverpass.query_allNetworkIle_de_France, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkIle_de_France.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Normandie query and create the corresponding json with the query data 
def allNetworkNormandie():
	resultat = overpass.query(requeteOverpass.query_allNetworkNormandie, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkNormandie.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Nouvelle Aquitaine query and create the corresponding json with the query data 
def allNetworkNouvelle_Aquitaine():
	resultat = overpass.query(requeteOverpass.query_allNetworkNouvelle_Aquitaine, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkNouvelle_Aquitaine.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Occitanie query and create the corresponding json with the query data 
def allNetworkOccitanie():
	resultat = overpass.query(requeteOverpass.query_allNetworkOccitanie, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkOccitanie.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Pays de la Loire query and create the corresponding json with the query data 
def allNetworkPays_de_la_Loire():
	resultat = overpass.query(requeteOverpass.query_allNetworkPays_de_la_Loire, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkPays_de_la_Loire.json"
	return createRelation_Way_Node(jsonFile, res)

# open the Province Alpes Cote Azur query and create the corresponding json with the query data 
def allNetworkProvence_Alpes_Cote_Azur():
	resultat = overpass.query(requeteOverpass.query_allNetworkProvence_Alpes_Cote_Azur, timeout=60)
	res = resultat.toJSON()
	jsonFile = "Json/allNetworkProvence_Alpes_Cote_Azur.json"
	return createRelation_Way_Node(jsonFile, res)

	
