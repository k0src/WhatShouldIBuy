document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();
        var inputValue = document.getElementById('searchInput').value;
        console.log("Input value:", inputValue);  // debug

        fetch('/process_input/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({'input_text': inputValue})
        })
        .then(response => {
            console.log('Response received:', response); //debuf
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data); // degub
            document.getElementById('result').innerText = data.processed_text;
        })
        .catch(error => console.error('Error:', error));
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
