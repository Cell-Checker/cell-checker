from mako.template import Template
from mako.lookup import TemplateLookup


def render_html(template_name, context):
    # Setup the template lookup, assuming templates are in the 'templates' directory
    lookup = TemplateLookup(directories=['templates'])

    # Load the template
    template = lookup.get_template(template_name)

    # Render the template with the provided context
    return template.render(**context)
