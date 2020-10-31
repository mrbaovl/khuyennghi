import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

from web.ContentBase import CB

if __name__ == "__main__":
    r_cols = ['stt', 'user_id', 'item_id', 'rating']
    ratings = pd.read_csv('data/data.csv', names=r_cols, encoding='latin-1')
    ratings = ratings.drop('stt', 1)
    ratings = ratings.loc[1:, :]
    ratings = ratings.apply(pd.to_numeric)
    ratings = ratings.to_numpy()

    testing = pd.read_csv('data/testing.csv', names=r_cols, encoding='latin-1')
    testing = testing.drop('stt', 1)
    testing = testing.loc[1:, :]
    testing = testing.apply(pd.to_numeric)
    testing = testing.to_numpy()

    training = pd.read_csv('data/training.csv', names=r_cols, encoding='latin-1')
    training = training.drop('stt', 1)
    training = training.loc[1:, :]
    training = training.apply(pd.to_numeric)
    training = training.to_numpy()

    n_cols = ['id_mon', 'web', 'mobile', 'desktop', 'devops', 'game']
    mon = pd.read_csv('data/monhoc.csv', names=n_cols, encoding='latin-1')
    mon = mon.apply(pd.to_numeric)
    mon = mon.to_numpy()
    X_train, X_test = train_test_split(ratings, test_size=0.3, random_state=42)
    rs = CB(X_train, X_test, mon)
    print(rs)
    rs.pred_all()
    rs.preList()
    filename = 'model/Model_CB.sav'
    # Save to file in the current working directory
    joblib.dump(rs, filename)

