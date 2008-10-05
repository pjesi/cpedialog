//for yui version 2.6.0
YAHOO.util.Event.addListener(window, "load", function() {
    EnhanceFromMarkup_update = new function() {
        YAHOO.widget.BaseCellEditor.prototype.asyncSubmitter = function() {
            // ++++ this is the inner function to handle the several possible failure conditions
            var onFailure = function (msg) {
                alert(msg);
            };

            var myBuildUrl = function(datatable, record) {
                var url = '';
                var cols = datatable.getColumnSet().keys;
                for (var i = 0; i < cols.length; i++) {
                    if (cols[i].isPrimaryKey) {
                        url += '&' + cols[i].key + '=' + encodeURIComponent(record.getData(cols[i].key));
                    }
                }
                return url;
            };

            var newData = this.getInputValue();
            // Copy the data to pass to the event
            var oldData = YAHOO.widget.DataTable._cloneObject(this.value);

            var editColumn = this.getColumn().key;
            var updateMethod;
            if (this.getDataTable().updateMethod) {
                updateMethod = this.getDataTable().updateMethod;
            } else {
                updateMethod = "Update";
            }
            YAHOO.util.Connect.asyncRequest(
                    'POST',
                    '/rpc?action=' + updateMethod + '&editColumn=' + editColumn + '&newData=' + encodeURIComponent(newData) +
                    '&oldData=' + encodeURIComponent(oldData) + myBuildUrl(this.getDataTable(), this.getRecord()),
            {
                success: function (o) {
                    // Update new value
                    this.value = newData;
                    this.getDataTable().updateCell(this.getRecord(), this.getColumn(), newData);

                    // Hide CellEditor
                    this.getContainerEl().style.display = "none";
                    this.isActive = false;
                    this.getDataTable()._oCellEditor =  null;

                    this.fireEvent("saveEvent",
                            {editor:this, oldData:oldData, newData:this.value});
                    YAHOO.log("Cell Editor input saved", "info", this.toString());

                    this.unblock();
                },
                failure: function(o) {
                    onFailure(o.statusText);
                    this.resetForm();
                    this.fireEvent("revertEvent",
                            {editor:this, oldData:oldData, newData:newData});
                    YAHOO.log("Could not save Cell Editor input " +
                            lang.dump(newData), "warn", this.toString());
                    this.unblock();
                },
                scope: this
            }
                    );
            this.unblock();            

        };
        ;
    };
    ;
});
