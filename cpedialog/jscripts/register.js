var callbackFunc;
function MakeXMLRequest(url, callback) {
    req = false;
    callbackFunc = callback;
    // branch for native XMLHttpRequest object
    if (window.XMLHttpRequest) {
        try {
            req = new XMLHttpRequest();
        } catch(e) {
            req = false;
        }
        // branch for IE/Windows ActiveX version
    } else if (window.ActiveXObject) {
        try {
            req = new ActiveXObject("Msxml2.XMLHTTP");
        } catch(e) {
            try {
                req = new ActiveXObject("Microsoft.XMLHTTP");
            } catch(e) {
                req = false;
            }
        }
    }
    if (req) {
        req.onreadystatechange = processReqChange;
        req.open("GET", url, true);
        req.send("");
    }
    return true;
}
function processReqChange() {
    // only if req shows "loaded"
    if (req.readyState == 4) {
        // only if "OK"
        if (req.status == 200) {
            // ...processing statements go here...
            callbackFunc(req.responseText);
        } else {
            alert("There was a problem retrieving the response:\n" +
                  req.statusText);
        }
    }
}

var email_unavailable = false;
var showAvailEmail = function(restext) {
    /* ...processing statements go here... */
    if (restext.match(/\s*True\s*/)) {
        notavail = false;
        invalid = false;
        email_unavailable = false;
        document.getElementById('email_unavailable_text').style.display = 'none';
        /* if everything is cool, show error positive */
        showCheck("checkEmailAlert");
        /*successmsg(document.all.checkEmailAlert,document.order_form.email.value+' is available.');*/
    } else if (restext.match(/\s*Invalid\s*/)) {
        notavail = true;
        invalid = true;
        showError("checkEmailAlert");
        email_unavailable = true;
        document.getElementById('email_unavailable_text').style.display = 'none';
        /*errormsg(document.all.checkEmailAlert,document.order_form.email.value+' is invalid.');*/
    } else if (restext.match(/\s*Claimed\s*/)) {
        notavail = true;
        invalid = false;
        emObj = document.getElementById('email');
        showError("checkEmailAlert");
        email_unavailable = true;
        if (isComcast) {
            document.getElementById('email_unavailable_comcast_text').style.display = '';
            document.getElementById('email_unavailable_text').style.display = 'none';
        } else {
            document.getElementById('email_unavailable_comcast_text').style.display = 'none';
            document.getElementById('email_unavailable_text').style.display = '';
        }
        /*errormsg(document.all.checkEmailAlert,document.order_form.email.value+' is not available.');*/
    }
}
/* }}} */
function doSigninExisting(template) {
    var email = document.getElementById("email").value;
    if (!template) {
        template = 'corp';
    }
    location.href = '/signin?t=' + template + '&email=' + encodeURIComponent(email);
}
function updateCountry() {
    /* {{{ */
    var zip = document.getElementById("ob_zip");
    var postalTr = document.getElementById('postal_tr');
    if (document.getElementById("ob_country").value != "US" && document.getElementById("ob_country").value != "CA") {
        zip.value = '';
        zip.disabled = true;
        clearCheck("checkZipAlert");
        postalTr.style.visibility = 'hidden';
    } else {
        zip.disabled = false;
        /*checkZip(true);*/
        postalTr.style.visibility = '';
    }
}
/* }}} */
function changeColor(elem) {
    /* {{{ */
    /*elem.style.backgroundColor="white";*/
}
/* }}} */
function checkFirstName(conservative) {
    /* {{{ */
    var name = document.getElementById("ob_firstname").value;
    if (name == "") {
        if (!conservative) showError("checkFirstNameAlert");
        return "Please enter a first name.";
    }
    /* if everything is cool, show error positive */
    showCheck("checkFirstNameAlert");
    return "";
}
/* }}} */
function checkLastName(conservative) {
    /* {{{ */
    var name = document.getElementById("ob_lastname").value;
    if (name == "") {
        if (!conservative) showError("checkLastNameAlert");
        return "Please enter a last name.";
    }
    /* if everything is cool, show error positive */
    showCheck("checkLastNameAlert");
    return "";
}
/* }}} */
function checkZip(conservative) {
    /* {{{ */
    if (document.getElementById("ob_zip").disabled) {
        clearCheck("checkZipAlert");
        return "";
    }
    var country = document.getElementById("ob_country").value;
    var postalCode = document.getElementById("ob_zip").value;
    if ((country == "US" || country == "CA") && postalCode.length == 0) {
        showError("checkZipAlert");
        return "Please enter a postal code.";
    }
    /* if everything is cool, show error positive */
    showCheck("checkZipAlert");
    return "";
}
/* }}} */
function checkTZ(conservative) {
    /* {{{ */
    var tz = document.getElementById("ob_timezone").value;
    if (tz == 1) {
        if (!conservative) showError("checkTZAlert");
        return "Please select a timezone.";
    }
    /* if everything is cool, show error positive */
    showCheck("checkTZAlert");
    return "";
}
/* }}} */
function showError(error_id) {
    /* {{{ */
    document.getElementById(error_id).innerHTML = "&nbsp;<img src=\"/images/ico_cross_org.gif\" width=14 height=14><br />";
}
/* }}} */
function showCheck(error_id) {
    /* {{{ */
    document.getElementById(error_id).innerHTML = "&nbsp;<img src=\"/images/ico_check_blu.gif\" width=14 height=14><br /><span style=\"color:blue\">";
}
/* }}} */
function clearCheck(error_id) {
    /* {{{ */
    document.getElementById(error_id).innerHTML = "&nbsp;";
}
/* }}} */
function checkBirthdate() {
    /* {{{ */
    var month = getObject('-month').value;
    var day = getObject('-day').value;
    var year = 1900;
    if (month == 0 || year == 0) {
        return "Please enter your birthdate.";
    }
    /* verify user is over 13 years old */
    var birthDate = new Date(year, month - 1, day);
    /* (month is 0-based, yeesh) */
    var today = new Date();
    var age = today.getFullYear() - birthDate.getFullYear();
    if (birthDate.getMonth() > today.getMonth() ||
        (birthDate.getMonth() == today.getMonth() && birthDate.getDate() > today.getDate())) {
        age -= 1;
        /* not yet to my birthday this year */
    }
    /* Set the birthday in a hidden form field, so refreshing/coming back to the page will work */
    document.getElementById('birthday_hidden').value = "0000-" + getObject('-month').selectedIndex + '-' + getObject('-day').selectedIndex;
    if (age < 13) {
        return 'You must be at least 13 years of age.';
    }

    return "";
}
/* }}} */

