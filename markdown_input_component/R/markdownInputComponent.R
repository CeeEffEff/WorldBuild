# AUTO GENERATED FILE - DO NOT EDIT

#' @export
markdownInputComponent <- function(id=NULL, className=NULL, options=NULL, style=NULL, value=NULL) {
    
    props <- list(id=id, className=className, options=options, style=style, value=value)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'MarkdownInputComponent',
        namespace = 'markdown_input_component',
        propNames = c('id', 'className', 'options', 'style', 'value'),
        package = 'markdownInputComponent'
        )

    structure(component, class = c('dash_component', 'list'))
}
