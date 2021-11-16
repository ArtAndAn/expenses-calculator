function send_form_data(form_data, api_url, redirect_url) {
    const xhr = new XMLHttpRequest();

    xhr.open('POST', api_url);
    xhr.send(form_data)

    xhr.onload = () => {
        check_auth_form(xhr, redirect_url)
    }
}

function check_auth_form(xhr, redirect_url) {
    const response = JSON.parse(xhr.response);
    if (response.message === 'error') {
        document.querySelectorAll('.alert').forEach(e => e.remove());
        for (const error in response.errors) {
            const form_field = document.getElementById(error)

            const error_div = document.createElement('div')
            error_div.className = 'alert alert-danger form-error-msg'

            const error_text = document.createElement('p')
            error_text.innerHTML = response.errors[error]

            error_div.append(error_text)

            form_field.append(error_div)
        }
    } else {
        window.location.replace(redirect_url)
    }
}