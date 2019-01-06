import collections

class Unit(object):
	def __init__(self, unit_class, conversion_coeff, unit_name):
		self._unit_class = unit_class
		self._conversion_coeff = conversion_coeff
		self._unit_name = unit_name

	@property
	def unit_class(self):
		return self._unit_class
	
	@property
	def conversion_coeff(self):
		return self._conversion_coeff
	
	@property
	def name(self):
		return self._name

	def __str__(self):
		return "%.1f %s(%s)" % (self.cardinality, self.name, self.unit_type)

class MassUnit(Unit):
	def __init__(self, conversion_coeff, unit_name):
		Unit.__init__(self, "mass", conversion_coeff, unit_name)

class VolumeUnit(Unit):
	def __init__(self, conversion_coeff, unit_name):
		Unit.__init__(self, "volume", conversion_coeff, unit_name)

class UnitValue(object):
	def __init__(self, cardinality, unit, value):
		assert(isinstance(unit, Unit))
		self._unit = unit
		self._value = value

class UnitLookup(object):
	def __init__(self):
		self._units = collections.defaultdict(list)
		self._register_unit(MassUnit(1, "g"))
		self._register_unit(MassUnit(0.001, "kg"))
		self._register_unit(MassUnit(, "oz"))


	def _register_unit(self, unit):
		self._units[unit.unit_class].append(unit)

	def lookup(self, unit_text):
		(cardinality, unit, ingredient) = unit_text.split(" ")
		cardinality = float(cardinality)
		unit = UndefinedUnit(cardinality, )
		print(cardinality)


if __name__ == "__main__":
	lookup = UnitLookup()
	lookup.lookup("4 EL Zucker")

