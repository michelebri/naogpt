import socket
import numpy as np
import time
import speech_recognition as sr
from pydub import AudioSegment
import io



recognizer = sr.Recognizer()
# Parametri del server a cui connettersi
SERVER_IP = '10.42.0.89'  # IP del robot NAO
SERVER_PORT = 4352  # Porta su cui il server sta ascoltando

# Crea un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connettiti al server
server_address = (SERVER_IP, SERVER_PORT)
sock.connect(server_address)


from google.cloud import speech


def transcribe_file(speech_file: str) -> speech.RecognizeResponse:
    """Transcribe the given audio file."""
    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)



    return (response.results)




try:
	# Invia il comando per iniziare la trasmissione audio
	start_command = "start"
	sock.sendall(start_command.encode('utf-8'))
	print("inviato")
	#while True:
		#   data = sock.recv(10024)
		#  print(data)
	time.sleep(15)
	give_size = "size"
	sock.sendall(give_size.encode('utf-8'))
	size = int(sock.recv(1000).decode('utf-8'))
	print(size)
	accumulated = 0
	data = b""
	stop_command = "audio"
	print("inviato audio")
	sock.sendall(stop_command.encode('utf-8'))
	while accumulated < size:
		part = sock.recv(16000)  # Receive data in chunks of 1024 byte
		accumulated += (len(part))
		data += part
	#print(data)
	audio_segment = AudioSegment(
		data=data,
		sample_width=2,  # 2 bytes for 16-bit audio
		frame_rate=16000,
		channels=1  # Assuming mono audio
	)

	# Export the audio segment to a bytes-like object
	audio_io = io.BytesIO()
	audio_segment.export(audio_io, format="wav")
	audio_io.seek(0)
	with open("output_audio.wav", "wb") as out_file:
		out_file.write(audio_io.read())
	print(transcribe_file("output_audio.wav"))

except:
	pass
