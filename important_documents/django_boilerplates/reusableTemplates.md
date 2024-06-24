Reusable form templates¶
The HTML output when rendering a form is itself generated via a template. You can control this by creating an appropriate template file and setting a custom FORM_RENDERER to use that form_template_name site-wide. You can also customize per-form by overriding the form’s template_name attribute to render the form using the custom template, or by passing the template name directly to Form.render().

The example below will result in {{ form }} being rendered as the output of the form_snippet.html template.

In your templates:
```
# In your template:
{{ form }}

# In form_snippet.html:

{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
```
Then you can configure the FORM_RENDERER setting:
```
settings.py¶
from django.forms.renderers import TemplatesSetting


class CustomFormRenderer(TemplatesSetting):
    form_template_name = "form_snippet.html"


FORM_RENDERER = "project.settings.CustomFormRenderer"
```
… or for a single form:
```
class MyForm(forms.Form):
    template_name = "form_snippet.html"
    ...
… or for a single render of a form instance, passing in the template name to the Form.render(). Here’s an example of this being used in a view:

def index(request):
    form = MyForm()
    rendered_form = form.render("form_snippet.html")
    context = {"form": rendered_form}
    return render(request, "index.html", context)

```