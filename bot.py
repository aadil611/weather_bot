
import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])



@app.command("/show-weather")
def show_weather_command(ack, body):
    ack()

    cities = ['Ahmedabad', 'Bengaluru', 'Chennai', 'Delhi', 'Hyderabad', 
                'Jaipur', 'Kanpur', 'Kolkata', 'Mumbai', 'Pune', 'Surat']

    city_options = [ {"label":city,"value":city} for city in cities ]

    app.client.dialog_open(
        trigger_id=body["trigger_id"],
        
        dialog=
            {
            "callback_id": "submit_weather",
            "title": "Select a city name",
            "submit_label": "Request",
            "state": "test",
            "elements": [
                {
                "label": "city",
                "type": "select",
                "name": "city",
                "options": city_options
                }
            ]
            }

        )





@app.action("submit_weather")
def handle_submission(ack, body, logger,say):
    ack()

    api_key = os.environ.get('OPENWEATHER_API_KEY')
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city = body["submission"]["city"]
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    
    response = requests.get(complete_url)

    # Parse the response and extract the weather information
    weather_data = {}
    x = response.json()

    if x["cod"] != "404":
        data = x["main"]
        weather_data["temp"] = data["temp"]
        weather_data["pressure"] = data["pressure"]
        weather_data["humidity"] = data["humidity"]
        weather_data["description"] = x["weather"][0]["description"]


    # Send a message to the user with the weather information
    user_id = body["user"]["id"]
    say(f"The weather in {city} is: {weather_data}")



if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    