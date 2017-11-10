from pymongo import MongoClient
import mapping
client = MongoClient()
db = client.transit

def connecttodb():
	db = db
	return db

def get_relations(line_no):
	ret = []
	for relation in db.mpkrelations.find({ 'line_number' : str(line_no) }):
		ret.append(relation['stop_list'])
	return ret

def getall_relations():
	ret = []
	for relation in db.mpkrelations.find():
		ret.append(relation['stop_list'])
	return ret

def set_segmentdefiniton(data):
	retobj = db.mpksegmentdefinitions.insert_one(data)
	return retobj

def build_segmentdefition(G, a, b, c, na, nb, path, length ):
	geojson = mapping.build_LineString(G, path)
	data = { "stop_a": a, "stop_b" : b, "stop_c" : c, "node_a" : na, "node_b" : nb, "path" : path, "geojson" : geojson, "length" : length }

