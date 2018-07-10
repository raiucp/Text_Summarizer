import speech_recognition as sr
import wave
import contextlib
from os import path
from multiprocessing.dummy import Pool as ThreadPool
def get_audio(audio_name):
	r = sr.Recognizer()
	meeting_audio = sr.AudioFile(audio_name)
	"""
	#testing with a part of audio
	with meeting_audio as source:
	    audio = r.record(source, duration=20)

	print(r.recognize_google(audio))
	"""

	fname = audio_name

	with contextlib.closing(wave.open(fname,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames/float(rate)
		#print(duration)
	audio_list = {}
	time = 0

	def recognize(audio):
	    #assert(type(audio)=='speech_recognition.AudioData')
	    #print(type(audio))
	    try:
	        value = r.recognize_google(audio,language='en')
	        return value
	    except sr.UnknownValueError:
	        for i in range(0,10):
	            try:
	                value = r.recognize_google(audio,language='en')
	                return value
	            except sr.UnknownValueError:
	                pass
	        print("Couldn't understand the audio")
	    except sr.RequestError as e:
	        print("Could not request results; {0}".format(e))
	i=1
	while time<duration:
	    with meeting_audio as src:
	        r.adjust_for_ambient_noise(src, duration=0.5)
	        audio_list['a'+str(i)]=(r.record(src,offset=time,duration = 30))
	        time = time+30
	        i+=1
	#print(type(audio_list['a1']))
	#print(recognize(audio_list['a1']))
	pool = ThreadPool(15)
	results = pool.map(recognize, list(audio_list.values()))

	pool.close()
	pool.join()
	file = open('output.txt','w')
	for item in results:
	    if item is not None:
	        file.write("%s " % item+'.')
	f.close()
	#print(results)
