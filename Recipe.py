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

from XMLParser import XMLParser

class Ingredient():
	def __init__(self, node, metadata):
		self._node = node
		self._meta = metadata

	@property
	def unit(self):
		return self._meta.getunitname(self._node.get("unit"))

	@property
	def cardinality(self):
		return self._node["count"]

	@property
	def name(self):
		return self._meta.getingredientname(self.iid)

	@property
	def iid(self):
		return self._node["name"]

class IngredientList():
	def __init__(self, node, metadata):
		self._node = node
		self._meta = metadata

	@property
	def name(self):
		return self._node.getname()

	def __iter__(self):
		for ingredient in self._node.ingredient:
			yield Ingredient(ingredient, self._meta)

class Recipe():
	def __init__(self, xml_filename, metadata):
		self._xml = XMLParser().parsefile(xml_filename)
		self._meta = metadata

	@property
	def name(self):
		return self._xml["name"]

	@property
	def ingredient_class_cnt(self):
		return len(list(self._xml.ingredients))

	@property
	def ingredient_classes(self):
		for node in self._xml.ingredients.getallchildren():
			if node.getname() != "#cdata":
				yield IngredientList(node, self._meta)

	@property
	def serves(self):
		if self._xml.getchild("serves") is not None:
			return [ (node["count"], node["value"]) for node in self._xml.serves.option ]

	@property
	def preparation(self):
		return self._xml.preparation

