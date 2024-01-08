import json
import os
import socket
import sys
import time
import redis
import boto3
import numpy as np
import pickle
from PIL import Image
from botocore.config import Config

from tool import TimeStatistics, send_msg, recv_msg, anonymize_server_port


def extract_entities_from_message(message):
    redis_client = redis.Redis(
        host="222.20.94.67",
        port=6379)

    if not redis_client.exists(message[:10]):
        client = boto3.client(service_name='comprehendmedical',
                              aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                              aws_secret_access_key=os.environ["AWS_ACCESS_KEY_ID"],
                              region_name="us-west-2",
                              config=Config(proxies={'https': 'http://222.20.68.152:7890'}))
        response = client.detect_phi(Text=message)
        redis_client.set(message[:10], pickle.dumps(response))
    return pickle.loads(redis_client.get(message[:10]))


def resize():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    message = "Pt is a 45-year-old male who is a junior high school mathematics teacher. His past medical history includes surgery on the left pretibial area in September 2017. Today he complained of right-sided chest pain and shortness of breath. The chief complaint began last night. The pain was sharp in nature, accompanied by shortness of breath and worsened with activity. The patient described that he suddenly felt a sharp pain during the teaching process, and the chest pain radiated to the right shoulder. He had no accompanying symptoms, including vomiting, dizziness, or loss of consciousness. The patient had no history of heart disease or other chronic diseases. He does not smoke and drinks alcohol occasionally. Over the past week, the patient had experienced mild dizziness and general malaise at home but had not sought medical advice. He has no recent cold symptoms and no cough or sputum production. Not currently taking any medications. Physical examination: The patient is conscious and the pain level is 7/10. Vital signs were normal, heart rate was 76 beats/min, blood pressure was 120/80mmHg, respiratory rate was 18 beats/min, and body temperature was 36.8 degrees Celsius. Cardiac auscultation revealed that S1 and S2 were normal and no murmur was heard. The lungs were clear on auscultation and no abnormal breath sounds were heard. The abdomen is flat and soft, with no tenderness or masses. There was no swelling of the limbs and no edema of the lower limbs. Neurological examination showed no obvious abnormalities. Based on the patient's symptoms and signs, acute coronary syndrome may be suspected, and it is recommended to conduct an ECG examination immediately and arrange an emergency CT scan for chest pain. At the same time, aspirin chewable tablets and nitroglycerin were given. The patient's electrocardiogram and vital signs need to be closely monitored, and further cardiac enzymology tests and cardiac color Doppler ultrasound should be considered. The patient and family have been informed that they may need to be hospitalized for further treatment and are currently awaiting further test results."
    response = extract_entities_from_message(message)
    data = pickle.dumps({"message": message, "entities": response['Entities']})
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("222.20.94.67", anonymize_server_port))
    send_msg(client_socket, data)
    data = recv_msg(client_socket)
    if data.decode() != "OK":
        raise RuntimeError("Not OK!")
    client_socket.close()
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == '__main__':
    resize()
