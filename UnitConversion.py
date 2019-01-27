#	recipes - Python-based HTML5 generation for cooking recipes
#	Copyright (C) 2019-2019 Johannes Bauer
#
#	This file is part of recipes.
#
#	recipes is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	recipes is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with recipes; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

class UnknownUnitException(Exception): pass

class UnitConversion():
	def __init__(self, conversion_dict):
		self._dict = dict(conversion_dict)

	def is_known(self, unit):
		return unit in self._dict

	def __call__(self, value, from_unit, to_unit):
		if from_unit == to_unit:
			return value
		if from_unit not in self._dict:
			raise UnknownUnitException("Cannot convert %.3f %s to anything, because I don't know the unit. Known: %s" % (value, from_unit, from_unit, ", ".join(sorted(self._dict.keys()))))
		if to_unit not in self._dict:
			raise UnknownUnitException("Cannot convert %.3f %s to anything, because I don't know the unit. Known: %s" % (value, to_unit, to_unit, ", ".join(sorted(self._dict.keys()))))
		from_scalar = self._dict[from_unit]
		to_scalar = self._dict[to_unit]
		return value * from_scalar / to_scalar
