import requete_bus
import re

#check the if the mandatory tags exists
def check_mandatory_tags(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	tags1 = "type" in r['tags'] 
	tags4 = "route" in r['tags'] 
	tags5= "operator" in r['tags']
	tags2 = "network" in r['tags'] 
	tags6= "ref" in r['tags'] 
	tags7= "name" in r['tags'] 
	tags8= "public_transport:version" in r['tags']
	tags3 = "from" in r['tags'] 
	tags9= "to" in r['tags']
	if not tags3:
		errors.addError({"type":"missing from tag","id":str(r['id']),"suggestion":"add a from tag"})

	if not tags2:
			errors.addError({"type":"missing network tag","id":str(r['id']),"suggestion":"add a network tag"})
	if not tags5:
			errors.addError({"type":"missing operator tag","id":str(r['id']),"suggestion":"add a operator tag"})

	if not tags6:
			errors.addError({"type":"missing ref tag","id":str(r['id']),"suggestion":"add a ref tag"})
	if not tags7:
			errors.addError({"type":"missing public_transport:version tag","id":str(r['id']),"suggestion":"add a public_transport:version tag"})

	if not tags8:
			errors.addError({"type":"missing from tag","id":str(r['id']),"suggestion":"add a from tag"})

	if not tags9:
			errors.addError({"type":"missing to tag","id":str(r['id']),"suggestion":"add a to tag"})

	if not tags1:
		errors.addError({"type":"missing type tag","id":str(r['id']),"suggestion":"add a type tag with route value"})
	else:
		if r['tags']['type'] != "route" :
			errors.addError({"type":"incorrect type value","id":str(r['id']),"suggestion":"must  be route"})
        
	if not tags4 :
		errors.addError({"type":"missing route tag","id":str(r['id']),"suggestion":"add a route tag with bus value"})
	else:
		if r['tags']['route'] != "bus" :
			errors.addError({"type":"incorrect route value","id":str(r['id']),"suggestion":"must  be bus"})

	return errors

#check if public_transport:version tag has correct value
def check_transport_version(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if "public_transport:version" in r['tags']:
		if r['tags']['public_transport:version'] == '1' or r['tags']['public_transport:version'] == '2':
			return errors
		errors.addError({"type":"incorrect transport version","id":str(r['id']),"suggestion":"should be 1 or 2"})

	return errors

#if ref tag is not in relataion , name has to be in relation
def has_identifier(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if 'name' in r['tags'].keys() or 'ref' in r['tags'].keys():
		return errors
	errors.addError({"type":"missing identificatio","id":str(r['id']),"suggestion":"a route should have at ref or name tag in order to be identified"})

	return errors



#the format for interval and duration has to be in format H:MM:SS , HH:MM:SS ,HH:MM, H:MM , MM or M
def check_duration_format(d):
	errors = requete_bus.ErrorSummary(str(0))
	length = len(d)
	if length == 8:
		if d[0].isdigit() and d[1].isdigit() and d[2] ==':' and d[3].isdigit() and d[4].isdigit() and d[5] ==':' and d[6].isdigit() and d[7].isdigit():
			return errors

	elif length ==7:
		if d[0].isdigit() and d[1] ==':' and d[2].isdigit() and d[3].isdigit() and d[4] ==':' and d[5].isdigit() and d[6].isdigit():
			return errors

	elif length ==5:
		if d[0].isdigit() and d[1].isdigit() and d[2] ==':' and d[3].isdigit() and d[4].isdigit():
			return errors
	
	elif length ==4:
		if d[0].isdigit() and d[1] ==':' and d[2].isdigit() and d[3].isdigit():
			return errors
	
	elif length ==2:
		if d[0].isdigit() and d[1].isdigit():
			return errors
					

	elif length ==1:
		if d[0].isdigit():
			return errors
	errors.addError({"type":"incorrect duration format","id":str(r['id']),"suggestion":"please use a correct duration format"})

	return errors


def check_opening_hours(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if 'opening_hours' in r['tags']:
		day = "((Mo)|(Tu)|(We)|(Th)|(Fr)|(Sa)|(Su))"
		month = "((Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(Jul)|(Aug)|(Sep)|(Oct)|(Nov)|(Dec))"
		time = "(\d\d:\d\d)"
		time_interval= "("+time +"-"+time+")"
		day_interval_hours= day+"((-" + day+ ")|(," +day+ ")*) " +time_interval+ "(,"+time_interval+")*"
		#pattern= "("+day_interval_hours+",)"
		return False
	return True



#check call the format checking function for duration and inteval tags
def check_duration_and_interval(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if "duration" in r['tags']:
		errors.join(check_duration_format(r['tags']['duration']).errors)
			
	if "interval" in r['tags']:
		errors.join(check_duration_format(r['tags']['interval']).erros)
	return errors


#there must be a fee tag as yes
def check_fee_tag(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if "fee" in r['tags']:
		if r['tags']['fee'] =="yes":
			return errors
		elif r['tags']['fee']=="no":
			return errors
		errors.addError({"type":"incorrect fee value","id":str(r['id']),"suggestion":"fee value should be yes or no"})
	if not "fee" in r['tags'] and "charge" in r['tags']:
		errors.addError({"type":"incorrect no fee tag","id":str(r['id']),"suggestion":"if charge tags is present fee tag should be too"})
	return errors
	
	
#check if wheelchair tag has correct value
def check_wheelchair_tag(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if "wheelchair" in r['tags']:
		if r['tags']['wheelchair']=="yes" :
			return errors
		elif r['tags']['wheelchair']=="no" :
			return errors
		elif r['tags']['wheelchair']=="limited" :
			return errors
		errors.addError({"type":"incorrect wheelchair value","id":str(r['id']),"suggestion":"wheechair value should be yes,no or limited"})

	return errors


#check if bicycle tag has correct value
def check_bicycle_tag(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if "bicycle" in r['tags']:
		if r['tags']['bicycle']=="yes" :
			return errors
		elif r['tags']['bicycle']=="no" :
			return errors
		elif r['tags']['bicycle']=="permissive" :
			return errors
		errors.addError({"type":"incorrect bicycle value","id":str(r['id']),"suggestion":"bicycle value should be yes,no or permissive"})
	return errors


#check if relation tag 'name' has correct format
def check_name_format(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if 'name' in r['tags']:
		if bool(re.fullmatch("Bus .+: .+ (((=>)|(->)|(-->)|(→)) .+)+" ,r['tags']['name']))==False and 'public_transport:version' in r['tags'] and r['tags']['public_transport:version']=='2':
			errors.addError({"type":"incorrect name format","id":str(r['id']),"suggestion":"name must match the following format : Bus (ref): (start) (=> or -> or --> or →) (destination)"})
	return errors



#check if colour tag has a correct hex format
def check_colour_code(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if 'colour' in r['tags']:
		pattern ="\#(\d|([A-F]|[a-f]))(\d|([A-F]|[a-f]))(\d|([A-F]|[a-f]))(\d|([A-F]|[a-f]))(\d|([A-F]|[a-f]))(\d|([A-F]|[a-f]))"
		if bool(re.fullmatch(pattern, r['tags']['colour']))==False:
			errors.addError({"type":"incorrect color value","id":str(r['id']),"suggestion":"colour should be in hex format"})

	return errors



#check if roundtrip tag has correct value
def check_roundtrip_tag(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if "roundtrip" in r['tags']:
		if r['tags']['roundtrip']=="yes" :
			return errors
		elif r['tags']['roundtrip']=="no" :
			return errors
		errors.addError({"type":"incorrect roundtrip value","id":str(r['id']),"suggestion":"change roundtrip value must be yes or no"})
	return errors


#check if way in member of relation has a valid role
def check_way_role(w):
	errors = requete_bus.ErrorSummary(str(w['ref']))
	if w['role']=='' or w['role']=="route" or w['role']=="foward" or w['role']=="backward" or w['role']=="hail_and_ride":
		return errors
	elif w['role']=="platform" or w['role']=="platform_exit_only" or w['role']=="platform_entry_only":
		return errors
	errors.addError({"type":"incorrect role value","id":str(w['ref']),"suggestion":"change role value to \"\",foward,backward,platform,platform_exit_only or platform_entry_only if it is one else delete it"})

	return erros



#check if node in member of relation has a valid role
def check_node_role(n):
	errors = requete_bus.ErrorSummary(str(n['ref']))
	if n['role']=="stop" or n['role']=="stop_exit_only" or n['role']=="stop_entry_only":
		return errors
	elif n['role']=="platform" or n['role']=="platform_exit_only" or n['role']=="platform_entry_only":
		return errors
	errors.addError({"type":"incorrect role value","id":str(n['ref']),"suggestion":"change role value to stop,stop_exit_only,stop_entry_only,platform,platform_exit_only,platform_entry_only if it is one else delete it"})
	return errors


#check role of members in a relation
def check_members_role(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	for elem in r['members']:
		if elem['type'] == 'way':
			errors.join(check_way_role(elem).errors)
		elif elem['type'] == 'node':
			errors.join(check_node_role(elem).errors)
	return errors


#call all functions to check a relation tags
def check_route_tags(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	errors.join(check_mandatory_tags(r).errors)
	errors.join(check_wheelchair_tag(r).errors)
	errors.join(check_bicycle_tag(r).errors)
	errors.join(check_roundtrip_tag(r).errors)
	errors.join(check_fee_tag(r).errors)
	errors.join(check_duration_and_interval(r).errors)
	errors.join(has_identifier(r).errors)
	errors.join(check_transport_version(r).errors)
	errors.join(check_name_format(r).errors)
	errors.join(check_colour_code(r).errors)
	return errors


def check_mandatory_route_master(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	tags1 = 'type' in r['tags'] and 'route_master' in r['tags']
	tags2 = 'operator' in r['tags'] and 'network' in r['tags']
	tags3 = 'ref' in r['tags'] and 'name' in r['tags']
	if 'type' in r['tags'] and 'route_master' in r['tags']:
		if r['tags']['type'] != 'route_master':
			errors.addError({"type":"incorrect type value","id":str(r['id']),"suggestion":"change type to route_master"})
		if r['tags']['route_master'] != 'bus':
			errors.addError({"type":"incorrect route value","id":str(r['id']),"suggestion":"change route to bus"})
		
		if not ('ref' in r['tags'] or 'official_name' in r['tags']):
			errors.addError({"type":"no identifiers","id":str(r['id']),"suggestion":"add a ref or an official_name to the route master"})
	errors.addError({"type":"missing tags","id":str(r['id']),"suggestion":"tags type and route_master must be in the route master tags"})
	return errors



def check_name_route_master(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if 'name' in r['tags']:
		pattern = "Bus .*"
		if bool(re.fullmatch(pattern, r['tags']['name'])) == False:
			errors.addError({"type":"incorrect name format","id":str(r['id']),"suggestion":"change the route name in correct format"})
	return errors

def check_tourism_tag(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if 'tourism' in r['tags']:
		if not (r['tags']['tourism']=='yes' or r['tags']['tourism']=='only'):
			errors.addError({"type":"incorrect value in tag tourism","id":str(r['id']),"suggestion":"value should be yes or only"})
	return errors

def check_school_tag(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	if 'school' in r['tags']:
		if not (r['tags']['school']=='yes' or r['tags']['school']=='only'):
			errors.addError({"type":"incorrect value in tag school","id":str(r['id']),"suggestion":"value should be yes or only"}) 
	return errors


def check_route_master_tags(r):
	errors = requete_bus.ErrorSummary(str(r['id']))
	errors.join(check_mandatory_route_master(r).errors)
	errors.join(check_name_route_master(r).errors)
	errors.join(check_wheelchair_tag(r).errors)
	errors.join(check_bicycle_tag(r).errors)
	errors.join(check_colour_code(r).errors)
	errors.join(check_tourism_tag(r).errors)
	errors.join(check_school_tag(r).errors)
	errors.join(check_duration_and_interval(r).errors)
		
	return errors