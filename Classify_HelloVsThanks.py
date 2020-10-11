from keras.models import Sequential
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# load dataset
dataset = numpy.loadtxt("output_hello_thanks.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:]/1000
Y = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

print(X)
print(len(X))
print(X.shape)
print(Y)
print(len(Y))

# create model
model = Sequential()
model.add(Dense(12, input_dim=800, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, epochs=600, batch_size=8,  verbose=2)
# calculate predictions
#predictions = model.predict(X)
# round predictions
#rounded = [round(x[0]) for x in predictions]
#print(rounded)

#test_set = numpy.loadtxt("test_data.csv", delimiter=",")
#X_test = test_set[:]/1000
#predictions = model.predict(X_test)
#rounded = [round(x[0]) for x in predictions]
rounded = []
for i in range(1,30):
    x = numpy.load('coordinates_output_'+str(i)+'.npy')
    y = model.predict(x)
    rounded.append(y)
for i in rounded:
    if i == 1:
        print("Hello")
    else:
        print("Thanks")




