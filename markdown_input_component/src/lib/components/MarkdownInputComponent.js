import React from 'react';
import PropTypes from 'prop-types';
import SimpleMDE from 'react-simplemde-editor';
import "easymde/dist/easymde.min.css";

/**
 * MarkdownInputComponent for Dash.
 * Provides a rich text editor for Markdown input with live preview.
 */
const MarkdownInputComponent = ({ id, value, setProps, className, style, options }) => {
    const handleChange = (newValue) => {
        if (setProps) {
            setProps({ value: newValue });
        }
    };

    return (
        <div id={id} className={`markdown-input-container ${className || ''}`} style={style}>
            <SimpleMDE
                value={value || ''}
                onChange={handleChange}
                options={options}
            />
        </div>
    );
};

MarkdownInputComponent.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The Markdown content.
     */
    value: PropTypes.string,

    /**
     * Dash callback property.
     */
    setProps: PropTypes.func,

    /**
     * Additional CSS class for the container.
     */
    className: PropTypes.string,

    /**
     * Inline style for the container.
     */
    style: PropTypes.object,

    /**
     * Options for the SimpleMDE editor.
     * See: https://github.com/sparksuite/simplemde-markdown-editor#configuration
     */
    options: PropTypes.object,
};

MarkdownInputComponent.defaultProps = {
    value: '',
    options: {
        spellChecker: false,
        status: false,
        toolbar: ["bold", "italic", "heading", "|", "quote", "code", "|", "preview", "side-by-side", "fullscreen"],
    },
};

export default MarkdownInputComponent;
