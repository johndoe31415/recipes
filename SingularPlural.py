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

class SingularPlural():
	def __init__(self, text):
		if "|" in text:
			(self._singular, ext) = text.split("|", maxsplit = 1)
			if ext.startswith("+"):
				self._plural = self._singular + ext[1:]
			else:
				self._plural = ext
		else:
			self._singular = text
			self._plural = text

	@property
	def singular(self):
		return self._singular

	@property
	def plural(self):
		return self._plural

	def __call__(self, value):
		if value == 1:
			return self.singular
		else:
			return self.plural