function setBirthday() {
    /* {{{ */
    var hiddenBDay = document.getElementById('birthday_hidden');
    if (hiddenBDay.value !== "") {
        var month = getObject('-month');
        var day = getObject('-day');
        var year = getObject('-year');

        var values = hiddenBDay.value.split('-');
        var hiddenYear = parseInt(values[0], 10);
        var hiddenMonth = parseInt(values[1], 10);
        var hiddenDay = parseInt(values[2], 10);

        month.selectedIndex = hiddenMonth;
        month.onchange();
        day.selectedIndex = hiddenDay;
        year.selectedIndex = hiddenYear;
    }
}
/* }}} */

function checkGender() {
    /* {{{ */
    if (document.order_form.gender[0].checked || document.order_form.gender[1].checked)
        return "";
    return "Please select gender.";
}
/* }}} */

function checkAgree() {
    /* {{{ */
    if (document.order_form.agreement.checked)
        return "";
    return "Please agree to the Terms of Service.";
}
/* }}} */

function checkEmail(conservative, checkA) {
    /* {{{ */
    var emailObj = document.getElementById("ob_email");
    if (!emailObj) {
        return "";
    }

    var email = emailObj.value;
    if (email == "" || !isValidEmail(email)) {
        if (!conservative) showError("checkEmailAlert");
        document.getElementById('email_unavailable_text').style.display = 'none';
        return "This e-mail address is invalid or not available";
    }
    if (checkA) {
        MakeXMLRequest("/signup?t=ajax&avail=true&email=" + email, showAvailEmail);
    } else if (email_unavailable) {
        showError("checkEmailAlert");
        return "This e-mail address is invalid or not available";
    }
    return "";
}
/* }}} */

function checkMember(email) {
    /* {{{ */
    if (email != "" && isValidEmail(email)) {
        MakeXMLRequest("/signup?t=ajax&avail=true&email=" + email, redirectToSignIn);
    }
}
/* }}} */

function redirectToSignIn(restext) {
    /* {{{ */
    if (restext.match(/\s*Claimed\s*/)) {
        location.href = "/signin?t=brs&r=%2Fpo3%2F%3Fmodule%3Dbrs%26action%3DdoSendWiz%26step%3D2%26done%3D%2Fcontact_list%253Fview%253D10";
    }
}
/* }}} */

function checkPassword(conservative) {
    /* {{{ */
    var el = document.getElementById("ob_password");
    if (!el) return '';

    var pass = el.value;
    if (pass == "") {
        if (!conservative) showError("checkPasswordAlert");
        return "Please enter a password";
    }
    else if (pass.length > 0 && (pass.length < 6)) {
        showError("checkPasswordAlert");
        return "Please enter a password at least 6 characters long";
    }
    /* if everything is cool, show error positive */
    showCheck("checkPasswordAlert");
    return "";
}
/* }}} */

function checkConfirm(conservative) {
    /* {{{ */
    var str = checkPassword(conservative);
    if (str != "") {
        showError("checkConfirmAlert");
        return str;
    }
    var el = document.getElementById("ob_confirm");
    if (!el) return '';
    var pass = el.value;
    if (pass != document.getElementById("ob_password").value) {
        showError("checkConfirmAlert");
        return "The passwords do not match";
    }
    /* if everything is cool, show error positive */
    showCheck("checkConfirmAlert");
    return "";
}
/* }}} */



