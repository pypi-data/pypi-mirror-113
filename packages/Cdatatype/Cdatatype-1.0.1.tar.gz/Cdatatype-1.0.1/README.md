A python package to count datatype and null values in columns.

#HOW TO USE

df = pd.dataframe(data)

from Cdatatype import datatypes

datatypes(df[['coulumn_name1','column_name2',......]])

@note - sometimes float values will be same as null values because null values like 'NaN' are also float values.