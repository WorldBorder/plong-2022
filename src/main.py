import json
import os
import unittest
import requete_bus
import requeteOverpass
import createJson
import tag_verification
import plotly.express as px
from OSMPythonTools.overpass import Overpass
overpass = Overpass()

# class for unit test
class TestTEST(unittest.TestCase):

    # test for all network RATP
    def test_allNetwork_RATP_ways(self):
        print("Testing the RATP operator paths:")
        relations, ways, nodes = createJson.allNetwork_RATP()
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetwork_RATP_nodes(self):
        print("Test the order of RATP nodes:")
        relations, ways, nodes = createJson.allNetwork_RATP()
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0],nodes,ways)))

    def test_allNetwork_RATP_members_role(self):
        print("Test on the roles of RATP members:")
        relations, ways, nodes = createJson.allNetwork_RATP()
        self.assertTrue(createJson.testErrorSummary(tag_verification.check_members_role(relations[0])))

    def test_allNetwork_RATP_route_tags(self):
        print("Test on RATP route tags:")
        relations, ways, nodes = createJson.allNetwork_RATP()
        self.assertTrue(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))

    # test for network Haut de France
    def test_allNetworkHautDeFrance_ways(self):
        print("Test on the ways in Haut de France: ")
        relations, ways, nodes = createJson.allNetworkHautDeFrance_Bus()
        print("For the bus line "+ str(relations[0]['tags']['name'])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkHautDeFrance_nodes(self):
        print("Test on the order of nodes in Haut de France:")
        relations, ways, nodes = createJson.allNetworkHautDeFrance_Bus()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertFalse(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkHautDeFrance_route_tag(self):
        print("Test on Haut de France road tags:")
        relations, ways, nodes = createJson.allNetworkHautDeFrance_Bus()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertFalse(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))

    # test for network Bourgogne
    def test_allNetworkBourgogne_France_Comte_ways(self):
        print("Test on Bourgogne ways:")
        relations, ways, nodes = createJson.allNetworkBourgogne_France_Comte()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkBourgogne_France_Comte_nodes(self):
        print("Test on Bourgogne nodes:")
        relations, ways, nodes = createJson.allNetworkBourgogne_France_Comte()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkBourgogne_route_tag(self):
        print("Test on Bourgogne tags:")
        relations, ways, nodes = createJson.allNetworkBourgogne_France_Comte()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))    


    # test for network Auvergne
    def test_allNetworkAuvergne_ways(self):
        print("Test on Auvergne ways:")
        relations, ways, nodes = createJson.allNetworkAuvergne_Rhone_Alpes()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkAuvergne_nodes(self):
        print("Test on Auvergne nodes:")
        relations, ways, nodes = createJson.allNetworkAuvergne_Rhone_Alpes()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkAuvergne_route_tag(self):
        print("Test on Auvergne tags:")
        relations, ways, nodes = createJson.allNetworkAuvergne_Rhone_Alpes()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))      



    # test for network Bretagne
    def test_allNetworkBretagne_ways(self):
        print("Test on Bretagne ways:")
        relations, ways, nodes = createJson.allNetworkBretagne()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkBretagne_nodes(self):
        print("Test on Bretagne nodes:")
        relations, ways, nodes = createJson.allNetworkBretagne()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkBretagne_route_tag(self):
        print("Test on Bretagne tags:")
        relations, ways, nodes = createJson.allNetworkBretagne()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertFalse(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))    


    # test for network Centre Val de Loire
    def test_allNetworkCentre_Val_de_Loire_ways(self):
        print("Test on Centre Val de Loire ways:")
        relations, ways, nodes = createJson.allNetworkCentre_Val_de_Loire()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkCentre_Val_de_Loire_nodes(self):
        print("Test on Centre Val de Loire nodes:")
        relations, ways, nodes = createJson.allNetworkCentre_Val_de_Loire()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertFalse(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkCentre_Val_de_Loire_route_tag(self):
        print("Test on Centre Val de Loire tags:")
        relations, ways, nodes = createJson.allNetworkCentre_Val_de_Loire()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertFalse(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))     


    # test for network Corse
    def test_allNetworkCorse_ways(self):
        print("Test on Corse ways:")
        relations, ways, nodes = createJson.allNetworkCorse()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkCorse_nodes(self):
        print("Test on Corse nodes:")
        relations, ways, nodes = createJson.allNetworkCorse()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkCorse_route_tag(self):
        print("Test on Corse tags:")
        relations, ways, nodes = createJson.allNetworkCorse()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertFalse(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))      


    # test for network Grand Est
    def test_allNetworkGrand_Est_ways(self):
        print("Test on Grand Est ways:")
        relations, ways, nodes = createJson.allNetworkGrand_Est()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertFalse(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkGrand_Est_nodes(self):
        print("Test on Grand Est nodes:")
        relations, ways, nodes = createJson.allNetworkGrand_Est()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkGrand_Est_route_tag(self):
        print("Test on Grand Est tags:")
        relations, ways, nodes = createJson.allNetworkGrand_Est()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))       


    # test for network Ile de France
    def test_allNetworkIle_de_France_ways(self):
        print("Test on Ile de France ways:")	
        relations, ways, nodes = createJson.allNetworkIle_de_France()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkIle_de_France_nodes(self):
        print("Test on Ile de France nodes:")	
        relations, ways, nodes = createJson.allNetworkIle_de_France()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkIle_de_France_route_tag(self):
        print("Test on Ile de France tags:")
        relations, ways, nodes = createJson.allNetworkIle_de_France()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))       


    # test for network Normandie
    def test_allNetworkNormandie_ways(self):
        print("Test on Normandie ways:")	
        relations, ways, nodes = createJson.allNetworkNormandie()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkNormandie_nodes(self):
        print("Test on Normandie nodes:")	
        relations, ways, nodes = createJson.allNetworkNormandie()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkNormandie_route_tag(self):
        print("Test on Normandie tags:")
        relations, ways, nodes = createJson.allNetworkNormandie()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertFalse(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))      


    # test for network Nouvelle Aquitaine
    def test_allNetworkNouvelle_Aquitaine_ways(self):
        print("Test on Nouvelle Aquitaine ways:")
        relations, ways, nodes = createJson.allNetworkNouvelle_Aquitaine()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkNouvelle_Aquitaine_nodes(self):
        print("Test on Nouvelle Aquitaine nodes:")
        relations, ways, nodes = createJson.allNetworkNouvelle_Aquitaine()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkNouvelle_Aquitaine_route_tag(self):
        print("Test on Nouvelle Aquitaine tags:")
        relations, ways, nodes = createJson.allNetworkNouvelle_Aquitaine()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))      


    # test for network Occitanie
    def test_allNetworkOccitanie_ways(self):
        print("Test on Occitanie ways:")
        relations, ways, nodes = createJson.allNetworkOccitanie()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkOccitanie_nodes(self):
        print("Test on Occitanie nodes:")
        relations, ways, nodes = createJson.allNetworkOccitanie()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkOccitanie_route_tag(self):
        print("Test on Occitanie tags:")
        relations, ways, nodes = createJson.allNetworkOccitanie()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))        


    # test for network Pays de la Loire
    def test_allNetworkPays_de_la_Loire_ways(self):
        print("Test on Pays de la Loire ways:")
        relations, ways, nodes = createJson.allNetworkPays_de_la_Loire()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkPays_de_la_Loire_nodes(self):
        print("Test on Pays de la Loire nodes:")
        relations, ways, nodes = createJson.allNetworkPays_de_la_Loire()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkPays_de_la_Loire_route_tag(self):
        print("Test on Pays de la Loire tags:")
        relations, ways, nodes = createJson.allNetworkPays_de_la_Loire()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertFalse(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))      


    # test for network Provence Alpes Cote Azur
    def test_allNetworkProvence_Alpes_Cote_Azur_ways(self):
        print("Test on Provence Alpes Cote Azur ways:")
        relations, ways, nodes = createJson.allNetworkProvence_Alpes_Cote_Azur()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_allNetworkProvence_Alpes_Cote_Azur_nodes(self):
        print("Test on Provence Alpes Cote Azur nodes:")
        relations, ways, nodes = createJson.allNetworkProvence_Alpes_Cote_Azur()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_allNetworkProvence_Alpes_Cote_Azur_route_tag(self):
        print("Test on Provence Alpes Cote Azur tags:")
        relations, ways, nodes = createJson.allNetworkProvence_Alpes_Cote_Azur()
        print("For the bus line "+ str(relations[0]['tags']["name"])+ " :")
        self.assertTrue(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))      
        

    # test for line 60
    def test_line_60_fromRATP_ways(self):
        print("Test the routes of the RATP bus 60:")
        relations, ways, nodes = createJson.line60_RATP()
        self.assertTrue(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_line_60_fromRATP(self):
        print("Test the RATP bus 60 nodes:")
        relations, ways, nodes = createJson.line60_RATP()
        self.assertTrue(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    def test_line_60_fromRATP_falseNodeOrder(self):
        print("Test the RATP false information nodes order:")
        relations, ways, nodes = createJson.line60_RATP_false()
        self.assertFalse(createJson.testErrorSummary(requete_bus.checkStopsOrder(relations[0], nodes, ways)))

    # test for line 60 with false information
    def test_line_60_fromRATP_falseWays(self):
        print("Test the RATP false information ways:")
        relations, ways, nodes = createJson.line60_RATP_false()
        self.assertFalse(createJson.testErrorSummary(requete_bus.continuousWays(relations[0], ways, nodes)))

    def test_line_60_fromRATP_falseTags(self):
        print("Test the RATP false information tags:")
        relations, ways, nodes = createJson.line60_RATP_false()
        self.assertFalse(createJson.testErrorSummary(tag_verification.check_route_tags(relations[0])))											

 # class main
if __name__ == '__main__':
    res = None 
    while res not in ["testUni", "test"]:
        res = input("Do you want to do unit tests or test yourself? (testUni/test)\n")
    if res == "testUni":
        print("Unit testing can take time, especially if you are testing for the first time.")
        print("The data must be processed throughout France, there is a lot of data to process.\n")
        unittest.main()
    else:
        # get the name of the bus line
        name_bus = input("Enter the name of the bus line you wanted to find: ")
        request = requeteOverpass.generate_request(name_bus)
        r = overpass.query(request)
        relations, ways, nodes = createJson.createTab(r.toJSON())
        
        operators = set()
        for relation in relations:
            operator = relation["tags"].get("operator", "inconnu")
            if operator not in operators:
                operators.add(operator)
                
        if len(operators) >= 2:
            # several bus lines found, show all operators		
            print("Several bus lines were found with the same name: {}".format(name_bus))
            print("Here are the operators found: {}".format(", ".join(operators)))
            operator = None
            while operator not in operators:
                operator = input("Please enter one of the operators above: ")
                if operator not in operators:
                    print("The operator entered is invalid. Try Again.")
            request = requeteOverpass.generate_request_withOperator(name_bus, operator)
            r = overpass.query(request)
            relations, ways, nodes = createJson.createTab(r.toJSON())	

        elif len(operators) <= 0:
            # no bus line found
            print("No bus line found with name {}".format(name_bus))


        if len(operators) >= 1:
            # create an ordered list of all nodes on the bus line
            all_nodes = []
            for way in ways:
                for node in way['nodes']:
                    all_nodes.append(node)

            # retrieve data from nodes
            node_data = []
            for node in nodes:
                node_data.append({
                    'type': 'node',
                    'id': node['id'],
                    'lat': node.get('lat', None),
                    'lon': node.get('lon', None),
                    'tags': node.get('tags', {})
                })

            # create a list of edges connecting the nodes of the line
            edge_data = []
            for i in range(len(all_nodes)-1):
                edge_data.append({'type': 'edge','id': f'edge_{i}','start_node': all_nodes[i],'end_node': all_nodes[i+1]})

            for i in relations:
                print("Verification of relation id "+str(i['id']))
                print("Verification continious way: ")
                createJson.testErrorSummary(requete_bus.continuousWays(i, ways, nodes))
                print("Verification check order node:")
                createJson.testErrorSummary(requete_bus.checkStopsOrder(i, nodes, ways))
                print("Verification tag route:")
                createJson.testErrorSummary(tag_verification.check_route_tags(i))

            #creates a map displaying the Open street map showing the desired bus line
            data = node_data + edge_data
            fig = px.scatter_mapbox(data, lat='lat', lon='lon', hover_name='id', hover_data=['type', 'tags'])
            fig.update_layout(mapbox_style="open-street-map")
            fig.write_html('Json/map.html')