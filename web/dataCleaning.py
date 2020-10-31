import pandas as pd

df = pd.read_excel('./data/D13HT.xls', sheet_name=0, header=0, skiprows=10, skip_footer=11)

# Cleaning Data ratings
df = df.drop('Unnamed: 3', 1)  # 0 for rows, 1 for columns
df = df.drop('Unnamed: 5', 1)
df = df.drop('Unnamed: 8', 1)
df = df.drop('Unnamed: 10', 1)
df = df.drop('Unnamed: 20', 1)
df = df.drop('Unnamed: 28', 1)
df = df.drop('Unnamed: 38', 1)
df = df.drop('Unnamed: 46', 1)
df = df.drop('Unnamed: 56', 1)
df = df.drop('Unnamed: 64', 1)
df = df.drop('Unnamed: 72', 1)
df = df.drop('Unnamed: 77', 1)
df = df.drop('Unnamed: 47', 1)
df = df.drop('Unnamed: 52', 1)
df = df.drop('Unnamed: 59', 1)
df = df.drop('TBN1', 1)
df = df.drop('TBN2', 1)
df = df.drop('TBN3', 1)
df = df.drop('TBN4', 1)
df['Họ và tên SV'] = df['Họ và tên SV'].map(str) + ' ' + df['Unnamed: 4']
df = df.drop('Unnamed: 4', 1)
df = df.loc[1:, :]
test = ['STT', 'Mã SV', 'Họ và tên SV', 'Ngày sinh', 'Nơi sinh', 'TBTL', 'Xếp loại']
for x in range(0, 52):
    test.append(x)
df.columns = test
df = df.drop('STT', 1)
df = df.drop('Họ và tên SV', 1)
df = df.drop('Ngày sinh', 1)
df = df.drop('Nơi sinh', 1)
df = df.drop('TBTL', 1)
df = df.drop('Xếp loại', 1)
df = df.drop('Mã SV', 1)

df.to_csv('temp.csv', encoding='utf-8')

training = df.iloc[:, :42]
training.to_csv('training_first.csv')
testing = df.iloc[:, 42:]
testing.to_csv('testing_first.csv')
print(df)

data_training = pd.DataFrame(columns=["IDSV", "IDMON", "DIEM"], dtype=int)
for i in range(training.shape[0]):
    for j in range(training.shape[1]):
        if pd.isna(training.values[i][j]) is True:
            continue
        else:
            data = [int(training.index.values[i] - 1), int(training.columns[j]),
                    float(float(training.values[i][j]) * 5 / 10)]
            data_training.loc[len(data_training)] = data

data_testing = pd.DataFrame(columns=["IDSV", "IDMON", "DIEM"], dtype=int)
for i in range(testing.shape[0]):
    for j in range(testing.shape[1]):
        if pd.isna(testing.values[i][j]) is True:
            continue
        else:
            data = [int(testing.index.values[i] - 1), int(testing.columns[j]), float(testing.values[i][j] * 5 / 10)]
            data_testing.loc[len(data_testing)] = data

data_training.to_csv('training_1.csv', encoding='utf-8')
data_testing.to_csv('testing.csv_1', encoding='utf-8')
