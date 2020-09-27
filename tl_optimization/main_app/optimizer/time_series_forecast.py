# Headers ........................................................................
# multivariate multi-step encoder-decoder lstm example
from numpy import array
from numpy import hstack
from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed

import os

# Preparing Data .................................................................
# split a multivariate sequence into samples
class Time_Series_Forecast:
    def __init__(self, intersection_name="", data=[], n_steps_in=3, n_steps_out=2 ):
        super().__init__()
        self.intersection_name = intersection_name
        self.model_location = "/trained_models/" + intersection_name 
        self.data = data
        self.testdata = []
        self.dataset = []
        self.n_steps_in = n_steps_in
        self.n_steps_out = n_steps_out
        print("Constructor >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def split_sequences(self, sequences, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            # check if we are beyond the dataset
            if out_end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix:out_end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        print("Split_sequences >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return array(X), array(y)

    def prepare_data(self):
        # define input sequence
        if len(self.data) == 0:
            in_seq1 = array([10, 20, 30, 40, 50, 60, 70, 80, 90])
            in_seq2 = array([15, 25, 35, 45, 55, 65, 75, 85, 95])
            out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])

            # convert to [rows, columns] structure
            in_seq1 = in_seq1.reshape((len(in_seq1), 1))
            in_seq2 = in_seq2.reshape((len(in_seq2), 1))
            out_seq = out_seq.reshape((len(out_seq), 1))
            
            # horizontally stack columns
            self.dataset = hstack((in_seq1, in_seq2, out_seq))
            # choose a number of time steps
            self.n_steps_in, self.n_steps_out = 3, 2
        else:
            seqArray = [ array(road_data) for road_data in self.data]
            # convert to [rows, columns] structure
            seqReshaped = [ seq.reshape((len(seq), 1)) for seq in seqArray ]
            if len( self.data ) == 2:
                self.dataset = hstack((seqReshaped[0], seqReshaped[1]))
            elif len( self.data ) == 3:
                self.dataset = hstack((seqReshaped[0], seqReshaped[1], seqReshaped[2]))
            else:
                self.dataset = hstack((seqReshaped[0], seqReshaped[1], seqReshaped[2], seqReshaped[3]))
        print("Prepare_data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # covert into input/output
        self.X, self.y = self.split_sequences( self.dataset, self.n_steps_in, self.n_steps_out)
        # the dataset knows the number of features, e.g. 2
        self.n_features = self.X.shape[2]
        return self.n_features


    # Data Forecasting ...........................................................................
    def forecast_model(self):
        # define model
        self.model = Sequential()
        self.model.add(LSTM(200, activation='relu', input_shape=(self.n_steps_in, self.n_features)))
        self.model.add(RepeatVector(self.n_steps_out))
        self.model.add(LSTM(200, activation='relu', return_sequences=True))
        self.model.add(TimeDistributed(Dense(self.n_features)))
        self.model.compile(optimizer='adam', loss='mse')
        # fit model
        self.model.fit(self.X, self.y, epochs=300, verbose=0)
        #self.model.save(self.model_location)
        print("Forecast_model >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return self.model

    # demonstrate prediction ......................................................................
    def prediction(self):
        x_input = array([[60, 65, 125], [70, 75, 145], [80, 85, 165]])
        if len(self.testdata) != 0:
            x_input = array(self.testdata)
            #self.model = keras.models.load_model(self.model_location)

        x_input = x_input.reshape((1, self.n_steps_in, self.n_features))
        yhat = self.model.predict(x_input, verbose=0)
        print(yhat)
        print("Prediction >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return yhat


    def predict_traffic(self):
        # Separate train/test data ....
        for road in self.data:
            roadtest = [ road.pop() for i in range(24) ]
            self.testdata.append(roadtest)

        # Prepare data ..................
        self.prepare_data()
        print("-------------------------------------------------------")

        # Training the Forecast Model .... 
        self.forecast_model()
        print("-------------------------------------------------------")

        # Predict traffic ................
        results = self.prediction()
        print("-------------------------------------------------------")
        print( results )
        return results

if __name__ == "__main__":
    
    intersection_name = "mrknowitall"
    tsf_services = Time_Series_Forecast(intersection_name=intersection_name)
    tsf_services.prepare_data()
    tsf_services.forecast_model()

    tsf_services = None
    tsf_services = Time_Series_Forecast(intersection_name=intersection_name)
    n_features = tsf_services.prepare_data()
    predict_data = [[60, 65, 125], [70, 75, 145], [80, 85, 165]]
    tsf_services.prediction( predict_data, n_features )
