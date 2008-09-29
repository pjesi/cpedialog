YAHOO.util.Event.onDOMReady(function() {
    var email_unavailable = false;
    var username_unavailable = false;
    function checkData() {
        var str;
        str = checkEmail(false, false);
        if (str != "" || email_unavailable) {
            alert(str);
            focusOn("email");
            return false;
        }

        str = checkUsername(false, false);
        if (str != "" || username_unavailable) {
            alert(str);
            focusOn("username");
            return false;
        }


        str = checkPassword(false);
        if (str != "") {
            alert(str);
            focusOn("password");
            return false;
        }


        str = checkFirstName(false);
        if (str != "") {
            alert(str);
            focusOn("firstname");
            return false;
        }

        str = checkLastName(false);
        if (str != "") {
            alert(str);
            focusOn("lastname");
            return false;
        }

        if (email_unavailable) {
            alert("e-mail is unavailable");
            focusOn("email");
            return false;
        }

        str = checkBirthdate();
        if (str != "") {
            alert(str);
            focusOn("birthday");
            return false;
        }

        str = checkGender();
        if (str != "") {
            alert(str);
            focusOn("");
            return false;
        }

        return true;
    };

    function checkEmail(conservative, checkA) {
        var emailObj = document.getElementById("email");
        if (!emailObj) {
            return "";
        }
        var email = emailObj.value;
        if (email == "" || !validatorEmail(email)) {
            if (!conservative) showError("checkEmailAlert");
            document.getElementById('email_unavailable_text').style.display = 'none';
            return "This e-mail address is invalid or not available";
        }
        if (checkA) {
            isEmailOrUsernameAvailiable("email", email);
        } else if (email_unavailable) {
            showError("checkEmailAlert");
            return "This e-mail address is invalid or not available";
        } else {
            document.getElementById('email_unavailable_text').style.display = 'none';
            showCheck("checkEmailAlert")
        }
        return "";
    };

    function checkUsername(conservative, checkA) {
        var usernameObj = document.getElementById("username");
        if (!usernameObj) {
            return "";
        }
        var username = usernameObj.value;
        if (username == "" || !validatorUsername(username)) {
            if (!conservative) showError("checkUsernameAlert");
            document.getElementById('username_unavailable_text').style.display = 'none';
            return "This username is invalid or not available";
        }
        if (checkA) {
            isEmailOrUsernameAvailiable("username", username);
        } else if (username_unavailable) {
            showError("checkUsernameAlert");
            return "This username is invalid or not available";
        } else {
            document.getElementById('username_unavailable_text').style.display = 'none';
            showCheck("checkUsernameAlert");
        }
        return "";
    };

    function isEmailOrUsernameAvailiable(property, value) {
        var propertyFirstUpperCased = property.substring(0, 1).toUpperCase() + property.substring(1);
        var callback = {
            success:function(o) {
                var result = YAHOO.lang.JSON.parse(o.responseText);
                if (result.match(/\s*True\s*/)) {
                    document.getElementById(property + '_unavailable_text').style.display = 'none';
                    if (property == "email") {
                        email_unavailable = false;
                    } else if (property == "username") {
                        username_unavailable = false;
                    }
                    showCheck("check" + propertyFirstUpperCased + "Alert");
                } else if (result.match(/\s*Invalid\s*/)) {
                    showError("check" + propertyFirstUpperCased + "Alert");
                    if (property == "email") {
                        email_unavailable = true;
                    } else if (property == "username") {
                        username_unavailable = true;
                    }
                    document.getElementById(property + '_unavailable_text').style.display = '';
                }
            },
            failure:handleFailure
        };
        var req = YAHOO.util.Connect.asyncRequest('POST', '/rpc?action=Is' + propertyFirstUpperCased + 'Available', callback, property + '=' + value);
    };

    function checkPassword(conservative) {
        var el = document.getElementById("password");
        if (!el) return '';

        var pass = el.value;
        if (pass == "") {
            if (!conservative) showError("checkPasswordAlert");
            return "Please enter a password";
        }
        else if (pass.length > 0 && (pass.length < 6)) {
            showError("checkPasswordAlert");
            document.getElementById("password_unavailable_text").style.display = '';
            return "Please enter a password at least 6 characters long";
        }
        document.getElementById("password_unavailable_text").style.display = 'none';
        showCheck("checkPasswordAlert");
        return "";
    };

    function checkFirstName(conservative) {
        var name = document.getElementById("firstname").value;
        if (name == "") {
            if (!conservative) showError("checkFirstNameAlert");
            return "Please enter a first name.";
        }
        showCheck("checkFirstNameAlert");
        return "";
    };

    function checkLastName(conservative) {
        var name = document.getElementById("lastname").value;
        if (name == "") {
            if (!conservative) showError("checkLastNameAlert");
            return "Please enter a last name.";
        }
        showCheck("checkLastNameAlert");
        return "";
    };

    function checkBirthdate() {
        var month = document.getElementById('month').value;
        var day = document.getElementById('day').value;
        var year = document.getElementById('year').value;
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
        document.getElementById('birthday').value = year + "-" + month + '-' + day;
        if (age < 13) {
            return 'You must be at least 13 years of age.';
        }

        return "";
    };

    function checkGender() {
        if (document.getElementById("gender_Female").checked || document.getElementById("gender_Male").checked)
            return "";
        return "Please select gender.";
    };

    function doSigninExisting(property, value) {
        location.href = '/login?' + property + '=' + encodeURIComponent(value);
    };

    //binding event to the form element.
    YAHOO.util.Event.addListener('email', 'blur', function(){checkEmail(false, true)});

    YAHOO.util.Event.on('username', 'blur', function(){checkUsername(false, true)});

    YAHOO.util.Event.on('password', 'blur', function(){checkPassword(false)});

    YAHOO.util.Event.on('firstname', 'blur', function(){checkFirstName(false)});

    YAHOO.util.Event.on('lastname', 'blur', function(){checkLastName(false)});

    YAHOO.util.Event.onAvailable("country", function() {
        var country = document.getElementById("country");
        for (var i = 0; i < countrys.length; i++) {
            var option = new Option(countrys[i].display, countrys[i].value);
            country.options[country.options.length] = option;
            if (countrys[i].value == document.getElementById("country_hidden").value) {
                country.options[country.options.length - 1].selected = true;
            }
        }
    });

    var birthday = document.getElementById("birthday").value;
    var year_, month_, day_;
    if (birthday != "" && birthday.indexOf("-") != -1) {
        var birth_nums = birthday.split("-");
        year_ = birth_nums[0];
        month_ = birth_nums[1];
        day_ = birth_nums[2];
    };

    YAHOO.util.Event.onAvailable("year", function() {
        var year = document.getElementById("year");
        var current_year = new Date().getFullYear();
        year.options[0] = new Option('Year', '');
        for (var i = 0; i < 100; i++) {
            var option = new Option(current_year, current_year);
            year.options[year.options.length] = option;
            if (current_year == year_) {
                year.options[year.options.length - 1].selected = true;
            }
            current_year--;
        }
    });

    YAHOO.util.Event.onAvailable("month", function() {
        var month = document.getElementById("month");
        for (var i = 0; i < month_list.length; i++) {
            var option = new Option(month_list[i].display, month_list[i].value);
            month.options[month.options.length] = option;
            if (month_list[i].value == month_) {
                month.options[month.options.length - 1].selected = true;
            }
        }
        function fnCallback(e) {
            var daysPerMonth = new Array(31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
            var selectedMonth = month[month.selectedIndex].value;
            var day = document.getElementById("day");
            if (selectedMonth != "") {
                var selectedDay = "";
                if (day.selectedIndex != -1) {
                    selectedDay = day[day.selectedIndex].value;
                }
                clearSelectOptions("day");
                for (var i = 1; i <= daysPerMonth[selectedMonth - 1]; i++) {
                    day.options[day.options.length] = new Option(i, i);
                }
                if (selectedDay != "") {
                    selectByValue("day", selectedDay);
                } else if (day_ != "") {
                    selectByValue("day", day_)
                }

            }
        }
        YAHOO.util.Event.addListener(month, "change", fnCallback);
    });

    YAHOO.util.Event.on('userForm', 'submit', function(e) {
        if (checkData()) {
            document.getElementById('userForm').submit();
        }
    });
});