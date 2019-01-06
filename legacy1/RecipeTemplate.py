import mako.template
import mako.lookup

from Unit import UnitLookup

class _RenderHelper(object):
	def __init__(self):
		self._ulookup = UnitLookup()

	def ingredient(self, text):
		unit = self._ulookup.lookup(text)
		print(unit)

class RecipeTemplate(object):
	def __init__(self, tname):
		self._lookup = mako.lookup.TemplateLookup("template/", input_encoding = "utf-8", output_encoding = "utf-8", strict_undefined = True)
		self._template = self._lookup.get_template(tname)
	
	def render(self):
		helper = _RenderHelper()
		rendervars = {
			"i":	helper.ingredient,
		}
		result = self._template.render(**rendervars)
		return result
