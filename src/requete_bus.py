import json
import re
from math import sin,cos,sqrt,radians,atan2
from OSMPythonTools.overpass import Overpass
overpass = Overpass()

def getNodesFromRelation(r):
	nodes=[]
	for e in r['members']:
		if(e['type']=='node'):
			nodes.append(e)
	return nodes

def getWaysFromRelation(r):
	ways=[]
	for e in r['members']:
		if(e['type']=='way'):
			ways.append(e)
	return ways

def getRoadsFromRelation(r):
	ways=[]
	for e in r['members']:
		if(e['type']=='way' and e['role']!='platform' and e['role']!='platform_exit_only' and e['role']!='platform_entry_only'):
			ways.append(e)
	return ways


#return a way's informations in a request
def seekWay(list,target):
	for e in list:
		if(target['ref']==e['id']):
			return e
	return None


#return a node's informations in a request
def seekNode(list,target):
	for e in list:
		if(target['ref']==e['id']):
			return e
	return null

#return a node information by its id, used to get lon and lat of a node by its id in relation
def seekNodeById(list,id):
	for e in list:
		if(str(id)==str(e['id'])):
			return e
	return None

#return a node's longitude and latitude
def seekNodeCoord(list,target):
	for e in list:
		if target == e['id']:
			return [e['lat'],e['lon']]
	return


#send the request into parameter to OSM with the overpass API
def requete_OSM(request):
	overpass = Overpass()
	query= request
	result= overpass.query(query, timeout=1000)
	json = result.toJSON()
	return json


#error class to summarise all erros found in a route
#errors has type of error,the id of the element where it was detected,a suggestion to fix the issue
class ErrorSummary:
	def __init__(self,relation):
		self.relation = relation
		self.errors = []

	def addError(self, e):
		self.errors.append(e)
	
	def __str__(self):
		res = "error summary for route:"+str(self.relation)+"\n"
		if len(self.errors)==0:
			return res+"nothing to report"
		else:
			for e in self.errors:
				res+= e["type"]+" at "+str(e["id"])+" :"+e["suggestion"]+"\n"
		return res

	def getRelation(self):
		return self.relation
	
	def getErrors(self):
		return self.errors

	def join(self,l):
		if len(l)>0:
			for e in l:
				self.errors.append(e)

