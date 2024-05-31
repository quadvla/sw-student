"""
This file contains the implementation of a VoiceAgent class that interacts with the OpenAI API to perform speech-to-text, text generation, and text-to-speech tasks. It also includes an example usage of the VoiceAgent class.

The VoiceAgent class has the following methods:
- text_generation: Generates a response to a user's question using the OpenAI API.

"""

from openai import OpenAI
import pyaudio

import base64
import requests
import argparse

import cv2
import time
import os

PERSONA = "My name is vision 60. I'm quadruped robot and architected to allow rapid adaptation to new environments \
            using our proprietary blind-mode control core that mimics how mammals operate across a range of urban and natural environments. \
            Even if the environment is completely unknown, vision sensors degrade or fail, you can be assured that when I fail, \
            slip or fall, it will get right back up and continue moving. \
            My goal is to make me an indispensable tool and continuously push the limits \
            to improve its ability to walk, run, crawl, climb and eventually swim in complex environments that our customers must operate in, \
            day in and day out. Ultimately, I am made to keep our warfighters, workers of harm’s way. \
            I will response to your question up to 150 tokens.\
            I can speak English, Korean, Japenese."


class GPTAgent:
    def __init__(
        self, args, base_path=os.path.dirname(os.path.abspath(__file__))
    ):
        self.with_image = args.with_image
        self.image_path = args.image_path
        self.stream_address = args.stream_address
        if (self.stream_address == '0'):
            self.stream_address = 0
        self.api_key = args.api_key
        self.client = OpenAI(api_key=self.api_key)


    # Function to encode the image
    def encode_image(self):
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def save_image_from_camera(self):
        cap = cv2.VideoCapture(self.stream_address)
        if not cap.isOpened():
            print("Error opening video stream or file")
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(self.image_path, frame) 
        cap.release()

    def loop(self):
        while True:
            print("\nEnter the question. Break for 'q' : ")
            question = input()
            time.sleep(1)
            if question == "q":
                print("Bye!")
                break
            elif question.strip():
                print(f"Question: {question}")
                print(f"Input with image: {self.with_image}")
                if self.with_image:
                    self.save_image_from_camera()
                answer = self.text_generation(question, self.with_image)
                print(f"Answer: {answer}")
 
    def text_generation(self, question, with_image):
        if with_image:
            base64_image = self.encode_image()

            headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {"role": "system", "content": PERSONA},
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": question,
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
                ]
                }
            ],
            "max_tokens": 1000
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            return response.json()['choices'][0]['message']['content']
        else:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": PERSONA},
                    {"role": "user", "content": question},
                ],
            )

            return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--with_image', action="store_true")
    parser.add_argument('--api_key', type=str, required=True, default="", help='API_KEY from the terminal command "echo $OPENAI_API_KEY"')
    parser.add_argument('--output', type=str, default="output.mp4")
    parser.add_argument('--image_path', type=str, default="./media/front_right.jpg")
    parser.add_argument('--stream_address', type=str, default="http://192.168.168.105:8080/stream?topic=/argus/ar0234_front_right/image_raw", help='default camera address for Vision60. for webcam use 0')
    args = parser.parse_args()
    
    ga = GPTAgent(args)
    ga.loop()

if __name__ == "__main__":
    main()
