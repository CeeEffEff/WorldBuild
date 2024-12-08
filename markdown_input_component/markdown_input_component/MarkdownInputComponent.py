# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MarkdownInputComponent(Component):
    """A MarkdownInputComponent component.
MarkdownInputComponent for Dash.
Provides a rich text editor for Markdown input with live preview.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    Additional CSS class for the container.

- options (dict; default {    spellChecker: False,    status: False,    toolbar: ["bold", "italic", "heading", "|", "quote", "code", "|", "preview", "side-by-side", "fullscreen"],}):
    Options for the SimpleMDE editor. See:
    https://github.com/sparksuite/simplemde-markdown-editor#configuration.

- style (dict; optional):
    Inline style for the container.

- value (string; default ''):
    The Markdown content."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'markdown_input_component'
    _type = 'MarkdownInputComponent'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, options=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'options', 'style', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'options', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(MarkdownInputComponent, self).__init__(**args)
