from ImportData import get_offenses
from DescribeData import bail_stats, bail_amount_stats, ptr_stats
from ModelData import model_bail_amount, model_ptr


df = get_offenses()


ptr_stats(df)


bail_stats(df)


bail_amount_stats(df)


model_bail_amount(df)


model_ptr(df)

