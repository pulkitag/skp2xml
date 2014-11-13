def tolComp(x, y, tol):
    if abs(x-y) < tol:
        return True
    else:
        return False

class Color:
	def __init__(self, hexString):
		assert(len(hexString)==7)
		hexString = hexString[1:]
		self.r_ = int(hexString[0:2], 16)/255.0
		self.g_ = int(hexString[2:4], 16)/255.0
		self.b_ = int(hexString[4:6], 16)/255.0

	def toStr(self):
		return '%.6f \t %.6f \t %.6f' % (self.r_, self.g_, self.b_)

class Point3d:
    def __init__(self,x=0.0,y=0.0,z=1.0):
        self.x_ = x
        self.y_ = y
        self.z_ = z

    def __eq__(self, other):
        tol = 1e-3
        return tolComp(self.x_, other.x_, tol) and \
               tolComp(self.y_, other.y_, tol) and \
               tolComp(self.z_, other.z_, tol)

    def display(self):
        print "%f \t %f \t %f" % (self.x_, self.y_, self.z_)

    def get_display_str(self):
        return "%f \t %f \t %f" % (self.x_, self.y_, self.z_)

    def get_display_strxy(self):
        return "%f \t %f" % (self.x_, self.y_)

class Store:
    def __init__(self, prefix = 'v'):
        self.x_ = []
        self.prefix_ = prefix

    def append(self, x):
        if x in self.x_:
            return self.x_.index(x)
        else:
            self.x_.append(x)
            return len(self.x_) - 1

    def append_and_write(self, x, fid):
        if x in self.x_:
            return self.x_.index(x)
        else:
            self.x_.append(x)
            if self.prefix_ == 'v' or self.prefix_ == 'vn':
                fid.write('%s \t %s \n' % (self.prefix_, x.get_display_str()))
            else:
                fid.write('%s \t %s \n' % (self.prefix_, x.get_display_strxy()))
            return len(self.x_) - 1


    def length(self):
        return len(self.x_)

class Material:
	def __init__(self):
		self.ka_ = Color('#000000')
		self.kd_ = Color('#ffffff')
		self.ks_ = Color('#555555')
		self.alpha_ = 1
		self.is_opacity_ = False
		self.is_image_ = False
		self.image_name_ = ''
		self.name_ = 'default'

	def setKa(self, hStr):
		self.ka_ = Color(hStr)

	def setKd(self, hStr):
		self.kd_ = Color(hStr)

	def setKs(self, hStr):
		self.ks_ = Color(hStr)

	def setName(self, name):
		self.name_ = name

	def setAlpha(self, alpha):
		self.alpha_ = float(alpha)

	def setOpacity(self, is_op):
		self.is_opacity_ = is_op

	def setIsImage(self, is_im):
		self.is_image_ = is_im

	def setImName(self, im_name):
		self.image_name_ = im_name

	def writeMaterial(self, fid):
		fid.write('newmtl \t %s \n' % self.name_)
		fid.write('Ka \t %s \n' % self.ka_.toStr())
		fid.write('Kd \t %s \n' % self.kd_.toStr())
		fid.write('Ks \t %s \n' % self.ks_.toStr())
		if self.is_opacity_:
			fid.write('d \t %.6f \n' % self.alpha_)

		if self.is_image_:
			fid.write('map_Kd \t %s \n' % self.image_name_)

		fid.write('\n')
