import xml.etree.ElementTree as ET
from utils import *

def get_string(fileName):
    fid  = open(fileName,'r')
    text = '<root> ' + fid.read() + ' </root>'
    fid.close()
    return text


class Xml2Obj:
    def __init__(self, objFid, mtlFid):
        self.objFid_ = objFid
        self.mtlFid_ = mtlFid
        self.vertices_    = Store('v')
        self.normals_     = Store('vn')
        self.uvcoords_    = Store('vt')
        self.default_matname_ = 'SKP2XML_DEFAULT'
        self.num_faces_ = 0


    def parse_version(self, elm):
        self.objFid_.write('#OBJ Model File\n')
        self.objFid_.write('#Converted using xml2obj (c) Pulkit Agrawal 2014\n')
        if elm.attrib.has_key('units'):
                self.objFid_.write('#Units %s \n' % elm.attrib['units'])
        self.objFid_.write('\n')
        self.objFid_.write('mtllib \t mymtl.mtl \n \n')

    
    def add_default_material(self):
        mat = Material()
        mat.setName(self.default_matname_)
        mat.writeMaterial(self.mtlFid_)
        

    def parse_material(self, elm):
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
        mat.writeMaterial(self.mtlFid_)


    def parse_materials(self, elm):
        for child in elm:
            self.parse_material(child)



    def write_triangle(self, tri):
        ''' 
            Write a single triangle 
            It is assumed that the triangle has only 3 children, i.e. vertices
        '''
        
        vIdx = []
        nIdx = []
        tIdx = []
        #print len(tri)
        for child in tri:
            if child.tag == 'Vertex':
                for v in child:
                    if v.tag == 'Point':
                        pt = Point3d(float(v.attrib['x']), float(v.attrib['y']), float(v.attrib['z']))
                        vIdx.append(self.vertices_.append_and_write(pt, self.objFid_))
                        #pt.display()
                    if v.tag == 'Normal':
                        pt = Point3d(float(v.attrib['nx']), float(v.attrib['ny']), float(v.attrib['nz']))
                        nIdx.append(self.normals_.append_and_write(pt, self.objFid_))
                    if not(self.isFront_) and v.tag == 'BackTextureCoords':
                        pt = Point3d(float(v.attrib['u']), float(v.attrib['v']), float(1.0))
                        tIdx.append(self.uvcoords_.append_and_write(pt, self.objFid_))
                    if v.tag == 'FrontTextureCoords':
                        pt = Point3d(float(v.attrib['u']), float(v.attrib['v']), float(1.0))
                        tIdx.append(self.uvcoords_.append_and_write(pt, self.objFid_))

        if not(self.isFront_ or self.isBack_):
            print "No Texture Found - Using default"
            self.objFid_.write('usemtl \t %s \n' % self.default_matname_)
            #assert False

        self.objFid_.write('f\t')
        
        if (self.isFront_ and self.isFrontTex_) or (not (self.isFront_) and self.isBackTex_):  
            for i in range(0,3):
                self.objFid_.write('%d/%d/%d \t' % (vIdx[i] + 1, tIdx[i] + 1, nIdx[i] + 1))
        else:
            for i in range(0,3):
                self.objFid_.write('%d//%d \t' % (vIdx[i] + 1, nIdx[i] + 1))
        self.objFid_.write('\n')


    def parse_triangle(self, tri):
        #print self.material_ 
        numTri    = int(tri.attrib['Count'])
        #print "Number of triangles: " + str(numTri)
        child     = [c for c in tri]
        #print "Number of vertices: " + str(len(child))
        triangles = [child[i:i+3] for i in range(0,numTri*3,3)]
        for t in triangles:
            self.write_triangle(t)


    def parse_face(self, face):
        frontName = ''
        backName  = ''
        self.isFront_ = False
        self.isBack_  = False
        self.isFrontTex_ = False
        self.isBackTex_  = False
        self.material_   = None
        self.num_faces_ += 1
        #return
        for child in face:
            if child.tag == 'FrontMaterial':
                self.isFront_ = True
                self.isFrontTex_ = int(child.attrib['HasTexture']) == 1
                frontName = child.attrib['Name']
                self.objFid_.write('usemtl \t %s \n' % frontName)
                self.material_ = frontName
            if child.tag == 'BackMaterial':
                self.isBack_ = True
                self.isBackTex_  = int(child.attrib['HasTexture']) == 1
                backName = child.attrib['Name']
                if not self.isFront_:
                    self.material_ = backName
                    self.objFid_.write('usemtl \t %s \n' % backName)

            if child.tag == 'Triangles':
                self.parse_triangle(child)
       

    def parse_group(self, elm):
        print "Group Found"
        for child in elm:
            if child.tag=='Face':
                self.parse_face(child)
            if child.tag =='Group':
                self.parse_group(child)
            


    def parse_geometry(self, elm):
        print "Geo Found"
        for child in elm:
            if child.tag=='Face':
                self.parse_face(child)


    def parse_component_definition(self, elm):
        print "Components Found"
        for child in elm:
            if child.tag =='Group':
                self.parse_group(child)
            if child.tag =='Face':
                self.parse_face(child)

    def parse_component_definitions(self, elm):
        print "CompDef Found"
        for child in elm:
            if child.tag =='ComponentDefinition':
                self.parse_component_definition(child)
            if child.tag =='Face':
                self.parse_face(child)
            if child.tag =='Group':
                self.parse_group(child)

    def parse_root(self, text):
        root = ET.fromstring(text)
        for child in root:
            if child.tag == 'SkpToXML':
                self.parse_version(child)
            elif child.tag == 'Layers':
                #Do Nothing
                print "Nothing"
            elif child.tag == 'Materials':
                self.add_default_material()
                self.parse_materials(child)
            elif child.tag =='ComponentDefinitions':
                self.parse_component_definitions(child)
            elif child.tag == 'Geometry':
                self.parse_geometry(child)
            elif child.tag == 'Group':
                self.parse_group(child)


def find_tags(root, tags):
    for child in root:
        if child.tag not in tags:
            tags.append(child.tag)
        find_tags(child, tags)
    return tags

def get_all_tags(filename):
    data   = get_string(filename)
    tags   = []
    root = ET.fromstring(data)
    find_tags(root, tags)
    return tags

def main(filename):
    data   = get_string(filename)
    objFid = open('tmp/myobj.obj','w')
    mtlFid = open('tmp/mymtl.mtl','w')
    parser = Xml2Obj(objFid, mtlFid);
    parser.parse_root(data)
    objFid.close()
    mtlFid.close()

    print "Number of vertices processed: %d" % parser.vertices_.length()
    print "Number of faces processed: %d" % parser.num_faces_

