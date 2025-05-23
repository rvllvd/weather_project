const input = document.getElementById('city-input');
const suggestions = document.getElementById('suggestions');
const weatherDiv = document.getElementById('weather');

input.addEventListener('input', () => {
    const q = input.value.trim();
    if (q.length < 2) {
        suggestions.innerHTML = '';
        return;
    }
    fetch(`/api/autocomplete/?q=${encodeURIComponent(q)}`)
        .then(res => res.json())
        .then(data => {
            suggestions.innerHTML = '';
            data.results.forEach(city => {
                const div = document.createElement('div');
                div.textContent = city;
                div.onclick = () => {
                    input.value = city;
                    suggestions.innerHTML = '';
                };
                suggestions.appendChild(div);
            });
        });
});

function getWeather() {
    const city = input.value.trim();
    if (!city) {
        return;
    }
    fetch('/api/weather/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({city})
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            weatherDiv.innerHTML = `<p style="color:#ff8080;">Ошибка: ${data.error}</p>`;
            return;
        }
        weatherDiv.innerHTML = `
            <h2>Погода в ${data.city}</h2>
            <p>Время: ${data.time}</p>
            <p>Температура: ${data.temperature} °C</p>
            <p>Ветер: ${data.windspeed} м/с</p>
            <p>Влажность: ${data.humidity} %</p>
        `;
    });
}
