(function() {
    var Dom = YAHOO.util.Dom,
            Event = YAHOO.util.Event;

    YAHOO.CSSGridBuilder = {
        init: function() {
            this.type = 'yui-t5';
            this.docType = 'doc2';
            this.sliderData = false;
            this.bd = Dom.get('bd');
            this.doc = Dom.get('doc2');
            this.template = Dom.get('which_grid');
            Dom.get('which_doc').options.selectedIndex = 1;  //950px
            Dom.get('which_grid').options.selectedIndex = 4; //yui-t5
            Dom.get('splitBody0').options.selectedIndex = 2;  //yui-gc
            Event.on(this.template, 'change', YAHOO.CSSGridBuilder.changeType, YAHOO.CSSGridBuilder, true);
            Event.on('splitBody0', 'change', YAHOO.CSSGridBuilder.splitBody, YAHOO.CSSGridBuilder, true);
            Event.on('which_doc', 'change', YAHOO.CSSGridBuilder.changeDoc, YAHOO.CSSGridBuilder, true);
            var reset_button = new YAHOO.widget.Button('resetBuilder');
            reset_button.on('click', YAHOO.CSSGridBuilder.reset, YAHOO.CSSGridBuilder, true);
        },
        reset: function(ev) {
            Dom.get('which_doc').options.selectedIndex = 1;  //950px
            Dom.get('which_grid').options.selectedIndex = 4; //yui-t5
            Dom.get('splitBody0').options.selectedIndex = 2;  //yui-gc

            this.changeDoc();
            this.changeType();
            this.splitBody();
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
            }
            if (ev) {
                Event.stopEvent(ev);
            }
        },
        changeType: function() {
            this.type = this.template.options[this.template.selectedIndex].value;
            this.doc.className = this.type;
        },
        splitBody: function() {
            this.splitBodyTemplate(Dom.get('splitBody0'));
        },
        splitBodyTemplate: function(tar) {
            var mainblock = Dom.get('div_mainblock');
            var mainblock_sub1 = Dom.get('div_mainblock_sub1');
            var mainblock_sub2 = Dom.get('div_mainblock_sub2');
            var list3 = Dom.get('list3').cloneNode(true);
            if (tar) {
                var bSplit = tar.options[tar.selectedIndex].value;
                var str = '';
                switch (bSplit) {
                    case '1':
                        mainblock.className = 'yui-g';
                        mainblock_sub1.className = "";
                        mainblock_sub2.className = "";
                        mainblock_sub2.style.display = "none";
                        break;
                    case '2':
                        mainblock.className = "yui-g";
                        mainblock_sub1.className = "yui-u first";
                        mainblock_sub2.className = "yui-u";
                        mainblock_sub2.style.display = "";
                        break;
                    case '3':
                        mainblock.className = "yui-gc";
                        mainblock_sub1.className = "yui-u first";
                        mainblock_sub2.className = "yui-u";
                        mainblock_sub2.style.display = "";
                        break;
                    case '4':
                        mainblock.className = "yui-gd";
                        mainblock_sub1.className = "yui-u first";
                        mainblock_sub2.className = "yui-u";
                        mainblock_sub2.style.display = "";
                        break;
                    case '5':
                        mainblock.className = "yui-ge";
                        mainblock_sub1.className = "yui-u first";
                        mainblock_sub2.className = "yui-u";
                        mainblock_sub2.style.display = "";
                        break;
                    case '6':
                        mainblock.className = "yui-gf";
                        mainblock_sub1.className = "yui-u first";
                        mainblock_sub2.className = "yui-u";
                        mainblock_sub2.style.display = "";
                        break;
                }
            }
        },

        switchNode:function(n1, n2) {
        {
            var tmp1 = [];
            var tmp2 = [];
            for (var i = 0; i < n1.childNodes.length; i++)
            {
                tmp1.push(n1.childNodes[i].cloneNode(true));
                n1.removeChild(n1.childNodes[i]);
            }
            for (var i = 0; i < n2.childNodes.length; i++)
            {
                tmp2.push(n2.childNodes[i].cloneNode(true));
                n2.removeChild(n2.childNodes[i]);

            }
            for (var i = 0; i < tmp1.length; i++)
            {
                n2.appendChild(tmp1[i]);
            }
            for (var i = 0; i < tmp2.length; i++)
            {
                n1.appendChild(tmp2[i]);
            }
        }
        },


        //show custom body size slider.
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
            showSlider.setHeader('Custom Body Size');
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
                if (typeof f == 'object') {
                    f = slider.getValue();
                }
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
        }
    };
})();
