import numpy as np
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
import pyttsx
from keras.models import model_from_json

engine = pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# load dataset
dataframe = pandas.read_csv("training_signs.csv", header=None)
dataset = dataframe.values
X = dataset[:,0:800].astype(float)/1000
Y = dataset[:,800]

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)

# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(250, input_dim=800, activation='tanh'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(100, activation='tanh'))
    model.add(Dense(10, activation='tanh'))
    model.add(Dense(8, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, dummy_y, epochs=20, batch_size=50, verbose=0)
    return model

model = baseline_model()

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
score = loaded_model.evaluate(X, dummy_y, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

def prediction(x):
    pred = model.predict(np.load(x)/1000)
    if max(pred[0]) == pred[0][0]:
        predicted_sign = "Hello"
    elif max(pred[0]) == pred[0][1]:
        predicted_sign = "I don't know"
    elif max(pred[0]) == pred[0][2]:
        predicted_sign = "Thank you"
    elif max(pred[0]) == pred[0][3]:
        predicted_sign = "Good Morning"
    elif max(pred[0]) == pred[0][4]:
        predicted_sign = "How are you doing?"
    elif max(pred[0]) == pred[0][5]:
        predicted_sign = "inventors"
    elif max(pred[0]) == pred[0][6]:
        predicted_sign = "rubbish"
    elif max(pred[0]) == pred[0][7]:
        predicted_sign = "we are"
    return predicted_sign
'''
for i in range(13,22):
    predicted_sign = prediction('coordinates_output_'+str(i)+'.npy')
    print(i, ': ', predicted_sign)
    engine.say(str(predicted_sign))
    engine.runAndWait()
'''



def modelPredict(x):
    pred = model.predict(x/1000)
    if max(pred[0]) == pred[0][0]:
        predicted_sign = "Hello"
    elif max(pred[0]) == pred[0][1]:
        predicted_sign = "I don't know"
    elif max(pred[0]) == pred[0][2]:
        predicted_sign = "Thank you"
    elif max(pred[0]) == pred[0][3]:
        predicted_sign = "Good Morning"
    elif max(pred[0]) == pred[0][4]:
        predicted_sign = "How are you doing?"
    elif max(pred[0]) == pred[0][5]:
        predicted_sign = "inventors"
    elif max(pred[0]) == pred[0][6]:
        predicted_sign = "rubbish"
    elif max(pred[0]) == pred[0][7]:
        predicted_sign = "we are"
    return predicted_sign