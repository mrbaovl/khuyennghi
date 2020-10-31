import os
import sys

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error


class CB(object):
    """docstring for CB"""

    def __init__(self, Y_data, Y_test, Y_mon):
        self.Y_data = Y_data
        self.Y_test = Y_test
        self.Y_mon = Y_mon
        # number of users and items. Remember to add 1 since id starts from 0
        self.n_users = 32  # int(np.max(self.Y_data[:, 0])) + 1
        self.n_items = 52  # int(np.max(self.Y_data[:, 1])) + 1
        self.d = 5  # data dimension
        self.W = np.zeros((self.d, self.n_users))
        self.b = np.zeros((1, self.n_users))

    def get_items_rated_by_user(self, user_id):
        """
    get all items which are rated by user n, and the corresponding ratings
    """
        # y = self.Y_data_n[:,0] # all users (may be duplicated)
        # item indices rated by user_id
        # we need to +1 to user_id since in the rate_matrix, id starts from 1
        # while index in python starts from 0
        ids = np.where(self.Y_data[:, 0] == user_id)[0]
        item_ids = self.Y_data[ids, 1].astype(np.int32)  # index starts from 0
        ratings = self.Y_data[ids, 2]
        return (item_ids, ratings)

    def pred_all(self):
        for n in range(self.n_users):
            ids, scores = self.get_items_rated_by_user(n)
            clf = Ridge(alpha=0.01, fit_intercept=True)
            Xhat = self.Y_mon[ids, 1:]
            clf.fit(Xhat, scores)
            self.W[:, n] = clf.coef_
            self.b[0, n] = clf.intercept_
        self.Yhat = self.Y_mon[:, 1:].dot(self.W) + self.b

    def preList(self):
        self.predList = []
        for n in range(self.n_users):
            ids = np.where(self.Y_data[:, 0] == n)[0]
            items_rated_by_u = self.Y_data[ids, 1].tolist()
            for i in range(self.n_items):
                if i not in items_rated_by_u:
                    temp = [];
                    rating = self.Yhat[i]
                    rating = rating[n]
                    temp.append(n)
                    temp.append(i)
                    temp.append(rating)
                    self.predList.append(temp)
        labels = ['user', 'item', 'rating']
        self.predList = pd.DataFrame.from_records(self.predList, columns=labels)

    def null_rated_item(self, user_id):
        ids = np.where(self.Y_data[:, 0] == user_id)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()
        # y_pred = self.X.dot(self.W[:, user_id])
        null_rated = []
        for i in range(self.n_items):
            if i in items_rated_by_u:
                null_rated.append((i, -1))
        return null_rated

    def get_result_item(self, user_id):
        ids = np.where(self.Y_test[:, 0] == user_id)[0]
        ids = self.Y_test[ids]
        ids = ids[ids[:, 1].argsort(kind='mergesort')]
        id_item = ids[:, 1].tolist()
        data_item = ids[:, 2].tolist()
        list_result = []
        temp = 0
        for i in range(52):
            if i not in id_item:
                list_result.append((i, -1))
            if i in id_item:
                list_result.append((i, data_item[temp]))
                temp = temp + 1
        return list_result

    def get_item_null(self, user_id):
        ids = np.where(self.Y_data[:, 0] == user_id)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()
        list_null = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                list_null.append((i, -1))
        return list_null

    def pred_for_user(self, user_id):
        ids = np.where(self.Y_data[:, 0] == user_id)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()
        predicted_ratings = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                rating = self.Yhat[i]
                rating = rating[user_id]
                predicted_ratings.append((i, rating))
        return predicted_ratings

    def evaluate_RMSE(self):
        SE = 0  # squared error
        for n in range(self.Y_test.shape[0]):
            user = self.predList['user'] == self.Y_test[n, 0]
            item = self.predList['item'] == self.Y_test[n, 1]
            pred = self.predList[user & item]
            pred = pred.iloc[0]['rating']
            SE += (pred - self.Y_test[n, 2]) ** 2
        RMSE = np.sqrt(SE / self.Y_test.shape[0])
        return RMSE

    def evaluate_MAE(self):
        temp = []  # squared error
        for n in range(self.Y_test.shape[0]):
            user = self.predList['user'] == self.Y_test[n, 0]
            item = self.predList['item'] == self.Y_test[n, 1]
            pred = self.predList[user & item]
            pred = pred.iloc[0]['rating']
            temp.append(pred)
        MAE = mean_absolute_error(self.Y_test[:, 2], temp)
        return MAE

    def evaluate_MSE(self):
        temp = []  # squared error
        for n in range(self.Y_test.shape[0]):
            user = self.predList['user'] == self.Y_test[n, 0]
            item = self.predList['item'] == self.Y_test[n, 1]
            pred = self.predList[user & item]
            pred = pred.iloc[0]['rating']
            temp.append(pred)
        MSE = mean_squared_error(self.Y_test[:, 2], temp)
        return MSE


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
