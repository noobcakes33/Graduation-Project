import os
import pyglet
import pyaudio
import speech_recognition as sr

name = ''
fileName = ''

sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer()

with sr.Microphone(device_index = 0, sample_rate = sample_rate, 
                        chunk_size = chunk_size) as source:
    #wait for a second to let the recognizer adjust the 
    #energy threshold based on the surrounding noise level
    r.adjust_for_ambient_noise(source)
    print("Say Something")
    #listens for the user's input
    audio = r.listen(source)
         
    try:
        name = r.recognize_google(audio)
        #fileName = name+'.gif'
        print(name)
     
    #error occurs when google could not understand what was said
     
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
     
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# name = 'hello good morning how are you doing are you ok'
o = name.split(' ')

gif_files = filter(lambda x: x.endswith('.gif'), os.listdir('C:/Users/Snow/Desktop/Graduation Project/Database/'))
print(gif_files)
F = []
for i in gif_files:
    F.append(i.split('.gif')[0])
print (F)

output = []
for i in range(len(o)):
    try:
        if o[i] in F:
            output.append(o[i])
        elif o[i]+' '+o[i+1] in F:
            output.append(o[i]+' '+o[i+1])
        elif o[i]+' '+o[i+1]+' '+o[i+2] in F:
            output.append(o[i]+' '+o[i+1]+' '+o[i+2])
        elif o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3] in F:
            output.append(o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3])
        elif o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3]+' '+o[i+4] in F:
            output.append(o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3]+' '+o[i+4])
        elif o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3]+' '+o[i+4]+' '+o[i+5] in F:
            output.append(o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3]+' '+o[i+4]+' '+o[i+5])
        else:
            print("nothing")
    except:
        pass
print(output)


#gif = ['hello.gif','are you ok.gif']
while True:
    for i in output:
        animation = pyglet.resource.animation('Database/'+str(i)+'.gif')
        sprite = pyglet.sprite.Sprite(animation)

        win = pyglet.window.Window(width=sprite.width, height=sprite.height)

        @win.event
        def on_draw():
            win.clear()
            sprite.draw()

        def close(event):
            win.close()

        pyglet.clock.schedule_once(close, 1.5)

        pyglet.app.run()
    break

