String.prototype.trim = function () {
    return this.replace(/^[\s\,]*/, "").replace(/[\s\,]*$/, ""); //for remove the space and comma at the begining/end of the tag.
};


//passowrd validator;
function validatorPassword(password) {
    var filter = /^s*[A-Za-z0-9]{4,20}s*$/;
    return filter.test(password);
}

//email validator;
function validatorEmail(email) {
    var filter = /^([-_A-Za-z0-9\.]+)@([_A-Za-z0-9]+\.)+[A-Za-z0-9]{2,3}$/;
    return filter.test(email);
}

//username validator;
function validatorUsername(username) {
    var filter = /^([-_A-Za-z0-9\.]+)$/;
    return filter.test(username);
}

function showError(error_id) {
    document.getElementById(error_id).innerHTML = "&nbsp;<img src=\"/img/ico_cross_org.gif\" width=14 height=14><br />";
}
function showCheck(error_id) {
    document.getElementById(error_id).innerHTML = "&nbsp;<img src=\"/img/ico_check_blu.gif\" width=14 height=14><br /><span style=\"color:blue\">";
}


var handleFailure = function(o) {
    if (o.responseText !== undefined) {
        alert("Client RPC Request Error, please retry.");
    }
}

//focus on the form element.
function focusOn(elemName) {
    try {
        var elem = document.getElementById(elemName);
        if (elem) {
            elem.focus();
            elem.select();
        }
    } catch (e) {
    }
    ;
}

//make the option with specified value to be selected.
function selectByValue(selectoId, value) {
    var selectObj = document.getElementById(selectoId);
    for (var i = 0; i < selectObj.length; i++) {
        if (selectObj[i].value == value) {
            selectObj[i].selected = true;
            break;
        }
    }
}

//clear the options of selector.
function clearSelectOptions(selectoId) {
    var e = document.getElementById(selectoId);
    if (e == null) {
        return true;
    }
    var length = e.options.length;
    for (var i = 0; i < length; i++) {
        e.options[0] = null;
    }
    return true;
}
