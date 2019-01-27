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

import re

class Tools():
	_SIMPLE_FRACTION_RE = re.compile("(?P<numerator>\d+)\s*/\s*(?P<denominator>\d+)")
	_WHOLE_SIMPLE_FRACTION_RE = re.compile("(?P<whole>\d+)\s+(?P<numerator>\d+)\s*/\s*(?P<denominator>\d+)")

	@classmethod
	def str2float(cls, text):
		text = text.strip()
		match = cls._WHOLE_SIMPLE_FRACTION_RE.fullmatch(text)
		if match:
			match = match.groupdict()
			return int(match["whole"]) + (int(match["numerator"]) / int(match["denominator"]))

		match = cls._SIMPLE_FRACTION_RE.fullmatch(text)
		if match:
			match = match.groupdict()
			return int(match["numerator"]) / int(match["denominator"])

		return float(text)
