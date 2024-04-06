document.addEventListener('DOMContentLoaded', function() {
    var loadingDiv = document.getElementById('loading');
    loadingDiv.style.display = 'none';

    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();

        var inputValue = document.getElementById('searchInput').value.trim(); 

        if (!inputValue) {
            var searchDiv = document.querySelector('.search');
            searchDiv.classList.add('shake');
            setTimeout(function() {
                searchDiv.classList.remove('shake');
            }, 500);
            return; 
        }

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
            
            var resultDiv = document.getElementById('result');

            resultDiv.innerHTML = '';

            data.recommendations.forEach(function(recommendation) {

                var recommendationDiv = document.createElement('div'); 
                recommendationDiv.classList.add('recommendations');
                
                recommendationDiv.style.padding = '10px';
                recommendationDiv.style.marginBottom = '20px';

                recommendationDiv.innerHTML = `
                    <h2>${recommendation.name}</h2>
                    <p><a href="${recommendation.link}" target="_blank"><img src="${recommendation.image}" alt="Product Image"></a></p>
                `;

                resultDiv.appendChild(recommendationDiv);

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