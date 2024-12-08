# AUTO GENERATED FILE - DO NOT EDIT

export markdowninputcomponent

"""
    markdowninputcomponent(;kwargs...)

A MarkdownInputComponent component.
MarkdownInputComponent for Dash.
Provides a rich text editor for Markdown input with live preview.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `className` (String; optional): Additional CSS class for the container.
- `options` (Dict; optional): Options for the SimpleMDE editor.
See: https://github.com/sparksuite/simplemde-markdown-editor#configuration
- `style` (Dict; optional): Inline style for the container.
- `value` (String; optional): The Markdown content.
"""
function markdowninputcomponent(; kwargs...)
        available_props = Symbol[:id, :className, :options, :style, :value]
        wild_props = Symbol[]
        return Component("markdowninputcomponent", "MarkdownInputComponent", "markdown_input_component", available_props, wild_props; kwargs...)
end

