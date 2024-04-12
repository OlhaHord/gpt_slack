import os
from slack_bolt import App
import openai

# Ініціалізація Slack App
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Функція для звернення до OpenAI API
def ask_openai(question):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # або інша доступна модель
            messages=[{"role": "system", "content": "The following is a conversation with a helpful assistant."},
                      {"role": "user", "content": question}]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Помилка при запиті до OpenAI: {str(e)}"

# Слухач подій, який реагує на згадки бота
@app.event("app_mention")
def handle_mention_events(body, say):
    event = body["event"]
    text = event["text"]
    response = ask_openai(text)
    say(response)

@app.route("/", methods=["GET", "POST"])
def handle_request():
    return "Hello World", 200

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
