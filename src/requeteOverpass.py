from OSMPythonTools.overpass import Overpass
overpass = Overpass()

# create a bus request with the name of the bus line
def generate_request(name_line):
	request='''
	area["ISO3166-1"="FR"][admin_level=2];
		(
			relation["route"="bus"][name~"^{}"](area);
		);
		out body;
		>;
		out skel qt;'''.format(name_line)
	return request

# create a bus request with the name of the bus line and the operator
def generate_request_withOperator(name_line, operator):
	request ='''
	area["ISO3166-1"="FR"][admin_level=2];
		(
			relation["route"="bus"][name~"^{}"]["operator"="{}"](area);
		);
		out body;
		>;
		out skel qt;'''.format(name_line, operator)
	return request

# bus request for the network RATP
query_allNetwork_RATP='''
area[name="Paris"]->.searchArea;
( 
  relation["route"="bus"]["operator"="RATP"](area.searchArea);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Haut de France
query_allNetworkHautDeFrance='''
( 
  relation["route"="bus"](49.4599, 1.3607, 51.1537, 4.3963);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Auvergne Rhone Alpes
query_allNetworkAuvergne_Rhone_Alpes='''
( 
  relation["route"="bus"](44.7958, 2.9209, 46.5987, 7.7679);
);
out body;
>;
out skel qt; '''

# bus request for the line 60 from RATP
query_line60_fromRATP='''
area[name="Paris"]->.searchArea;
( 
  relation["route"="bus"]["operator"="RATP"][name~"^Bus 60"](area.searchArea);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Bourgogne Franche Comte
query_allNetworkBourgogne_Franche_Comte='''
( 
  relation["route"="bus"](46.0938, 3.9648, 48.0714, 7.2138);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Bretagne
query_allNetworkBretagne='''
( 
  relation["route"="bus"](47.9215, -5.3901, 48.8459, -1.0901);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Centre Val de Loire
query_allNetworkCentre_Val_de_Loire='''
( 
  relation["route"="bus"](46.2366, 0.2332, 48.0089, 3.3036);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Corse
query_allNetworkCorse='''
( 
  relation["route"="bus"](41.0918, 8.4082, 43.1497, 9.8622);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Grand Est
query_allNetworkGrand_Est='''
( 
  relation["route"="bus"](47.7151, 2.5879, 49.7767, 7.3140);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Ile de France
query_allNetworkIle_de_France='''
( 
  relation["route"="bus"](48.2751, 1.4449, 49.3126, 3.5596);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Normandie
query_allNetworkNormandie='''
( 
  relation["route"="bus"](48.2915, -1.9268, 50.0039, 1.8952);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Nouvelle Aquitaine
query_allNetworkNouvelle_Aquitaine='''
( 
  relation["route"="bus"](43.2682, -1.7236, 46.1937, 2.1069);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Occitanie
query_allNetworkOccitanie='''
( 
  relation["route"="bus"](42.1577, 0.7129, 44.6742, 4.1390);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Pays de la Loire
query_allNetworkPays_de_la_Loire='''
( 
  relation["route"="bus"](46.2366, -3.5376, 48.0589, -0.5570);
);
out body;
>;
out skel qt; '''

# bus request for the whole region Provence Alpes Cote d'Azur
query_allNetworkProvence_Alpes_Cote_Azur='''
( 
  relation["route"="bus"](42.9001, 5.5059, 44.4950, 7.8223);
);
out body;
>;
out skel qt; '''





