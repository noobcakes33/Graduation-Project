import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
import pyttsx

engine = pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

from sklearn.pipeline import Pipeline
# fix random seed for reproducibility
#seed = 7
#numpy.random.seed(seed)
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
estimator = KerasClassifier(build_fn=baseline_model)
kfold = KFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, X, dummy_y, cv=kfold)
print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

def prediction(x):
    pred = baseline_model().predict(numpy.load(x)/1000)
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
        predicted_sign = "rubbish"
    elif max(pred[0]) == pred[0][6]:
        predicted_sign = "We are"
    elif max(pred[0]) == pred[0][7]:
        predicted_sign = "inventors"
    return predicted_sign
'''
for i in range(1,51):
    pred = prediction('coordinates_output_'+str(i)+'.npy')
    print(pred)
    engine.say(str(pred))
    engine.runAndWait()
'''
import h5py

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")