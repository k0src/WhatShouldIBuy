document.addEventListener('DOMContentLoaded', function() {
    var loadingDiv = document.getElementById('loading');
    loadingDiv.style.display = 'none';

    var accordingDiv = document.getElementById('according');
    accordingDiv.style.display = 'none';

    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();
        loadingDiv.style.display = 'block';

        var inputValue = document.getElementById('searchInput').value;
        fetch('/process_input/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({'input_text': inputValue})
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            loadingDiv.style.display = 'none';
            accordingDiv.style.display = 'block';

            console.log('Data received:', data);
            
            var resultDiv = document.getElementById('result');

            resultDiv.innerHTML = '';

            data.recommendations.forEach(function(recommendation) {

                var recommendationDiv = document.createElement('div');

                recommendationDiv.classList.add('recommendations');

                recommendationDiv.innerHTML = `
                    <h2><a href="${recommendation.link}" target="_blank">${recommendation.name}</a></h2>
                    <p><img src="${recommendation.image}" alt="Product Image"></p>
                `;

                resultDiv.appendChild(recommendationDiv);

                console.log('New div created:', recommendation);
            });
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