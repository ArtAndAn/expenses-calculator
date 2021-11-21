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

function create_xhr(method, url, content_type) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, API_URL + url)
    xhr.withCredentials = true
    xhr.setRequestHeader('X-CSRFToken', get_cookie('csrftoken'))
    if (content_type) {
        xhr.setRequestHeader('Content-Type', content_type)
    }
    return xhr
}

function send_form_data(form_data, api_url, redirect_url, content_type = null, form_name = 'auth') {
    const xhr = create_xhr('POST', api_url, content_type)
    xhr.send(form_data);

    xhr.onload = () => {
        if (form_name === 'auth') {
            check_auth_form(xhr, redirect_url);
        } else if (form_name === 'category') {
            check_category_form(xhr, redirect_url)
        } else if (form_name === 'expenses') {
            check_expenses_form(xhr, redirect_url)
        }
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

function check_expenses_form(xhr, redirect_url) {
    const response = JSON.parse(xhr.response)
    if (response.message === 'error') {
        document.querySelectorAll('.alert').forEach(e => e.remove());
        const fields_div = document.getElementById('expenses_fields')

        const error_message_div = document.createElement('div')
        error_message_div.className = 'alert alert-danger popup_error'

        const error_message = document.createElement('p')
        error_message.innerHTML = 'Check that all fields are filled and amount is less than 1 million'

        error_message_div.append(error_message)
        fields_div.after(error_message_div)
    } else {
        window.location.replace(redirect_url)
    }
}

function check_inputs(form, value, error) {
    for (let field = 1; field < form.length; field++) {
        let field_name = 'category' + field
        let field_data = form[field_name].value
        let form_field = document.getElementsByName(field_name)[0]
        if (!field_data) {
            let last_element_number = form.length - 1
            let last_element_name = 'category' + last_element_number
            let last_elem = document.getElementsByName(last_element_name)[0]
            show_error(last_elem, 'You can not send empty fields')
        } else if (field_data === value) {
            show_error(form_field, error)
        }
    }
}

function show_error(field, error) {
    const error_div = document.createElement('div');
    error_div.className = 'alert alert-danger popup_error';

    const error_text = document.createElement('p');
    error_text.innerHTML = error;

    error_div.append(error_text);

    field.after(error_div);
}

function check_category_form(xhr, redirect_url) {
    const response = JSON.parse(xhr.response);
    if (response.message === 'error') {
        document.querySelectorAll('.alert').forEach(e => e.remove());
        form = document.getElementById('new_category')

        for (let field in response.errors) {
            for (let error in response.errors[field]) {
                let error_info = response.errors[field][error]

                check_inputs(form, error, error_info)
            }
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
            '<select class="form-select px-2 py-0" id="category-select" name="category_select' + fields_count + '"></select>' +
            '<label for="amount" class="expenses-form-text">Enter amount:</label>' +
            '<input type="number" id="amount" placeholder="0.00" step="0.01"  min="0" max="1000000"  ' +
            'name="spend' + fields_count + '"/>' +
            '<label for="date" class="expenses-form-text">Enter date:</label>' +
            '<input type="date" id="date"  name="date' + fields_count + '"/>' +
            '</div>')
        get_categories()
    })
}

function send_category() {
    const send_button = document.getElementById('send_category')

    send_button.addEventListener('click', function () {
        const form = document.getElementById('new_category')
        const form_data = [];

        for (let field = 1; field < form.length; field++) {
            let field_name = 'category' + field
            let field_data = form[field_name].value
            let user = user_data.username

            form_data.push({'name': field_data, 'user': user})
        }

        const data_to_api = JSON.stringify(form_data)
        send_form_data(data_to_api, '/expenses/category', '/add_expenses', 'application/json',
            'category')
    })
}

function send_expenses() {
    const send_button = document.getElementById('send_expenses')

    send_button.addEventListener('click', function () {
        const form = document.getElementById('expenses_form')
        const form_data = []
        const rows = (form.length - 3) / 3
        const user = user_data.username

        for (let field = 1; field < rows + 1; field++) {
            let category_field_name = 'category_select' + field
            let category_field_data = form[category_field_name].value

            let spend_field_name = 'spend' + field
            let spend_field_data = form[spend_field_name].value

            let date_field_name = 'date' + field
            let date_field_data = form[date_field_name].value

            form_data.push({
                'category': category_field_data,
                'spend': spend_field_data,
                'date': date_field_data,
                'user': user
            })
        }
        const data_to_api = JSON.stringify(form_data)
        send_form_data(data_to_api, '/expenses/expenses', '/charts', 'application/json',
            'expenses')
    })
}

function get_categories() {
    const xhr = create_xhr('GET', '/expenses/category')
    xhr.send()
    xhr.onload = () => {
        const response = JSON.parse(xhr.response)
        const all_selects = document.querySelectorAll('select')

        response.forEach((category) => {
            const option = document.createElement('option');
            option.value = category['name'];
            option.innerHTML = category['name'];
            all_selects.forEach((x) => {
                x.appendChild(option)
            })
        })
    }
}

function buttons_eventlisteners() {
    const total_time_button = document.getElementById('total_time')
    const last_month_button = document.getElementById('last_month')
    const last_week_button = document.getElementById('last_week')
    const time_period_select_button = document.getElementById('send_time_period')

    total_time_button.addEventListener('click', () => {
        create_expenses_page('total')
    })
    last_month_button.addEventListener('click', () => {
        create_expenses_page('month')
    })
    last_week_button.addEventListener('click', () => {
        create_expenses_page('week')
    })
    time_period_select_button.addEventListener('click', () => {
        get_time_period_data(time_period_select_button)
    })
}

function get_time_period_data(button) {
    const form = document.getElementById('time_period_form')
    const period = form.from.value + ':' + form.until.value
    create_expenses_page(period)
}

function remove_prev_data() {
    document.getElementById('expenses-div').innerHTML = ''
    while (document.getElementById('line_after_charts')) {
        document.getElementById('line_after_charts').remove()
    }
    while (document.getElementById('table_title')) {
        document.getElementById('table_title').remove()
    }
    while (document.querySelector('table')) {
        document.querySelector('table').remove()
    }
}

function create_expenses_page(period) {
    const xhr = create_xhr('GET', '/expenses/expenses?period=' + period)
    xhr.send()
    xhr.onload = () => {
        const response = JSON.parse(xhr.response)
        if (response.message === 'ok') {
            document.getElementsByClassName('btn-close')[0].click()
            const expenses_div = document.getElementById('expenses-div')

            remove_prev_data()

            expenses_div.className = 'expenses_div'
            const round_image_url = 'http://0.0.0.0:8000/expenses/expenses/roundimage?period=' + period
            const bar_image_url = 'http://0.0.0.0:8000/expenses/expenses/barimage?period=' + period
            expenses_div.insertAdjacentHTML('beforeend',
                '<img src="' + round_image_url + '" alt="Expenses round chart">')
            expenses_div.insertAdjacentHTML('beforeend',
                '<div class="vertical_line"></div>')
            expenses_div.insertAdjacentHTML('beforeend',
                '<img src="' + bar_image_url + '" alt="Expenses bar chart">')
            setTimeout(() => {
                draw_expenses_table(response.data)
            }, 500)
        } else {
            const form = document.getElementById('time_period_form')

            const prev_error = document.getElementsByClassName('alert alert-danger popup_error')[0]
            if (prev_error) {
                prev_error.remove()
            }

            form.insertAdjacentHTML('afterend',
                '<div class="alert alert-danger popup_error">' +
                '<p>' + response.error + '</p>' +
                '</div>')
        }
    }
}

function draw_expenses_table(response) {
    const main_content_div = document.getElementsByClassName('expenses_page_content')[0]
    main_content_div.insertAdjacentHTML('beforeend', '<hr id="line_after_charts">')
    main_content_div.insertAdjacentHTML('beforeend', '<h4 class="mb-3" id="table_title">Your last expenses in selected time period</h4>')
    main_content_div.insertAdjacentHTML('beforeend', '<table class="table expenses_table">\n' +
        '  <thead>\n' +
        '    <tr>\n' +
        '      <th scope="col">Date</th>\n' +
        '      <th scope="col">Category</th>\n' +
        '      <th scope="col">Amount</th>\n' +
        '    </tr>\n' +
        '  </thead>\n' +
        '  <tbody  id="table_body">\n' +
        '  </tbody>\n' +
        '</table>')
    const table = document.getElementById('table_body')
    for (let expense in response) {
        table.insertAdjacentHTML('beforeend',
            '<tr>' +
            '<td>' + response[expense].date + '</td>' +
            '<td>' + response[expense].category + '</td>' +
            '<td>' + response[expense].spend + '</td>' +
            '</tr>')
    }
}

const API_URL = 'http://0.0.0.0:8000'
let user_data

get_csrf()
check_user()
