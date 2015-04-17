from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SelectField, validators
from wtforms.widgets import TextArea
from wtforms.widgets import html_params, HTMLString
from cgi import escape

# custom widget to display SelectField
class MyOption(object):
   def __call__(self, field, **kwargs):
       options = dict(kwargs, value=field._value())
       if field.checked:
           options['selected'] = True

       label = field.label.text
       render_params = (html_params(**options), escape(unicode(label)))

       return HTMLString(u'<option %s>%s</option>' % render_params)

# Item Form
class ItemForm(Form):
	name = TextField('itemname', [validators.Required()], description = "Name")
	category_id = SelectField('category_id', [validators.Required()], coerce=int, description = "Category", option_widget=MyOption())
	description = TextField('description', [validators.Required()], description = "Description", widget=TextArea())
	
# Category Form
class CategoryForm(Form):
	name = TextField('category', [validators.Required()], description = "Name")
	
		

