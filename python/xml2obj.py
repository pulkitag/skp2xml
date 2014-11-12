import xml.etree.ElementTree as ET
from utils import *

def get_string(fileName):
	fid  = open(fileName,'r')
	text = '<root> ' + fid.read() + ' </root>'
	fid.close()
	return text

def parse_version(elm, objFid):
	objFid.write('#OBJ Model File\n')
	objFid.write('#Converted using xml2obj (c) Pulkit Agrawal 2014\n')
	if elm.attrib.has_key('units'):
		objFid.write('#Units %s \n' % eml.attrib['units'])

def parse_material(elm, mtlFid):
	mat = Material()
	if elm.attrib.has_key('Name'):
		mat.setName(elm.attrib['Name'])
	if elm.attrib.has_key('Color'):
		mat.setKd(elm.attrib['Color'])
	if elm.attrib.has_key('Alpha'):
		mat.setOpacity(True)
		mat.setAlpha(elm.attrib['Alpha'])

	for child in elm:
		if child.tag == 'Texture':
			if child.attrib.has_key('Path'):
				mat.setIsImage(True)
				mat.setImName(child.attrib['Path'])
			else:
				assert False
	
	mat.writeMaterial(mtlFid)

def parse_materials(elm, mtlFid):
	for child in elm:
		parse_material(child, mtlFid)

def parse_data(text, objFid, mtlFid):
	root = ET.fromstring(text)
	for child in root:
		if child.tag == 'SkpToXml':
			parse_version(child,objFid)
		elif child.tag == 'Layers':
			#Do Nothing
		elif child.tag == 'Materials':
			parse_materials(child, mtlFid)
		elif child.tag == 'Geometry':
			#parse_geometry(child, objFid)

def main(filename):
	data   = get_string(filename)
	objFid = open('tmp/myobj.obj','w')
	mtlFid = open('tmp/mymtl.mtl','w')
	parse_data(data, objFid, mtlFid)


