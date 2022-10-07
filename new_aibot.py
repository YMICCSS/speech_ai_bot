import glob
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import eel
import pretty_errors
import requests
import os
from web_crawler import craw
import win32api

#Azure  cosmes資料庫位置以及金鑰
endpoint = "cosmes資料庫位置"
key = '這邊要輸入cosmes資料庫服務金鑰'
client = CosmosClient(endpoint, key)
database_name = 'Cosmes'
database = client.create_database_if_not_exists(id=database_name)
container_name = 'Animation_Speech'
# container = AI預測出結果後，答案的資料庫容器
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/Question"),
    offer_throughput=400
)

@eel.expose
def main ():
    # 說出檔案D:\speech\ssml.xml內的指令，唸出來,只有部分地區的金鑰才能合成神經語言，使用前請先檢查創建服務的地區
    speech_config = SpeechConfig(subscription="82d504596ee74646aeac63433427b804", region="japanwest")
    audio_config = AudioOutputConfig(use_default_speaker=True)
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    ssml_string = open(".\speech\ssml.xml", "r", encoding="utf-8-sig").read()
    # 開始識別語音並轉成文字，要修改下面兩個參數
    speech_key, service_region = "輸入語音識別服務 speech_key", "japanwest"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="zh-TW")
    print("請問您有甚麼問題?~~~")

    # 產生辨別出的文字
    result = speech_recognizer.recognize_once()
    result = result.text
    print("讀取到的內容 : "+result)

    # 到本機AI服務5800port取得預測結果
    r = requests.get(f'http://127.0.0.1:5800/{result}')
    predictions = json.loads(r.text).get("answer")
    # 到資料庫中撈取正確答案
    query = "SELECT * FROM c WHERE c.Question IN ('%s')" % (predictions)
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    I_get_answer = items[0].get("Answer")

    # 先以「課程介紹」這個分類，來代替未來「我要上課」這個分類，開啟簽到表
    if predictions =="課程介紹":
        lession_data = craw()
        lessions = lession_data
        length = len(lession_data)
        eel.print_lession(lessions, length)
        # 找到答案更換 Oresult 檔案後發出回應
        import xml.etree.ElementTree as ET
        ET.register_namespace("", "https://www.w3.org/2001/10/synthesis")
        tree = ET.parse(".\speech\Oresult.xml")  #修改文件
        root = tree.getroot()
        root[0][0].text = "請點擊課程名稱，開啟當天簽到表"
        tree.write(".\speech\Oresult.xml", encoding="utf-8")
        # 說出檔案D:\speech\Oresult.xml內的指令，唸出來,只有部分地區的金鑰才能合成神經語言，使用前請先檢查創建服務的地區
        speech_config = SpeechConfig(subscription="輸入語音識別服務 speech_key", region="japanwest")
        audio_config = AudioOutputConfig(use_default_speaker=True)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        ssml_string = open(".\speech\Oresult.xml", "r", encoding="utf-8-sig").read()
        result3 = synthesizer.speak_ssml_async(ssml_string).get()
        print("讀取結束")
        return I_get_answer
    else:
        eel.update_display(I_get_answer)
        # 找到答案更換 Oresult 檔案後發出回應
        import xml.etree.ElementTree as ET
        ET.register_namespace("", "https://www.w3.org/2001/10/synthesis")
        tree = ET.parse(".\speech\Oresult.xml")  # 修改文件
        root = tree.getroot()
        root[0][0].text = I_get_answer
        tree.write(".\speech\Oresult.xml", encoding="utf-8")
        # 說出檔案D:\speech\Oresult.xml內的指令，唸出來,只有部分地區的金鑰才能合成神經語言，使用前請先檢查創建服務的地區
        speech_config = SpeechConfig(subscription="輸入語音識別服務 speech_key", region="japanwest")
        audio_config = AudioOutputConfig(use_default_speaker=True)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        ssml_string = open(".\speech\Oresult.xml", "r", encoding="utf-8-sig").read()
        result3 = synthesizer.speak_ssml_async(ssml_string).get()
        print("讀取結束")
        return I_get_answer

# 按鈕按按下課表的按鈕後，會觸動javascript的函式，函式會再來觸動此python函式，開啟指定的簽到表
@eel.expose
def open_sign_in_form(file_path):
    # 讀取簽到表中的檔案，以取得檔案名稱
    sign_in_form = glob.glob("sign_in_form/*.csv")
    sign_in_form_list = []
    for item in sign_in_form:
        item = item.replace("\\", "/")
        sign_in_form_list.append(item)
    win32api.ShellExecute(0, 'open', os.getcwd()+'\\'+"sign_in_form\\"+file_path+".csv", '', '',1)

eel.init(os.getcwd()+'\web')  # 定義html文件所在文件夾名稱
eel.start(os.getcwd()+'\web'+'\main.html',size = (600,730))


