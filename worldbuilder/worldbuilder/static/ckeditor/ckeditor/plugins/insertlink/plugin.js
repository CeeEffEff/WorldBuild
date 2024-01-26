// static/js/ckeditor_plugins/insertlink.js
CKEDITOR.plugins.add('insertlink', {
    icons: 'insertlink',
    init: function (editor) {
        editor.addCommand('insertLinkCommand', {
            exec: function (editor) {
                // Open a custom dialog for object selection
                editor.openDialog('insertlinkDialog');
            }
        });
        var staticUrl = CKEDITOR.getUrl('/static/');
        // Add the "Insert Link" button to the toolbar
        editor.ui.addButton('InsertLink', {
            label: 'Insert Link',
            command: 'insertLinkCommand',
            toolbar: 'insert',
            icon: staticUrl + '/ckeditor/ckeditor/plugins/insertlink/icons/insertlink.png'
        });

        // Do the list getting ahead of time and only add the dialog once that is done
        fetch(CKEDITOR.getUrl('/lists'))
            .then(response => response.json())
            .then(data => {
                build_dialog(data);
            })
            .catch(error => console.error('Error fetching objects:', error));
    }
});
function build_dialog(data) {
    const tabs = [];
    const model_names = [];
    data.forEach((model_name) => {
        model_names.push(model_name);
        tabs.push(
            {
                id: model_name,
                // id: 'tab-' + model_name,
                label: model_name + ' Models',
                elements: [
                    {
                        type: 'select',
                        id: 'modelId',
                        label: 'Select',
                        items: [], // Populate this dynamically in Django admin
                        setup: function (widget) {
                            // Set the value when editing an existing link
                            this.setValue(widget.data.objectId);
                        },
                    }
                ]
            }
        );
    });
    CKEDITOR.dialog.add('insertlinkDialog', function (editor) {
        return {
            title: 'Insert Link to Model',
            minWidth: 150 * model_names.length,
            minHeight: 200,
            contents: tabs,
            onShow: function () {
                const dialog = this;
                fetch(CKEDITOR.getUrl('/lists'))
                    .then(response => response.json())
                    .then(data => {
                        data.forEach((model_name) => {
                            const select = dialog.getContentElement(model_name, 'modelId');
                            // Make an AJAX request to a Django view that returns the list of objects
                            fetch(CKEDITOR.getUrl('/lists/' + model_name))
                                .then(response => response.json())
                                .then(data => {
                                    // Clear existing options
                                    // select.getInputElement().$.length = 0;
                                    select.clear();
                                    // Dynamically set the items
                                    const items = data.map(object => [object.model + object.pk, object.fields.name]);
                                    items.forEach(([value, text]) => {
                                        select.add(text, value);
                                    });
                                })
                                .catch(error => console.error('Error fetching objects:', error));
                        });
                    });
            },
            onOk: function (widget) {
                const dialog = this;
                const select = dialog.getContentElement(dialog._.currentTabId, 'modelId');
                // Set the data to be used in the final link
                editor.insertHtml(select.getValue());
            }
        };
    });
}