function checkData() { /* {{{ */
    var str;
    str = checkEmail(false, false);
    if (str != "" || email_unavailable) {
        alert(str);
        focusOn("ob_email");
        return false;
    }


    str = checkPassword(false);
    if (str != "") {
        alert(str);
        focusOn("ob_password");
        return false;
    }


    str = checkFirstName(false);
    if (str != "") {
        alert(str);
        focusOn("ob_firstname");
        return false;
    }

    str = checkLastName(false);
    if (str != "") {
        alert(str);
        focusOn("ob_lastname");
        return false;
    }

    if (email_unavailable) {
        alert("e-mail is unavailable");
        focusOn("ob_email");
        return false;
    }

    str = checkBirthdate();
    if (str != "") {
        alert(str);
        focusOn("-month");
        return false;
    }

    str = checkGender();
    if (str != "") {
        alert(str);
        focusOn("");
        return false;
    }

    return true;
}
/* }}} */

/* put check marks next to valid values */
function doOnload() { /* {{{ */
    checkEmail(true, true);
    checkPassword(true);
    checkFirstName(true);
    checkLastName(true);
    setBirthday();

    var tz = document.getElementById("ob_timezone");
    tz.value = guessTimezone();

    var emailObj = document.getElementById('ob_email');
    if (emailObj) {
        emailObj.focus();
    } else {
        var passObj = document.getElementById('ob_password');
        if (passObj) {
            passObj.focus();
        }
    }
}
/* }}} */

/* Timezone code stolen from po3 plaxo/i18n.js */

function guessTimezone() { // {{{
    var dateObj = new Date();
    dateObj.setMonth(12);
    dateObj.setDate(1);
    var decOffset = dateObj.getTimezoneOffset();

    dateObj.setMonth(6);
    var junOffset = dateObj.getTimezoneOffset();
    var dst = 0;
    var stdOffset, dstOffset;

    if (junOffset > decOffset) {
        stdOffset = junOffset;
        dstOffset = decOffset;
    } else {
        stdOffset = decOffset;
        dstOffset = junOffset;
    }
    if (dstOffset != stdOffset) dst = 1; // Determine DST recognition
    stdOffset *= -60;
    var index = 443; // US Eastern by default
    for (var k in timezones) {
        if (stdOffset == timezones[k][1]) {
            index = timezones[k][0]; // offset matches
            if (dst == timezones[k][2]) { // if DST matches, we have a perfect match and can stop searching
                break;
            }
        }
    }
    return index;
}
; // }}}
var timezones = [ // {{{
    [1001, -43200, 0],
    [414, -39600, 0],
    [441, -36000, 0], // US Hawaii
    [449, -32400, 1], // US Alaska
    [444, -28800, 1], // US Pacific
    [442, -25200, 0], // US Arizona
    [447, -25200, 1], // US Mountain
    [162, -25200, 1],
    [86, -21600, 0],
    [448, -21600, 1], // US Central
    [161, -21600, 1],
    [318, -21600, 0],
    [63, -18000, 0],
    [443, -18000, 1], // US Eastern
    [445, -18000, 0],
    [319, -14400, 1],
    [73, -14400, 0],
    [152, -14400, 1],
    [314, -12600, 1],
    [1003, -10800, 1],
    [53, -10800, 0],
    [1004, -10800, 1],
    [1005, -7200, 1],
    [279, -3600, 1],
    [278, -3600, 0],
    [40, 0, 0],
    [376, 0, 1],
    [328, 3600, 1],
    [378, 3600, 1],
    [333, 3600, 1],
    [373, 3600, 1],
    [1006, 3600, 0],
    [330, 7200, 1],
    [334, 7200, 1],
    [52, 7200, 1],
    [24, 7200, 0],
    [338, 7200, 1],
    [270, 7200, 0],
    [198, 10800, 1],
    [226, 10800, 0],
    [363, 10800, 1],
    [41, 10800, 0],
    [256, 12600, 1],
    [229, 14400, 0],
    [200, 14400, 1],
    [218, 16200, 0],
    [1007, 18000, 1],
    [220, 18000, 0],
    [1008, 19800, 0],
    [222, 20700, 0],
    [193, 21600, 1],
    [272, 21600, 0],
    [1010, 21600, 0],
    [238, 23400, 0],
    [201, 25200, 0],
    [223, 25200, 1],
    [271, 28800, 0],
    [215, 28800, 1],
    [258, 28800, 0],
    [292, 28800, 0],
    [257, 28800, 0],
    [253, 32400, 0],
    [260, 32400, 0],
    [248, 32400, 1],
    [307, 34200, 1],
    [300, 34200, 0],
    [304, 36000, 0],
    [309, 36000, 1],
    [408, 36000, 0],
    [298, 36000, 1],
    [247, 36000, 1],
    [227, 39600, 0],
    [432, 43200, 1],
    [219, 43200, 0],
    [1009, 46800, 0]
]; // }}}