#attempt to suggestion a solution when way members of a route are not continuous 
def continuousWaysSuggestion(r,ways,w,node_data):
	errors = ErrorSummary(str(r['id']))
	continuous_attempt = correctRouteExists(ways,w)
	if continuous_attempt[0]==-1 :
		#TODO :
		errors.addError({"type":"way continuation error","id":str(r['id']),"suggestion":"the ways are not continuous there may have missing ways to route,please find them and add them"})
	else:
		normal = "["
		#if route is circular we suggestion a continuation of ways, first way may not be the starting point
		if "from" in r['tags'] and "to" in r['tags']:
			if r['tags']['from'] == r['tags']['to']:
				for e in range(0,len(continuous_attempt)):
					normal += str(e[0]['id'])
					if(i<len(continuous_attempt)-1):
						normal+=","
				normal+="]"
				errors.addError({"type":"way continuation error","id":str(r['id']),"suggestion":"some ways may be swaped , correct order may be :"+normal})
			
		else:#case for regular route
			nodes= getNodesFromRelation(r)
			#if role of first node is a stop we check if it is from first or last way to determine if order is reversed
			if(nodes[0]['role'] == 'stop' or nodes[0]['role'] =='stop_exit_only' or nodes[0]['role'] =='stop_entry_only' ):
				if nodes[0] in continuous_attempt[0]:
					for e in range(0,len(continuous_attempt)):
						normal += str(continuous_attempt[e][0]['id'])
						if(i<len(continuous_attempt)-1):
							normal+=","
						normal+="]"
					errors.addError({"type":"way continuation error","id":str(r['id']),"suggestion":"some ways may be swaped , correct order may be :"+normal})
				if nodes[0] in continuous_attempt[-1]:
					for e in range(0,len(continuous_attempt)):
						normal += str(continuous_attempt[len(continuous_attempt)-1-e][0]['id'])
						if(i<len(continuous_attempt)-1):
							normal+=","
						normal+="]"
					errors.addError({"type":"way continuation error","id":str(r['id']),"suggestion":"some ways may be swaped , correct order may be :"+normal})
			#if role of first node is a platform we check if it is near first or last way to determine if order is reversed
			elif(nodes[0]['role'] == 'platform' or nodes[0]['role'] =='platform_exit_only' or nodes[0]['role'] =='platform_entry_only' ):
				near_first =False
				near_last =False
				for n in continuous_attempt[0][0]['nodes']:
					req =requete_OSM("(node("+ str(n['id'])+");out body;>;out skel qt;")["elements"][0]
					if len(areNear(seekNode(node_data,(nodes[0]['ref'])),req).getErrors())==0:
						near_first = True
				for n in continuous_attempt[-1][0]['nodes']:
					req =requete_OSM("(node("+ str(n['id'])+");out body;>;out skel qt;")["elements"][0]
					if len(areNear(seekNode(node_data,(nodes[0]['ref'])),req).getErrors())==0:
						near_last = True
				if near_first and not near_last :
					for e in range(0,len(continuous_attempt)):
						normal += str(continuous_attempt[e][0]['id'])
						if(i<len(continuous_attempt)-1):
							normal+=","
						normal+="]"
					errors.addError({"type":"way continuation error","id":str(r['id']),"suggestion":"some ways may be swaped , correct order may be :"+normal})
				elif not near_first and  near_last :
					for e in range(0,len(continuous_attempt)):
						normal += str(continuous_attempt[len(continuous_attempt)-1-e][0]['id'])
						if(i<len(continuous_attempt)-1):
							normal+=","
						normal+="]"
					errors.addError({"type":"way continuation error","id":str(r['id']),"suggestion":"some ways may be swaped , correct order may be :"+normal})
			else :
				for e in range(0,len(continuous_attempt)):
					normal += str(continuous_attempt[e][0]['id'])
					if(i<len(continuous_attempt)-1):
						normal+=","
					normal+="]"
				reverse ="["
				for e in range(0,len(continuous_attempt)):
					reverse += str(continuous_attempt[len(continuous_attempt)-1-e][0]['id'])
					if(i<len(continuous_attempt)-1):
						reverse+=","
					reverse+="]"
				errors.addError({"type":"way continuation error","id":str(r['id']),"suggestion":"some ways may be swaped , correct order may be :"+normal +" or "+reverse})	
	return errors.getErrors()





#Verifie la continuité d'une suite de Way
def continuousWays(r,w,node_data):
    errors = ErrorSummary(str(r['id']))
    ways= getRoadsFromRelation(r)
    direction=True
    j=0
    for i in range(0,len(ways)-1):
        way1 = seekWay(w,ways[i])['nodes']
        way2 =  seekWay(w,ways[i+1])['nodes']
        if i==0:
            if way1[-1] == way2[0]:
                direction=True
            elif way1[-1] ==  way2[-1]:
                direction=False
            elif way1[0] == way2[0]:
                direction=True
            elif way1[0] == way2[-1]:
                direction=False
            else:
                errors.join(continuousWaysSuggestion(r,ways,w,node_data))
                return errors
            break
        else :
            match direction:
                case True: 
                    if way1[-1] == way2[0]:
                        direction=True
                    elif way1[-1] ==  way2[-1]:
                        direction=False
                    else:
                        errors.join(continuousWaysSuggestion(r,ways,w,node_data))
                        return errors
                    break
                case False:
                    if way1[0] == way2[0]:
                        direction=True
                    elif way1[0] == way2[-1]:
                        direction=False
                    else:
                        errors.join(continuousWaysSuggestion(r,ways,w,node_data))
                        return errors
                    break
	
    return errors

