# import packages
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
from sklearn.feature_selection import chi2
from sklearn.metrics import roc_auc_score, roc_curve, auc, precision_score, f1_score, mean_squared_error, accuracy_score

# report coefficients
def coef(model, X, X_train, y_train):

    df_coef = pd.DataFrame(list(zip(X.columns, np.transpose(model.coef_))))

    score, pvalues = chi2(X_train, y_train)

    df_coef['p-value'] = pd.DataFrame(list(zip(np.transpose(pvalues))))

    df_coef = df_coef.rename(columns = {0:'feature', 1:'coefficient'})

    df_coef['coefficient'] = df_coef['coefficient'].str[0]
    
    # intercept    
    df_intercept = pd.DataFrame(data=model.intercept_,
                                index=[0],
                                columns=['coefficient'])

    df_intercept['feature'] = 'Intercept'
    
    df_intercept = df_intercept[['feature', 'coefficient']]

    df_coef.update(df_intercept)

    df_coef['intercept'] = df_coef.iloc[0,1]
    
    df_coef = df_coef[df_coef['feature'] != 'Intercept']

    df_coef['log_odds'] = df_coef['intercept'] + df_coef['coefficient']    

    df_coef['odds'] = np.exp(df_coef['log_odds'])

    df_coef['probability'] = df_coef['odds'] / (1 + df_coef['odds'])

    df_coef.sort_values('probability', ascending=False, inplace=True)

    return df_coef

# report predictions
def pred(model, X, y, df_offenses):

    df_pred = X

    df_pred['predicted'] = model.predict(X)

    df_pred['actual'] = y

    df_pred['spn'] = df_offenses['SPN']

    return df_pred

# report accuracy
def accuracy(model, X_test, y_test):

    accuracy_model = model.score(X_test, y_test)
    accuracy_baseline = 1-y_test.mean()
    accuracy_change = accuracy_model - accuracy_baseline
    df_accuracy = pd.DataFrame({'Baseline Accuracy': [accuracy_baseline],
                                'Model Accuracy': [accuracy_model],
                                'Change in Accuracy': [accuracy_change]})
    df_accuracy['Baseline Accuracy'] = round(df_accuracy['Baseline Accuracy'],2)
    df_accuracy['Model Accuracy'] = round(df_accuracy['Model Accuracy'],2)
    df_accuracy['Change in Accuracy'] = round(df_accuracy['Change in Accuracy'],2)
    
    # ROC
    y_true = y_test
    y_pred = model.predict(X_test)
    df_accuracy['roc_auc_score'] = round(
            roc_auc_score(y_true, y_pred)
            ,2)
    fpr, tpr, threshold = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig('plot_roc.png')
    
    # precision score
    df_accuracy['precision_score'] = round(
            precision_score(y_true, y_pred)
            ,2)
    
    # f1 score
    df_accuracy['f1_score'] = round(
            f1_score(y_true, y_pred)
            ,2)
    
    # mean squared error
    df_accuracy['mean_squared_error'] = round(
            mean_squared_error(y_true, y_pred)
            ,2)
    
    # accuracy score
    df_accuracy['accuracy_score'] = round(
            accuracy_score(y_true, y_pred)
            ,2)
    
    return df_accuracy
