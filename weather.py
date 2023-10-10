import requests
from bs4 import BeautifulSoup


def collect_data():
    response = requests.get("https://weather.com/en-ZA/weather/today/l/0d8f0367de2da09c33f8b20775e5b982a75dd19ce46de81ba5e1e7373e12d532")
    news_24_data = response.text

    soup = BeautifulSoup(news_24_data, "html.parser")
    more_soup = BeautifulSoup(str(soup.find("section", class_="card Card--card--2AzRg Card--containerQuery--T7772")), "html.parser")

    state_of_day = [tag.string for tag in more_soup.select(".Ellipsis--ellipsis--3ADai")]

    temperature_span_tags = more_soup.select(".Column--temp--1sO_J")
    temperatures = []

    for tag in temperature_span_tags:
        temperature = str(tag)[-29] + str(tag)[-28]
        if 20 > int(temperature) > 10:
            temperatures.append(temperature + "°" + "(Cool)")
        elif 20 <= int(temperature) < 30:
            temperatures.append(temperature + "°" + "(Warm)")
        elif int(temperature) >= 30:
            temperatures.append(temperature + "°" + "(Hot)")
        else:
            temperatures.append(temperature + "°" + "(Cold)")

    state_of_atmosphere = [tag.string for tag in more_soup.find_all("title")]

    precipitation_span_tags = [str(tag) for tag in more_soup.find_all("span", class_="Column--precip--3JCDO")]
    precipitation = []
    for tag in precipitation_span_tags:
        if "Column--precip--3JCDO" in tag and "Accessibility--visuallyHidden--H7O4p" in tag:
            try:
                int(tag[-10])
                try:
                    int(tag[-11])
                    precipitation.append(f"{tag[-11]}{tag[-10]}{tag[-9]}%")
                except ValueError:
                    precipitation.append(f"{tag[-10]}{tag[-9]}%")
            except ValueError:
                precipitation.append(f"{tag[-9]}%")
        elif "Column--precip--3JCDO" in tag:
            precipitation.append("0%")

    gauteng_weather_conditions = [
        f"In the {state_of_day[num].lower()} the weather conditions will be: {temperatures[num]}, {state_of_atmosphere[num]}, with {precipitation[num]} chance of rain.\n\n"
        for num in range(4)]

    new_gauteng_weather_conditions = "".join(gauteng_weather_conditions)

    return new_gauteng_weather_conditions


class MakeSoup:
    def __init__(self):
        self.collected_data = collect_data()


print("Weather Conditions for Rietondale, Gauteng:\n")
print(MakeSoup().collected_data)

