document.addEventListener("DOMContentLoaded", () => {
    const apikey = "978e545fbf6fe3b6907fdb005b004e0e";
    const apiurl = "https://api.openweathermap.org/data/2.5/weather?units=metric&q=";

    const SearchBox = document.querySelector(".search input");
    const SearchBtn = document.querySelector(".search button");
    const weatherIcon = document.querySelector(".weather-icon");

    async function checkWeather(city) {
        if (!city) {
            alert("Please enter a city name");
            return;
        }

        try {
            const response = await fetch(apiurl + city + `&appid=${apikey}`);

            if (!response.ok) {
                throw new Error("City not found");
            }

            const data = await response.json();

            document.querySelector(".city").innerHTML = data.name;
            document.querySelector(".temp").innerHTML = Math.round(data.main.temp) + "°C";
            document.querySelector(".humidity").innerHTML = data.main.humidity + "%";
            document.querySelector(".wind").innerHTML = data.wind.speed + " km/h";

            if(data.weather[0].main == "Clouds") {
                weatherIcon.src = "images/clouds.png";
                }
                else if(data.weather[0].main == "Clear"){
                weatherIcon.src = "images/clear.png";
                }
                else if(data.weather[0].main == "Rain"){
                weatherIcon.src = "images/rain.png";
                }
                else if(data.weather[0].main == "Drizzle"){
                weatherIcon.src = "images/drizzle.png";
                }
                else if(data.weather[0].main == "Mist") {
                weatherIcon.src = "images/mist.png";
                }
               
                document.querySelector(".weather").style.display = "block";
        } catch (error) {
            alert(error.message);
        }

    }

    SearchBtn.addEventListener("click", () => {
        checkWeather(SearchBox.value);
    });

    SearchBox.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            checkWeather(SearchBox.value);
        }
    });
});
