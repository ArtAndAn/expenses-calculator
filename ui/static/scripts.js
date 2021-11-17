function check_user() {
    const xhr = create_xhr('GET', '/user')
    xhr.send()

    xhr.onload = () => {
        const user_status_resp = JSON.parse(xhr.response)
        const user = user_status_resp.user

        create_page_header(user)
    }
}

function get_csrf() {
    const xhr = create_xhr('GET', '/get_csrf')
    xhr.send()
}

function send_form_data(form_data, api_url, redirect_url) {
    const xhr = create_xhr('POST', api_url)
    xhr.send(form_data);

    xhr.onload = () => {
        check_auth_form(xhr, redirect_url);
    }
}

function check_auth_form(xhr, redirect_url) {
    const response = JSON.parse(xhr.response);
    if (response.message === 'error') {
        document.querySelectorAll('.alert').forEach(e => e.remove());
        for (const error in response.errors) {
            const form_field = document.getElementById(error);

            const error_div = document.createElement('div');
            error_div.className = 'alert alert-danger form-error-msg';

            const error_text = document.createElement('p');
            error_text.innerHTML = response.errors[error];

            error_div.append(error_text);

            form_field.append(error_div);
        }
    } else {
        window.location.replace(redirect_url);
    }
}

function create_page_header(user) {
    const header = document.querySelector('header');

    if (user.is_authenticated === false) {
        header.insertAdjacentHTML('beforeend',
            '<div class="header-line  me-auto"></div>\n' +
            '<a href="/login" class="nav-link header-link">Login</a>\n' +
            '<div class="header-line"></div>\n' +
            '<a href="/register" class="nav-link header-link register-link">Register</a>');
    } else {
        header.insertAdjacentHTML('beforeend',
            '<div class="header-line"></div>\n' +
            '<a href="/charts" class="nav-link header-link">Charts</a>\n' +
            '<div class="header-line"></div>\n' +
            '<a href="/add_expenses" class="nav-link header-link">Add expenses</a>\n' +
            '<div class="header-line  me-auto"></div>' +
            '<p class="header-text">Hi, ' + user.username + '! You\'re logged in</p>' +
            '<div class="header-line"></div>\n' +
            '<a href="/logout" id="logout" class="nav-link header-link register-link">LogOut</a>\n');
    }
}

function get_cookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function create_xhr(method, url) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, API_URL + url)
    xhr.withCredentials = true
    xhr.setRequestHeader('X-CSRFToken', get_cookie('csrftoken'))
    return xhr
}

function logout() {
    const xhr = create_xhr('POST', '/logout')
    xhr.send()

    xhr.onload = () => {
        const response = JSON.parse(xhr.response)
        if (response.message === 'logged out') {
            window.location.replace('/');
        }
    }
}

const API_URL = 'http://0.0.0.0:8000'

get_csrf()
check_user()
