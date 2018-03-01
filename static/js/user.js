function user_password_form_check() {
    let password_form = document.forms.password_form;
    if (password_form["new"].value === password_form["repeat"].value) {
        return true;
    }
    else {
        return false;
    }
}

function repeat_password_check() {
    let password_form = document.forms.password_form;
    if (password_form["new"].value !== password_form["repeat"].value) {
        password_form["new"].style.borderColor = "rgba(255, 0, 0, 0.5)";
        password_form["repeat"].style.borderColor = "rgba(255, 0, 0, 0.5)";
    }
    else {
        password_form["new"].style.borderColor = "rgba(0, 0, 0, 0.5)";
        password_form["repeat"].style.borderColor = "rgba(0, 0, 0, 0.5)"
    }
}