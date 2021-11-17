function check_user() {
    const xhr = create_xhr('GET', '/user')
    xhr.send()

    xhr.onload = () => {
        const user_status_resp = JSON.parse(xhr.response)
        user_data = user_status_resp.user

        create_page_header(user_data)
    }
}

function get_csrf() {
    const xhr = create_xhr('GET', '/get_csrf')
    xhr.send()
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
            '<div class="header-line  me-auto"></div>' +
            '<a href="/login" class="nav-link header-link">Login</a>' +
            '<div class="header-line"></div>' +
            '<a href="/register" class="nav-link header-link register-link">Register</a>');
    } else {
        header.insertAdjacentHTML('beforeend',
            '<div class="header-line"></div>' +
            '<a href="/charts" class="nav-link header-link">Charts</a>' +
            '<div class="header-line"></div>' +
            '<a href="/add_expenses" class="nav-link header-link">Add expenses</a>' +
            '<div class="header-line  me-auto"></div>' +
            '<p class="header-text">Hi, ' + user.username + '! You\'re logged in</p>' +
            '<div class="header-line"></div>' +
            '<a href="/logout" id="logout" class="nav-link header-link register-link">LogOut</a>');
    }
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

function authorized_page() {
    if (!user_data) {
        setTimeout(authorized_page, 100)
    } else {
        if (!user_data.is_authenticated) {
            window.location.replace('/errors/403')
        }
    }
}

function add_category_field() {
    const add_button = document.getElementById('add_category_field')

    add_button.addEventListener('click', function () {
        const form = document.getElementById('new_category')
        const field_name = 'category' + form.length
        form.insertAdjacentHTML('beforeend',
            '<input type="text" id="form-category" name="' + field_name + '" class="form-control popup_input"' +
            ' placeholder="Enter category name:" required/>')
    })
}

function add_expenses_field() {
    const add_button = document.getElementById('add_expenses_field')

    add_button.addEventListener('click', function () {
        let fields_count = document.getElementsByClassName('expenses-form-line').length + 1
        const fields_div = document.getElementById('expenses_fields')
        fields_div.insertAdjacentHTML('beforeend',
            '<div class="expenses-form-line">' +
            '<label for="category-select" class="expenses-form-text">Select category:</label>' +
            '<select class="form-select px-2 py-0" id="category-select" name="category' + fields_count + '">' +
            '<option>Shop</option>' +
            '<option>Market</option>' +
            '<option>Pharmacy</option>' +
            '<option>Gym</option>' +
            '</select>' +
            '<label for="amount" class="expenses-form-text">Enter amount:</label>' +
            '<input type="number" id="amount" placeholder="0.00" step="0.01"  min="0" max="100000"  ' +
            'name="spend' + fields_count + '"/>' +
            '<label for="date" class="expenses-form-text">Enter date:</label>' +
            '<input type="date" id="date"  name="date' + fields_count + '"/>' +
            '</div>')
    })
}

function send_category() {
    const send_button = document.getElementById('send_category')

    send_button.addEventListener('click', function () {
        const form = document.getElementById('new_category')
        const form_data = new FormData();

        for (let field = 1; field < form.length; field++) {
            let field_name = 'category' + field
            let field_data = form[field_name].value
            form_data.append(field_name, field_data)
        }

        send_form_data(form_data, '/new_category', '/')
    })
}

const API_URL = 'http://0.0.0.0:8000'
let user_data

get_csrf()
check_user()