#return an array of a continuous route made of way in ways
#if none exists returns [-1]
def correctRouteExists(ways,way_data):
	remaining_ways = ways
	order =[]
	for i in range(0,len(remaining_ways)):
		#first iteration
		if len(order)==0:
			order.append((seekWay(way_data,remaining_ways[i]),False))
		else:
			
			for j in range(0,len(remaining_ways)):
				newWay = seekWay(way_data,remaining_ways[j])
		
				#regular case add to start or end of order
				if order[-1][1]==False:
					if order[0][0]['nodes'][-1] ==newWay['nodes'][0]:
						order.append((newWay,False))
						remaining_ways.pop(j)
						break
					elif  order[-1][0]['nodes'][-1] ==newWay['nodes'][-1]:
						order.append((newWay,True))
						remaining_ways.pop(j)
						break
				else:
					if order[-1][0]['nodes'][0] ==newWay['nodes'][-1]:
						order.append((newWay,False))
						remaining_ways.pop(j)
						break
					elif order[-1][0]['nodes'][0] ==newWay['nodes'][0]:
						order.append((newWay,True))
						remaining_ways.pop(j)
						break
				if order[0][1]==False:
					if order[0][0]['nodes'][0] ==newWay['nodes'][-1]:
						order.append((newWay,False))
						remaining_ways.pop(j)
						break
					elif  order[0][0]['nodes'][0] ==newWay['nodes'][0]:
						order.append((newWay,True))
						remaining_ways.pop(j)
						break
				else:
					if order[0][0]['nodes'][-1] ==newWay['nodes'][-1]:
						order.append((newWay,False))
						remaining_ways.pop(j)
						break
					elif order[-1][0]['nodes'][-1] ==newWay['nodes'][0]:
						order.append((newWay,True))
						remaining_ways.pop(j)
						break
	if len(remaining_ways) >0:
		return [-1]
	else:
		return order

#source : https://www.geeksforgeeks.org/minimum-distance-from-a-point-to-the-line-segment-using-vectors/

# Function to return the minimum distance
# between a line segment AB and a point E
def minDistance(A, B, platform) :
	reqAns = 9999999999999
	for E in platform:
		# vector AB
		AB = [None, None]
		AB[0] = B['lat'] - A['lat']
		AB[1] = B['lon'] - A['lon']
	
		# vector BP
		BE = [None, None]
		BE[0] = E['lat'] - B['lat']
		BE[1] = E['lon'] - B['lon']
	
		# vector AP
		AE = [None, None]
		AE[0] = E['lat'] - A['lat']
		AE[1] = E['lon'] - A['lon']
	
		# Variables to store dot product
	
		# Calculating the dot product
		AB_BE = AB[0] * BE[0] + AB[1] * BE[1]
		AB_AE = AB[0] * AE[0] + AB[1] * AE[1]
	
		# Minimum distance from
		# point E to the line segment
		
	
		# Case 1
		if (AB_BE > 0) :
	
			# Finding the magnitude
			y = E['lon'] - B['lon']
			x = E['lat'] - B['lat']
			reqAns = min(reqAns,sqrt(x * x + y * y))
	
		# Case 2
		elif (AB_AE < 0) :
			y = E['lon'] - A['lon']
			x = E['lat'] - A['lat']
			reqAns = min(reqAns,sqrt(x * x + y * y))
	
		# Case 3
		else:
	
			# Finding the perpendicular distance
			x1 = AB[0]
			y1 = AB[1]
			x2 = AE[0]
			y2 = AE[1]
			mod = sqrt(x1 * x1 + y1 * y1)
			reqAns = min(reqAns,abs(x1 * y2 - y1 * x2) / mod)
	#print(reqAns)
	return reqAns < 0.0005


#check if to points are near each other (distance <= 5 meters)
def areNear(node1,node2):
	
	dlon = radians(node1['lon'])-radians(node2['lon'])
	dlat =radians(node1['lat'])-radians(node2['lat'])

	a = sin(dlat/2)**2 + cos(radians(node1['lat']))*cos(radians(node2['lat'])) * sin(dlon/2)**2
	c = 2*atan2(sqrt(a),sqrt(1-a))
	dist = 6371000 * c
	return dist <= 5

#check if at least one point from a list is at most 5 meters awway from node2
def oneIsNear(list,node2):
	for node1 in list:
		dlon = radians(node1['lon'])-radians(node2['lon'])
		dlat =radians(node1['lat'])-radians(node2['lat'])

		a = sin(dlat/2)**2 + cos(radians(node1['lat']))*cos(radians(node2['lat'])) * sin(dlon/2)**2
		c = 2*atan2(sqrt(a),sqrt(1-a))
		dist = 6371000 * c
		if dist <= 5:
			return True
	return False

