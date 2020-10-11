import pyttsx

engine = pyttsx.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)
what_to_say = ['Hello', 'We are', 'inventors', 'from', 'higher technological institute',
               'and this is', 'our graduation project']

engine.say([i for i in what_to_say])
engine.runAndWait()
