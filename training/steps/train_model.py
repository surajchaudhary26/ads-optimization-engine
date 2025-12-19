from sklearn.linear_model import LinearRegression


def train(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model
