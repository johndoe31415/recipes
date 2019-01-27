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

import json
from SingularPlural import SingularPlural
from UnitConversion import UnitConversion

class Metadata():
	def __init__(self, conversion_file, ingredient_file):
		with open(conversion_file) as f:
			self._conversion = json.load(f)
		with open(ingredient_file) as f:
			self._ingredient = json.load(f)
		self._mass_units = UnitConversion(self._conversion["units"]["mass"])
		self._volume_units = UnitConversion(self._conversion["units"]["volume"])

	@property
	def mass_units(self):
		return self._mass_units

	@property
	def volume_units(self):
		return self._volume_units

	def getingredientname(self, cid):
		ingredient = self._ingredient["ingredients"].get(cid)
		if ingredient is None:
			return SingularPlural(cid)
		return SingularPlural(ingredient["name"])

	def getunitname(self, unit_id):
		if unit_id is None:
			return None
		else:
			return SingularPlural(self._ingredient["units"].get(unit_id, unit_id))

	def getservingname(self, serving_id):
		return SingularPlural(self._ingredient["servings"].get(serving_id, serving_id))

	def get_density_of(self, ingredient_id):
		return self._conversion["ingredients"].get(ingredient_id, { }).get("density_g_per_l")

	def get_grams_per_unit_of(self, ingredient_id):
		return self._conversion["ingredients"].get(ingredient_id, { }).get("unit_weight_grams")

	def get_preferred_unit_of(self, ingredient_id):
		return self._ingredient["ingredients"].get(ingredient_id, { }).get("prefer")
