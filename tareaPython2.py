import base64
import requests
import json
import collections
import struct
import BaseHTTPServer

def tarea1(origen, destino):
	origen = request.json["origen"]
	destino = request.json["destino"]
	agmh = "https://maps.googleapis.com/maps/api/directions/json?origin="+origen+"&destination="+destino+"&key=AIzaSyDcONfTyjtc5vBc4xoIMKOVtDPYA5VXkjk"
	agmhRes = requests.post(agmh, None)
	agmhRes2 = json.loads(agmhRes.text)
	desCol = collections.defaultdict(list)
	sl = agmhRes["routes"][0]["legs"][0]["start_location"]
	desCol["ruta"].append({"lat": sl["lat"], "lng": sl["lng"]})
	ubica = agmhRes["routes"][0]["legs"][0]["steps"]
    	for desti in ubica:
		lat = desti["end_location"]["lat"]
		lng = desti["end_location"]["lng"]
		desCol["ruta"].append({"lat": lat, "lng": lng})
	return json.dumps(desCol, indent=3)

def tarea2(origin):
	origen = request.json["origen"]
	agmh = "https://maps.googleapis.com/maps/api/geocode/json?address=(origen)&key=AIzaSyDXvf09KDyp0cTk5nroClhViAJBa2fwVRk"
	agmhRes = requests.post(coord_url.replace("(origen)", origin, 1), None)
	myJson = json.loads(agmhRes.text)
	if myJson["status"] != "OK":
		return -1
	newAGMH = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=lat,lng&radius=500&type=restaurant&key=AIzaSyDXvf09KDyp0cTk5nroClhViAJBa2fwVRk"
	lat = myJson["results"][0]["geometry"]["location"]["lat"]
	lng = myJson["results"][0]["geometry"]["location"]["lng"]
	print "Lat %s, Lng: %s" % (lat, lng)
	newAGMH = newAGMH.replace("lat", str(lat), 1)
	newAGMH = newAGMH.replace("lng", str(lng), 1)
	agmhRes = requests.post(newAGMH, None)
	myJson = json.loads(agmhRes.text)
	if myJson["status"] != "OK":
		return -1
	myJson = myJson["results"]
	ubi = collections.defaultdict(list)
	for nUBI in myJson:
		lat = nUBI["geometry"]["location"]["lat"]
		lng = nUBI["geometry"]["location"]["lng"]
		name = nUBI["name"]
		ubi["restaurantes"].append({"nombre":name,"lat":lat,"lon":lng})
	return json.dumps(ubi)

def tarea3(data):
    arreglo = data.decode('base64')
    ancho = struct.unpack('<%dH' % 2, arreglo[18:22])[0]
    altura = struct.unpack('<%dH' % 2, arreglo[22:26])[0]
    agmh = struct.unpack('<%dH' % 1, arreglo[28:30])[0]
    byteIn = struct.unpack('<%dH' % 2, arreglo[10:14])[0]
    print "Len %s\t|\tWidth %s\t|\tHeight %s\t|\tBPP %s\t|\tOffset %s" % (len(arreglo), ancho, altura, agmh, byteIn)
    saigo = bytearray(arreglo[:byteIn])
    i = 0
    if byteIn == 32:
        for pixel in arreglo[byteIn::4]:
            if i+byteIn+3 < len(arr):
                red = struct.unpack('B', arreglo[i+byteIn+1])[0]
                green = struct.unpack('B', arreglo[i+byteIn+2])[0]
                blue = struct.unpack('B', arreglo[i+byteIn+3])[0]
                grisSca = (red + green + blue) / 3
                saigo.append(b'\xFF')
                saigo.append(grisSca)
                saigo.append(grisSca)
                saigo.append(grisSca)
                i += 4
    elif byteIn == 24:
        for pixel in arreglo[byteIn::3]:
            if i+byteIn+2 < len(arreglo):
                red = struct.unpack('B', arreglo[i+byteIn])[0]
                green = struct.unpack('B', arreglo[i+byteIn+1])[0]
                blue = struct.unpack('B', arreglo[i+byteIn+2])[0]
                grisSca = (red + green + blue) / 3
                saigo.append(grisSca)
                saigo.append(grisSca)
                saigo.append(grisSca)
                i += 3
    else:
        return -1

