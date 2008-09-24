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
