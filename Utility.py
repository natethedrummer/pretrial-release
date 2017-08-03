# import packages
import pandas as pd

# output to excel
def out_to_xl(df_coef, df_accuracy, df_pred):
    writer = pd.ExcelWriter('explain_release.xlsx')
    df_coef.to_excel(writer, 'coefficients')
    df_accuracy.to_excel(writer, 'accuracy')
    df_pred.to_excel(writer, 'predictions')
    return writer.save()