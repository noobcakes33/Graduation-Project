import h5py
from keras.models import model_from_json
from multi_signs import *

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
#loaded_model.fit(X, dummy_y, epochs=10, batch_size=50, verbose=0)

print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
