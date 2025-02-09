import pandas as pd
import numpy as np
# from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

df=pd.read_csv('inputDataset.csv')
df = df.replace('?', np.nan)
df = df.dropna()

X=df.drop(columns=['class'])
Y=df['class']


X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2)

classifier=KNeighborsClassifier(n_neighbors=1,p=2,metric='euclidean')
classifier.fit(X_train,Y_train)
joblib.dump(classifier,'AppClassifier.joblib')

Y_pred=classifier.predict(X_test)
# Y_pred

cm=confusion_matrix(Y_test,Y_pred)
print(cm)

print(accuracy_score(Y_test,Y_pred))



# model=DecisionTreeClassifier()
# model.fit(X_train,Y_train)
#joblib.dump(model,'AppClassifier.joblib')

# predictions=model.predict(X_test)
# score=accuracy_score(Y_test,predictions)
# score



