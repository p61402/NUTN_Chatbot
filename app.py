import os, sys
from flask import Flask, request
import requests
from pymessenger import Bot
import query3
import know2
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

                send_actions(sender_id)

                if messaging_event.get('message'):
                    if 'quick_reply' in messaging_event['message'] and 'payload' in messaging_event['message']['quick_reply']:
                        payload_command, payload_type = messaging_event['message']['quick_reply']['payload'].split()
                        if payload_type == 'follow-up':
                            c, k = query3.find_class(payload_command)
                            if c and k:
                                with open('record/test_pattern.txt', 'r') as pattern_file:
                                    pattern, keywords = pattern_file.read().splitlines()
                                    pattern, keywords = pattern.split(), keywords.split()
                                for i in range(len(pattern)):
                                    if pattern[i] == "N":
                                        pattern[i], keywords[i] = c, k
                                keywords = [keyword[4:] for keyword in keywords]
                                question = "".join(keywords)
                                send_text_message(sender_id, "問句: " + question)
                                response, match_number = query3.question(question)
                                if match_number == 52 or match_number == 87:
                                    if response:
                                        send_quick_reply(sender_id, response, match_number)
                                    else:
                                        send_text_message(sender_id, "沒東西")
                                elif match_number == 1:
                                    send_text_message(sender_id, response[0])
                                    send_button(sender_id, response[1])
                                else:
                                    if match_number != -1 and match_number != -2:
                                        response = ", ".join(response)
                                    send_text_message(sender_id, response)
                        elif payload_type == 'normal':
                            response, match_number = query3.question(payload_command)
                            if match_number == 52 or match_number == 87:
                                if response:
                                    send_quick_reply(sender_id, response, match_number)
                                else:
                                    send_text_message(sender_id, "沒東西")
                            elif match_number == 1:
                                send_text_message(sender_id, response[0])
                                send_button(sender_id, response[1])
                            else:
                                if match_number != -1 and match_number != -2:
                                    response = ", ".join(response)
                                send_text_message(sender_id, response)
                        else:
                            send_text_message(sender_id, "無法度")
                    # Extracting text message
                    elif 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                        # Echo
                        response, match_number = query3.question(messaging_text)
                        if match_number == 52 or match_number == 87:
                            if response:
                                send_quick_reply(sender_id, response, match_number)
                            else:
                                send_text_message(sender_id, "沒東西")
                        elif match_number == 1:
                            send_text_message(sender_id, response[0])
                            send_button(sender_id, response[1])
                        else:
                            if match_number != -1 and match_number != -2:
                                response = ", ".join(response)
                            send_text_message(sender_id, response)

                elif messaging_event.get('postback'):
                    if 'payload' in messaging_event['postback']:
                        payload_command = messaging_event['postback']['payload']
                    else:
                        payload_command = 'no payload'

                    if payload_command == "do nothing":
                        send_text_message(sender_id, "收到!")
                    else:
                        payload_command = payload_command.split()
                        if payload_command[0] == 'detail':
                            properties = know2.instance_all_properties(payload_command[1])
                            response_text = payload_command[1][4:] + "的資料如下：" + "\n"
                            for p in properties:
                                response_text += p[0] + " : " + p[1] + "\n"
                            send_text_message(sender_id, response_text)
                        elif payload_command[0] == 'relation':
                            relations = know2.instance_relation(payload_command[1])
                            response_text = payload_command[1][4:] + "的關係如下：" + "\n"
                            for r in relations:
                                response_text += r + "\n"
                            send_text_message(sender_id, response_text)

    return "ok", 200


def send_actions(sender_id):
    response_message = json.dumps({
      "recipient": {
        "id": sender_id
      },
      "sender_action": "typing_on"
    })

    call_send_api(sender_id, response_message)


def send_text_message(sender_id, message_data):
    response_message = json.dumps({"recipient": {"id": sender_id},
                                   "message": {"text": message_data}})
    call_send_api(sender_id, response_message)


def send_button(sender_id, instance):
    data = json.dumps({
        "recipient": {
            "id": sender_id
            },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "已經查詢到" + instance[4:] + "的相關資訊。",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "列出" + instance[4:] + "的資料",
                            "payload": "detail" + " " + instance
                        },
                        {
                            "type": "postback",
                            "title": "查看" + instance[4:] + "的關係",
                            "payload": "relation" + " " + instance
                        },
                        {
                            "type": "postback",
                            "title": "什麼也不做",
                            "payload": "do nothing"
                        }
                    ]
                }
            }
        }
    })

    call_send_api(sender_id, data)


def send_quick_reply(sender_id, options, match_number):
    if match_number == 87:
        payload = 'follow-up'
    elif match_number == 52:
        payload = 'normal'
    else:
        print("Something wrong in send_quick_reply.")
    quick_reply = []
    for option in options:
        quick_reply.append({
            "content_type": "text",
            "title": option,
            "payload": option + ' ' + payload,
        })

    data = json.dumps({
                "recipient": {"id": sender_id},
                "message": {"text": "請選擇!",
                            "quick_replies": quick_reply}
            })
    call_send_api(sender_id, data)


def send_list(sender_id, elements):
    data_list = json.dumps({"recipient": {"id": sender_id},
      "message": {
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"generic",
            "elements":[
               {
                "title":"我是QOO",
                "image_url":"http://2.bp.blogspot.com/-bubsfFNnyzA/VfqziE7FOyI/AAAAAAAGK_M/lfuJ6hFnc48/s1600/TF003323.png",
                "subtitle":"哈哈哈哈哈哈",
                "default_action": {
                  "type": "web_url",
                  "url": "https://www.google.com",
                  "messenger_extensions": True,
                  "webview_height_ratio": "tall",
                },
                "buttons":[
                  {
                    "type":"web_url",
                    "url":"https://www.google.com",
                    "title":"View Website"
                  },{
                    "type":"postback",
                    "title":"Start Chatting",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD"
                  }
                ]
              }
            ]
          }
        }
      }
    })
    call_send_api(sender_id, data_list)


def call_send_api(sender_id, message_data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(token=PAGE_ACCESS_TOKEN)
    req = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=message_data)
    print("[{}] Reply to {}: {}", req.status_code, sender_id, message_data)


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True, port=80)
