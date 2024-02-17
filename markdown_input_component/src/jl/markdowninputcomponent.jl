# AUTO GENERATED FILE - DO NOT EDIT

export markdowninputcomponent

"""
    markdowninputcomponent(;kwargs...)

A MarkdownInputComponent component.
MarkdownInputComponent is a wrapper on the SimpleMDE component.
It renders an input with the property `value`
which is editable by the user.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `value` (String; optional): The value displayed in the input.
"""
function markdowninputcomponent(; kwargs...)
        available_props = Symbol[:id, :value]
        wild_props = Symbol[]
        return Component("markdowninputcomponent", "MarkdownInputComponent", "markdown_input_component", available_props, wild_props; kwargs...)
end

