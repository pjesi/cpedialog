(function() {
    var Dom = YAHOO.util.Dom,
            Event = YAHOO.util.Event,
            txt = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas sit amet metus. Nunc quam elit, posuere nec, auctor in, rhoncus quis, dui. Aliquam erat volutpat. Ut dignissim, massa sit amet dignissim cursus, quam lacus feugiat.';

    YAHOO.CSSGridBuilder = {
        init: function() {
            this.type = 'yui-t5';
            this.docType = 'doc2';
            this.rows = [];
            this.rows[0] = Dom.get('splitBody0');
            this.sliderData = false;

            this.bd = Dom.get('bd');
            this.doc = Dom.get('doc2');
            this.template = Dom.get('which_grid');

            Event.on(this.template, 'change', YAHOO.CSSGridBuilder.changeType, YAHOO.CSSGridBuilder, true);
            Event.on('splitBody0', 'change', YAHOO.CSSGridBuilder.splitBody, YAHOO.CSSGridBuilder, true);
            Event.on('which_doc', 'change', YAHOO.CSSGridBuilder.changeDoc, YAHOO.CSSGridBuilder, true);

            var reset_button = new YAHOO.widget.Button('resetBuilder');
            reset_button.on('click', YAHOO.CSSGridBuilder.reset, YAHOO.CSSGridBuilder, true);

            var add_button = new YAHOO.widget.Button('addRow');
            add_button.on('click', YAHOO.CSSGridBuilder.addRow, YAHOO.CSSGridBuilder, true);
        },
        reset: function(ev) {
            for (var i = 1; i < this.rows.length; i++) {
                if (this.rows[i]) {
                    if (Dom.get('splitBody' + i)) {
                        Dom.get('splitBody' + i).parentNode.parentNode.removeChild(Dom.get('splitBody' + i).parentNode);
                    }
                }
            }
            this.rows = [];
            this.rows[0] = Dom.get('splitBody0');
            Dom.get('which_doc').options.selectedIndex = 1;  //950px
            Dom.get('which_grid').options.selectedIndex = 4; //yui-t5
            Dom.get('splitBody0').options.selectedIndex = 2;  //yui-gc

            this.changeDoc();
            this.changeType();
            this.splitBody();
            Event.stopEvent(ev);
        },
        addRow: function(ev) {
            var tmp = Dom.get('splitBody0').cloneNode(true);
            tmp.id = 'splitBody' + this.rows.length;
            this.rows[this.rows.length] = tmp;
            this.rowCounter++;
            var p = document.createElement('p');
            p.innerHTML = 'Row:<a href="#" class="rowDel" id="gridRowDel' + this.rows.length + '" title="Remove this row">[X]</a><br>';
            p.appendChild(tmp);
            Dom.get('splitBody0').parentNode.parentNode.appendChild(p);
            Event.on(tmp, 'change', YAHOO.CSSGridBuilder.splitBody, YAHOO.CSSGridBuilder, true);
            Event.on('gridRowDel' + this.rows.length, 'click', YAHOO.CSSGridBuilder.delRow, YAHOO.CSSGridBuilder, true);
            this.splitBody();
            Event.stopEvent(ev);
        },
        delRow: function(ev) {
            var tar = Event.getTarget(ev);
            var id = tar.id.replace('gridRowDel', '');
            Dom.get('splitBody0').parentNode.parentNode.removeChild(tar.parentNode);
            this.rows[id] = false;
            this.splitBody();
            Event.stopEvent(ev);
        },
        changeCustomDoc: function(ev) {
            var tar = Event.getTarget(ev);
            this.docType = Dom.get('which_doc').options[Dom.get('which_doc').selectedIndex].value;
            Event.stopEvent(ev);
        },
        changeDoc: function(ev) {
            this.docType = Dom.get('which_doc').options[Dom.get('which_doc').selectedIndex].value;
            if (this.docType == 'custom-doc') {
                this.showSlider();
            } else {
                this.doc.style.width = '';
                this.doc.style.minWidth = '';
                this.sliderData = false;
                this.doc.id = this.docType;
                this.doTemplate();
            }
            if (ev) {
                Event.stopEvent(ev);
            }
        },
        changeType: function() {
            this.type = this.template.options[this.template.selectedIndex].value;
            this.doc.className = this.type;
            this.doTemplate();
        },
        doTemplate: function() {
            var html = '';
            var str = '';
            var navStr = '';
            if (!this.bodySplit) {
                this.splitBody();
            }
            str = this.bodySplit.replace(/\{0\}/g, '');
            switch (this.type) {
                case 'yui-t7':
                    html = str;
                    break;
                default:
                    html = '<div id="yui-main">' + "\n\t" + '<div class="yui-b">' + str + '</div>' + "\n\t" + '</div>' + "\n\t" + '<div class="yui-b"><ul class="list" id="list4"></ul></div>' + "\n\t";
                    break;
            }
            this.bd.innerHTML = html;
        },
        PixelToEmStyle: function(size, prop) {
            var data = '';
            var prop = ((prop) ? prop.toLowerCase() : 'width');
            var sSize = (size / 13);
            data += prop + ':' + (Math.round(sSize * 100) / 100) + 'em;';
            data += '*' + prop + ':' + (Math.round((sSize * 0.9759) * 100) / 100) + 'em;';
            if ((prop == 'width') || (prop == 'height')) {
                data += 'min-' + prop + ':' + size + 'px;';
            }
            return data;
        },
        splitBody: function() {
            this.bodySplit = '';
            for (var i = 0; i < this.rows.length; i++) {
                this.splitBodyTemplate(Dom.get('splitBody' + i));
            }
            this.doTemplate();
        },
        splitBodyTemplate: function(tar) {
            if (tar) {
                var bSplit = tar.options[tar.selectedIndex].value;
                var str = '';
                switch (bSplit) {
                    case '1':
                        str += '<div class="yui-g"><ul class="list" id="list2">' + "\n";
                        str += '{0}';
                        str += '</ul></div>' + "\n";
                        break;
                    case '2':
                        str += '<div class="yui-g">' + "\n";
                        str += '    <div class="yui-u first"><ul class="list" id="list2">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '    <div class="yui-u"><ul class="list" id="list3">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '</div>' + "\n";
                        break;
                    case '3':
                        str += '    <div class="yui-gb">' + "\n";
                        str += '        <div class="yui-u first"><ul class="list" id="list2">' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '        <div class="yui-u"><ul class="list" id="list3">' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '        <div class="yui-u"><ul class="list" id="list6">' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '    </div>' + "\n";
                        break;
                    case '4':
                        str += '<div class="yui-g">' + "\n";
                        str += '    <div class="yui-g first">' + "\n";
                        str += '        <div class="yui-u first"><ul class="list" id="list2">' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '        <div class="yui-u"><ul class="list" id="list3">' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '    </div>' + "\n";
                        str += '    <div class="yui-g">' + "\n";
                        str += '        <div class="yui-u first"><ul class="list" id="list6">' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '        <div class="yui-u"><ul class="list" id="list7">' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '    </div>' + "\n";
                        str += '</div>' + "\n";
                        break;
                    case '5':
                        str += '<div class="yui-g">' + "\n";
                        str += '    <div class="yui-u first"><ul class="list" id="list2"> ' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '    <div class="yui-g">' + "\n";
                        str += '        <div class="yui-u first"><ul class="list" id="list3"> ' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '        <div class="yui-u"><ul class="list" id="list6"> ' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '    </div>' + "\n";
                        str += '</div>' + "\n";
                        break;
                    case '6':
                        str += '<div class="yui-g">' + "\n";
                        str += '    <div class="yui-g first">' + "\n";
                        str += '        <div class="yui-u first"><ul class="list" id="list5">' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '        <div class="yui-u"><ul class="list" id="list6">' + "\n";
                        str += '{0}';
                        str += '        </ul></div>' + "\n";
                        str += '    </div>' + "\n";
                        str += '    <div class="yui-u"><ul class="list" id="list2">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '</div>' + "\n";
                        break;
                    case '7':
                        str += '<div class="yui-gc">' + "\n";
                        str += '    <div class="yui-u first"><ul class="list" id="list2">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '    <div class="yui-u"><ul class="list" id="list3">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '</div>' + "\n";
                        break;
                    case '8':
                        str += '<div class="yui-gd">' + "\n";
                        str += '    <div class="yui-u first"><ul class="list" id="list3">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '    <div class="yui-u"><ul class="list" id="list2">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '</div>' + "\n";
                        break;
                    case '9':
                        str += '<div class="yui-ge">' + "\n";
                        str += '    <div class="yui-u first"><ul class="list" id="list2">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '    <div class="yui-u"><ul class="list" id="list3">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '</div>' + "\n";
                        break;
                    case '10':
                        str += '<div class="yui-gf">' + "\n";
                        str += '    <div class="yui-u first"><ul class="list" id="list3">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '    <div class="yui-u"><ul class="list" id="list2">' + "\n";
                        str += '{0}';
                        str += '    </ul></div>' + "\n";
                        str += '</div>' + "\n";
                        break;
                }
                this.bodySplit += '<div id="gridBuilder' + (this.rows.length - 1) + '">' + str + '</div>';
            }
        },
        showSlider: function() {
            var handleCancel = function() {
                showSlider.hide();
                return false;
            }
            var handleSubmit = function() {
                YAHOO.CSSGridBuilder.sliderData = Dom.get('sliderValue').value;

                showSlider.hide();
            }

            var myButtons = [
                { text:'Save', handler: handleSubmit, isDefault: true },
                { text:'Cancel', handler: handleCancel }
            ];

            var showSlider = new YAHOO.widget.Dialog('showSlider', {
                    close: true,
                    draggable: true,
                    modal: true,
                    visible: true,
                    fixedcenter: true,
                    width: '275px',
                    zindex: 9001,
                    postmethod: 'none',
                    buttons: myButtons
                }
            );
            showSlider.hideEvent.subscribe(function() {
                this.destroy();
            }, showSlider, true);
            showSlider.setHeader('CSSGridBuilder Custom Body Size');
            var body = '<p>Adjust the slider below to adjust your body size or set it manually with the text input. <i>(Be sure to include the % or px in the text input)</i></p>';
            body += '<form name="customBodyForm" method="POST" action="">';
            body += '<p>Current Setting: <input type="text" id="sliderValue" value="100%" size="8" onfocus="this.select()" /></p>';
            body += '<span>Unit: ';
            body += '<input type="radio" name="movetype" id="moveTypePercent" value="percent" checked> <label for="moveTypePercent">Percent</label>&nbsp;';
            body += '<input type="radio" name="movetype" id="moveTypePixel" value="pixel"> <label for="moveTypePixel">Pixel</label></span>';
            body += '</form>';
            body += '<div id="sliderbg"><div id="sliderthumb"><img src="/img/thumb-n.gif" /></div>';
            body += '</div>';
            showSlider.setBody(body);


            var handleChange = function(f) {
                if (typeof f == 'object') { f = slider.getValue(); }
                if (Dom.get('moveTypePercent').checked) {
                    var w = Math.round(f / 2);
                    Dom.get('custom-doc').style.width = w + '%';
                    Dom.get('sliderValue').value = w + '%';
                } else {
                    var w = Math.round(f / 2);
                    var pix = Math.round(Dom.getViewportWidth() * (w / 100));
                    Dom.get('custom-doc').style.width = pix + 'px';
                    Dom.get('sliderValue').value = pix + 'px';
                }
                Dom.get('custom-doc').style.minWidth = '250px';
            }

            var handleBlur = function() {
                f = Dom.get('sliderValue').value;
                if (f.indexOf('%') != -1) {
                    Dom.get('moveTypePercent').checked = true;
                    f = (parseInt(f) * 2);
                } else if (f.indexOf('px') != -1) {
                    Dom.get('moveTypePixel').checked = true;
                    f = (((parseInt(f) / Dom.getViewportWidth()) * 100) * 2);
                } else {
                    Dom.get('sliderValue').value = '100%';
                    f = 200;
                }
                slider.setValue(f);
            }

            showSlider.render(document.body);
            var slider = YAHOO.widget.Slider.getHorizSlider('sliderbg', 'sliderthumb', 0, 200, 1);
            slider.setValue(200);
            slider.onChange = handleChange;

            Event.on(['moveTypePercent', 'moveTypePixel'], 'click', handleChange);
            Event.on('sliderValue', 'blur', handleBlur);

            this.doc.id = this.docType;
            this.doc.style.width = '100%';
            this.doTemplate();
        }
    };
})();
