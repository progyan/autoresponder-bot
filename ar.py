import os
import time
import datetime
import openai
import urllib.request
import json

apikey = ""
botid = ""
botinfo = ""
INITSTR = """
Дальше приведён диалог """
INITSTR2 = """, далее называемого П с тобой, автоответчиком, далее называемым А.
"""
LOGSTART = """

---------------------------
LOG AT """
INPUTMAXLEN = 1024
ANSWERMAXLEN = 512

with open("keys.txt", "r", encoding="utf-8") as f:
    apikey = f.readline()
    botid = f.readline()
    botinfo = f.readline()

openai.api_key = apikey
completion = openai.Completion()
chat_log = {}
names = {}
link = "https://api.telegram.org/bot" + botid + "/getUpdates"
lastmsgid = 0
lastlogminute = 0

with open("ar-save.txt", "r", encoding="utf-8") as f:
    lastmsgid = int(f.readline())

def constructlogstr(chatid):
    if chatid not in chat_log.keys():
        chat_log[chatid] = []
    cl = chat_log[chatid]
    logstr = ""
    for i in range(0, len(cl)):
        entry = cl[len(cl) - 1 - i][0] + ": " + cl[len(cl) - 1 - i][1] + "\n"
        if len(logstr) >= INPUTMAXLEN:
            break
        logstr = entry + logstr
    return logstr

def ask(question, chatid):
    prompt = f'{INITSTR + names[chatid] + INITSTR2 + constructlogstr(chatid)}П: {question}\nА:'
    print(prompt)
    response = completion.create(
        prompt=prompt, engine="text-davinci-003", temperature=0.7,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=ANSWERMAXLEN)
    answer = response.choices[0].text.strip()
    return answer

def getmessage(j, i):
    if "message" not in j["result"][i].keys():
        return False, False
    msginfo = j["result"][i]["message"]
    msg = msginfo["text"]
    if "П:" in msg or "А:" in msg:
        os.system("sh ./send.sh " + str(msginfo["chat"]["id"]) + " \"⚠️ [Ошибка при обработке ввода. Попробуйте другой ввод.]\" " + botid)
        return False, False
    names[msginfo["chat"]["id"]] = "пользователя " + msginfo["chat"]["first_name"]
    return msg, msginfo["chat"]["id"]

def getlastmessage():
    global lastmsgid

    with urllib.request.urlopen(link) as f:
        txt = f.read()
        j = json.loads(txt)
        if len(j["result"]) - 1 > lastmsgid:
            lastmsgid += 1
            return getmessage(j, lastmsgid)
        else:
            return False, False

def writelog():
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(LOGSTART + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        for key in chat_log.keys():
            f.write("CHAT " + str(key) + ":\n")
            f.write(constructlogstr(key))
        f.close()
    with open("ar-save.txt", "w", encoding="utf-8") as f:
        f.write(str(lastmsgid))
        f.close()


# init missing
with urllib.request.urlopen(link) as f:
    txt = f.read()
    j = json.loads(txt)
    for i in range(lastmsgid + 1):
        prompt, chatid = getmessage(j, i)
        if not prompt:
            continue
        if chatid not in chat_log.keys():
            chat_log[chatid] = []
        chat_log[chatid].append(("П", prompt))

while True:
    prompt, chatid = getlastmessage()
    if prompt:
        now = datetime.datetime.now()
        if now.minute != lastlogminute:
            writelog()
        answer = ask(prompt, chatid)
        print(prompt)
        print(answer)
        chat_log[chatid].append(("П", prompt))
        chat_log[chatid].append(("А", answer))
        os.system("sh ./send.sh " + str(chatid) + " \"" + answer.replace("\"", "\\\"") + "\" " + botid)
    time.sleep(1)