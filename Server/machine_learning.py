from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

import data_process

x_scaler = StandardScaler()
y_scaler = StandardScaler()


def model_training():
    columns = ["Date", "Open", "High"]
    df = data_process.get_df("NVidia_stock_history.csv", columns)  # df = [Year, Month, Day, Open, High]

    numpy_dataset = df.to_numpy()

    X = numpy_dataset[:, :4]

    y = numpy_dataset[:, 4]

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    y_train = y_train.reshape((-1, 1))
    y_test = y_test.reshape((-1, 1))

    x_train = x_scaler.fit_transform(x_train)

    y_train = y_scaler.fit_transform(y_train)

    # We then create the model and train it.
    batch_size = 32
    epochs = 20

    model = Sequential()

    model.add(Dense(64, activation="relu", input_shape=(x_train.shape[1],)))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.2))

    # Note here, we only use one neuron in the output
    # layer and use a linear activation function.
    model.add(Dense(1, activation="linear"))

    # We use a Mean Squared Error - mse - loss.
    model.compile(loss="mse", optimizer=SGD())

    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_split=0.1)

    # With the model trained we can evaluate it on the test set
    x_test = x_scaler.transform(x_test)
    y_test = y_scaler.transform(y_test)

    print("\n|| ============== model evaluation ============== ||")
    model.evaluate(x_test, y_test)

    # If we have a new sample we can obtain the median
    # house price like:

    # new_sample = [[2025, 3, 17, 128.1199951171875]]
    # new_sample_normalised = x_scaler.transform(new_sample)
    # raw_output = model.predict(new_sample_normalised)
    # output = y_scaler.inverse_transform(raw_output)
    # print("============== output ==============")
    # print(output)

    return model


def evaluate_model(model, year, month, day, open_value):
    new_sample = [[year, month, day, open_value]]
    new_sample_normalised = x_scaler.transform(new_sample)
    raw_output = model.predict(new_sample_normalised)
    output = y_scaler.inverse_transform(raw_output)

    return output


if __name__ == "__main__":
    trained_model = model_training()
    result = evaluate_model(trained_model, 2025, 3, 17, 120)
    print(result)