def isSorted(tab):
	for i in range(0,len(tab)-1):
		if tab[i] > tab[i+1]:
			return False
	return True

#store all the road's node from a relation in form of an Array of Arrays of nodes.
#each index has all ids of all nodes for a way element
def organizeWaysNodes(nodes_data,ways_data,r):
	res = []
	it = 0
	for w in range(0,len(r['members'])):
		if r['members'][w]['type']=='way'and r['members'][w]['role']!='platform' and r['members'][w]['role']!='platform_exit_only' and r['members'][w]['role']!='platform_entry_only':
			res.append([])
			for n in seekWay(ways_data,r['members'][w])['nodes']:
				res[it].append(n)
			it+=1	
	return res

#checks if node order is consistent 2 times:
#	once with stop and platform nodes, avoid asking and checking hundreds of nodess
#	twice with all nodes from the ways of the route
def checkStopsOrder(r,node_data,way_data):
	errors = ErrorSummary(r['id'])
	nodes =getNodesFromRelation(r)
	platforms=[]
	stops=[]
    
	for i in nodes:
		if i['role'] == 'stop' or i['role'] =='stop_exit_only' or i['role'] =='stop_entry_only' :
			stops.append(seekNode(node_data,i))
	for i in range(0,len(r['members'])):
		if r['members'][i]['role'] == 'platform' or r['members'][i]['role'] =='platform_exit_only' or r['members'][i]['role'] =='platform_entry_only':
			platforms.append([])
			#case platform is a node
			if r['members'][i]['type']=='node':
				platforms[-1].append(seekNode(node_data,r['members'][i]))
			#case platorm is an area
			elif r['members'][i]['type']=='way':
				requete = "("
				for j in seekWay(way_data,r['members'][i])['nodes']:
					#requete des noeuds
					
					requete += "node("+str(j)+");"
				requete+=");out body;>;out skel qt;"
				res =requete_OSM(requete)["elements"]
				for j in res:
					platforms[-1].append(j)

			#case when area is a relation
			elif r['members'][i]['type']=='relation':
				requete = "("
				for j in r['members'][i]['members']:
					#request way to get its nodes id
					requete += "way("+str(j['ref'])+");"
				requete+=");out body;>;out skel qt;"
				res =requete_OSM(requete)["elements"]
				requete = "("
				for j in res:
					for node in j:
						requete += "node("+str(node)+");"
				requete+=");out body;>;out skel qt;"
				res =requete_OSM(requete)["elements"]
				for j in res:
					platorm[-1].append(j)



	result = [-1]*len(platforms) #contient les indices des point de la route proche de chaque stop 
	current = 0



	for i in range(0,len(platforms)):
		
		plat = platforms[i]
		
		for j in range(0,len(stops)):
			sto = stops[j]
			if oneIsNear(plat,sto) and j < current:
				result[i] = j
			elif oneIsNear(plat,sto) and j >= current:
				result[i] = j
				current = j
				break
	
	if isSorted(result) and (-1 not in result):
		return errors
	elif -1 not in result:
		order = []
		for i in range(0,len(result)):
			smallest = -1
			for j in range(0,len(result)):
				if result[j] >= smallest:
					smallest = j
			order.append(result.pop(smallest))
		platform_order = "[]"
		for i in range(0,len(order)):
			platform_order+=str(platforms[order[i]]['id'])
			if i< len(order)-1:
				platform_order+=";"
		platform_order+="]"
		errors.addError({"type":"platform too far from road","id":str(platforms[i]["id"]),"suggestion":"platforms order is not correct, correct order may be"+platform_order})
		return errors
	else:
		
		nodes = organizeWaysNodes(node_data,way_data,r)
		requete = "("
		for i in nodes:
			for j in i:
				requete += "node("+str(j)+");"
		requete+=");out body;>;out skel qt;"
		road_data = requete_OSM(requete)["elements"]



		result = [-1]*len(platforms)

		current = 0
		found =False
		for i in range(0,len(platforms)):
			plat = platforms[i]
			for j in range(0,len(nodes)):
				if found and j>0:
					break
				found = False
				nod = nodes[j]
				for n in range(0,len(nod)-1):
					n_data1 =seekNodeById(road_data,nod[n])
					n_data2 =seekNodeById(road_data,nod[n+1])
					
					if(n_data1 != None and n_data2 !=None):

						if (oneIsNear(plat,n_data1) or oneIsNear(plat,n_data1) or minDistance(n_data1,n_data2,plat)) and j < current:
							result[i] = j
						elif (oneIsNear(plat,n_data1) or oneIsNear(plat,n_data1) or minDistance(n_data1,n_data2,plat)) and j >= current:
							result[i] = j
							current = j
							found = True
							break

							
		if isSorted(result) and (-1 not in result):
			return errors
		elif -1  in result:
			for i in range(0,len(result)):
				if i==0 and result[i] == -1:
					string_ids =""
					for ids in platforms[i]:
						string_ids+=" "+str(ids["id"])
					errors.addError({"type":"starting platform too far from road","id":string_ids,"suggestion":"either firt ways are missing or platform is too far please correct it"})
				elif i==0 and result[i] == -1:
					string_ids =""
					for ids in platforms[i]:
						string_ids+=" "+str(ids["id"])
					errors.addError({"type":"ending platform too far from road","id":string_ids,"suggestion":"either last ways are missing or platform is too far please correct it"})
				elif result[i] == -1:
					string_ids =""
					for ids in platforms[i]:
						string_ids+=" "+str(ids["id"])

					errors.addError({"type":"platform too far from road","id":string_ids,"suggestion":"relocate the platform node closer to the road"})
			return errors
		else:
			
			order = []
			for i in range(0,len(result)):
				smallest = -1
				for j in range(0,len(result)):
					if result[j] >= smallest:
						smallest = j
				order.append(result.pop(smallest))
			platform_order = "["
			for i in range(0,len(order)):
				platform_order+=str(platforms[i][0]['id'])
				if i< len(order)-1:
					platform_order+=";"
			platform_order+="]"
			string_ids =""
			for ids in platforms[i]:
				string_ids+=" "+str(ids["id"])
			errors.addError({"type":"platform too far from road","id":string_ids,"suggestion":"platforms order is not correct, correct order may be"+platform_order})

			return errors


