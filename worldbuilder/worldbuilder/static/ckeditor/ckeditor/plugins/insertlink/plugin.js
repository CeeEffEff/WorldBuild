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
        // Define the dialog window
        CKEDITOR.dialog.add('insertlinkDialog', function (editor) {
            return {
                title: 'Insert Link',
                minWidth: 400,
                minHeight: 200,
                contents: [
                    {
                        id: 'tab-basic',
                        label: 'Basic Settings',
                        elements: [
                            {
                                type: 'select',
                                id: 'objectId',
                                label: 'Select Object',
                                items: [],  // Populate this dynamically in Django admin
                                setup: function (widget) {
                                    // Set the value when editing an existing link
                                    this.setValue(widget.data.objectId);
                                },
                                commit: function (widget) {
                                    // Set the data to be used in the final link
                                    widget.setData('objectId', this.getValue());
                                }
                            }
                        ]
                    }
                ],
                onShow: function () {
                    const dialog = this;
                    const select = dialog.getContentElement('tab-basic', 'objectId');
                    // Make an AJAX request to a Django view that returns the list of objects
                    fetch('/path/to/objects/')
                        .then(response => response.json())
                        .then(data => {
                            // Populate the 'items' array in the select element
                            select.items = data.objects.map(object => [object.id, object.name]);
                        })
                        .catch(error => console.error('Error fetching objects:', error));
                }
            };
        });
    }
});
