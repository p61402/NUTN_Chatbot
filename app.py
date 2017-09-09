import os, sys
from flask import Flask, request
import requests
from pymessenger import Bot
import query3
import json

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAOBui2KGS4BADs57JIgWgZC0UL0t1xlZAEBarJj7WdpfefacA9jpjnnfXWeHghVumh6KkmJdQBpQCh1xaMjAysZBtZAEyGYax6W8motCHBKN8oeKPb7XxZAOagj9Kb5KsxZBK70BKc6IOCaVt3l1TuDr2pfzPczWzFsuus9Cz3CLMNsZAsClB3"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    # Echo
                    response, match_number = query3.question(messaging_text)
                    if match_number == 15:
                        send_quick_reply(sender_id, response)
                    else:
                        send_text_message(sender_id, response)

    return "ok", 200


def send_text_message(sender_id, message_data):
    response_message = json.dumps({"recipient": {"id": sender_id},
                                   "message": {"text": message_data}})
    call_send_api(sender_id, response_message)


def send_quick_reply(sender_id, options):
    quick_reply = []
    for option in options:
        quick_reply.append({
            "content_type": "text",
            "title": option,
            "payload": option,
        })

    data = json.dumps({
                "recipient": {"id": sender_id},
                "message": {"text": "hello",
                            "quick_replies": quick_reply}
            })
    call_send_api(sender_id, data)


def call_send_api(sender_id, message_data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(token=PAGE_ACCESS_TOKEN)
    req = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=message_data)
    print("[{}] Reply to {}: {}", req.status_code, sender_id, message_data)


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug = True, port = 80)
