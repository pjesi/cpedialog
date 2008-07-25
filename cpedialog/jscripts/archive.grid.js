YAHOO.util.Event.addListener(window, "load", function() {
    EnhanceFromMarkup = new function() {
        var myColumnDefs = [
            {key:"monthyear",label:"Month Year",sortable:true},
            {key:"entrycount",sortable:true,label:"Entry count"},
            {key:"id",label:"Id",sortable:true,isPrimaryKey:true},
            {key:"delete",label:"Delete",action:'delete',formatter:function(elCell) {
                elCell.innerHTML = '<img src="/img/delete.gif" title="delete row" />';
                elCell.style.cursor = 'pointer';}},
            {key:"refreshcount",label:"Refresh entry count",action:'refresh',formatter:function(elCell) {
                elCell.innerHTML = 'refresh';
                elCell.style.cursor = 'pointer';}}
        ];

        this.myDataSource = new YAHOO.util.DataSource(YAHOO.util.Dom.get("archivetable"));
        this.myDataSource.responseType = YAHOO.util.DataSource.TYPE_HTMLTABLE;
        this.myDataSource.responseSchema = {
            fields: [{key:"tag"},{key:"entrycount"}, {key:"id"}, {key:"delete"}, {key:"refreshcount"}
            ]
        };
        this.myDataTable = new YAHOO.widget.DataTable("archivediv", myColumnDefs, this.myDataSource,
           { sortedBy:{key:"entrycount",dir:"desc"}});

        // Set up editing flow
        this.highlightEditableCell = function(oArgs) {
            var elCell = oArgs.target;
            if (YAHOO.util.Dom.hasClass(elCell, "yui-dt-editable")) {
                this.highlightCell(elCell);
            }
        };
        this.myDataTable.subscribe("cellMouseoverEvent", this.highlightEditableCell);
        this.myDataTable.subscribe("cellMouseoutEvent", this.myDataTable.onEventUnhighlightCell);
        //this.myDataTable.subscribe("cellClickEvent", this.myDataTable.onEventShowCellEditor);

        var myBuildUrl = function(datatable,record) {
            var url = '';
            var cols = datatable.getColumnSet().keys;
            for (var i = 0; i < cols.length; i++) {
                if (cols[i].isPrimaryKey) {
                    url += '&' + cols[i].key + '=' + encodeURIComponent(record.getData(cols[i].key));
                }
            }
            return url;
        };

        this.myDataTable.subscribe('cellClickEvent', function(ev) {
            var target = YAHOO.util.Event.getTarget(ev);
            var column = this.getColumn(target);
            if (column.action == 'delete') {
                if (confirm('Are you sure to delete the archive (no article will be deleted.) ?')) {
                    var record = this.getRecord(target);
                    YAHOO.util.Connect.asyncRequest('POST','/rpc?action=DeleteArchive' + myBuildUrl(this,record),
                    {
                        success: function (o) {
                            if (o.responseText == 'true') {
                                this.deleteRow(target);
                            } else {
                                alert(o.responseText);
                            }
                        },
                        failure: function (o) {
                            alert(o.statusText);
                        },
                        scope:this
                    }
                            );
                }
            } else {
                this.onEventShowCellEditor(ev);
            }
        });

        ;
    };
});