return base64.b64encode(saigo)

def tarea4():
	if not request.json or not "data" in request.json:
		abort(400)
	else
		data = request.json["data"]
		name = request.json["nombre"]
		size = request.json["tamano"]
		dataS = shrink(data, size["alto"], size["ancho"])
		while(dataS["redo"] == True)
			dataS = shrink(dataS["data"], size["alto"], size["ancho"])
		image = ("nombre": name
				"data": dataS["data"])
	return jsonify(image).200

def shrink(imageD, wantL, wantA)
	decoImage = base64.standard_b64decode(imageD)
	wantA = int.from_bytes(decoImage[0x12:0x16], byteorder="little", signed=False)
	wantL = int.from_bytes(decoImage[0x10:0x14], byteorder="little", signed=False)
	pixImg = int.from_bytes(decoImage[0x14:0x16], byteorder="little", signed=False)
	decodeI = bytearray()

	cutA = wantA
	cutB = wantL
	cutA = 0
	cutB = 0
"""
	agmh = request.json["name"]
	digi = request.json["data"]
	ancho = request.json["tamanio"]["ancho"]
	altura = request.json["tamanio"]["largo"]
    
	arreglo = base64.standard_b64decode(digi)
    	anc = int.from_bytes(arreglo[0x12:0x16], byteorder="little", signed=False)
	lar = int.from_bytes(arreglo[0x16:0x19], byteorder="little", signed=False)
	mete32 = arreglo[0x1C]
	print(anc, lar, mete32)
return ""
"""

class Server(BaseHTTPServer.BaseHTTPRequestHandler):
def do_POST(save):
        newLen = int(save.headers.getheader('content-length', 0))
        pb = json.loads(save.rfile.read(newLen))
        if save.path == "/tarea1":
            try:
                agmh = tarea1(pb["origen"], pb["destino"])
            except Exception, err:
                print err
                save.send_response(400)
                save.send_header("Content-type", "application/json")
                save.end_headers()
                save.wfile.write("{\"error\":\"No ha especificado el origen\"}")
                return
            if agmh == -1:
                save.send_response(500)
                save.send_header("Content-type", "application/json")
                save.end_headers()
                save.wfile.write("{\"error\":\"Direccion erronea\"}")
            else:
                save.send_response(200)
                save.send_header("Content-type", "application/json")
                save.end_headers()
                save.wfile.write(r)
        elif save.path == "/tarea2":
            try:
                agmh = tarea2(pb["origen"])
            except Exception, err:
                print err
                save.send_response(400)
                save.send_header("Content-type", "application/json")
                save.end_headers()
                save.wfile.write("{\"error\":\"No ha especificado el origen\"}")
                return
            if agmh == -1:
                save.send_response(500)
                save.send_header("Content-type", "application/json")
                save.end_headers()
                save.wfile.write("{\"error\":\"Direccion erronea\"}")
            else:
                save.send_response(200)
                save.send_header("Content-type", "application/json")
                save.end_headers()
                save.wfile.write(r)
        elif save.path == "/tarea3":
            try:
                agmh = tarea3(pb["data"])
                name = pb["nombre"]
            except Exception, err:
                print err
                save.send_response(400)
                save.send_header("Content-type", "application/json")
                save.end_headers()
                save.wfile.write("{\"error\":\"No ha especificado el origen\"}")
                return
            if agmh == -1:
                save.send_response(500)
                save.send_header("Content-type", "application/json")
                save.end_headers()
                save.wfile.write("{\"error\":\"No es posible modificarlo\"}")
            else:
                save.send_response(200)
                save.send_header("Content-type", "application/json")
                save.end_headers()
                data = collections.defaultdict(list)
                data["nombre"] = name.replace(".bmp", "(blanco y negro).bmp", 1)
                data["data"] = agmh
                save.wfile.write(json.dumps(data))
        else:
            save.send_response(500)
            save.send_header("Content-type", "application/json")
            save.end_headers()
            save.wfile.write("{}")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(("localhost", 8080), Server)
    print "Server Started"
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print "Server Stopped"