#return an Array of all nodes informations from a request, contains : id , lon and lat information 
def extract_nodes_data(elements):
	nodes=[]
	for i in elem:
		if i['type']=='node':
				nodes.append(i)
	return nodes

#return an Array of all nodes informations from a request, contains : way id plus all it's nodes id
def extract_ways_data(elements):
	ways=[]
	for i in elem:
		if(i['type']=='way'):
				ways.append(i)
	return ways

#return an Array of all relations from a request
def extract_relations_data(elements):
	relations=[]
	for i in elem:
		if(i['type']=='relation'):
				relations.append(i)
	return relations

#return an Array of way corresponding to the route, separates the bus platforms from the roads
def request_route_nodes(relation,way_data):
	id=[]
	for w in relation['members']:
		if w['type']=='way':
			way =seekWay(way_data,w)
			for n in way['nodes']:
				id.append(n)
	request = "("
	for i in id:
		request+="node("+str(i)+");"
	request+=");out body;>;out skel qt;"
	res =requete_OSM(request)['elements']
	return res

#main function to test an bus line integrity
def check_line(request):
	json = requete_OSM(request)
	elements = json['elements']
	nodes_data = extract_nodes_data(elements)
	ways_data = extract_ways_data(elements)
	relations = extract_relations_data(elements)
	errors = []
	for r in relations:
		r_error = continuousWays(r,ways_data,nodes_data)
		r_error.join(check_members_role(r).errors)
		#if the ways order is not coherent we can not use them to find a coherent node order
		if(len(r_error.errors) <=0):
			r_error.join(checkStopsOrder(r,nodes_data,ways_data).errors)
		r_error.join(check_route_tags(r).errors)
		errors.append(r_error)
	return errors
