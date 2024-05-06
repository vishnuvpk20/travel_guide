import pandas as pd

df = pd.read_csv("cultural_etiquette_data.csv")

print(df.columns)
print(list(set(df.Section)))
# print(df.head())
print(df[(df.Country =='Argentina') & (df.Section =='Especially for Women')])
# print(list(df[(df.Country =='Argentina') & (df.Section =='The People')]["Detail"])[0])

import pandas as pd

# Assuming df is your DataFrame with columns 'Country', 'Section', and 'Detail'

# Step 1: Remove duplicates based on the 'Detail' column
df_clean= pd.read_csv("df_cleaned.csv")
df = df.append(df_clean)
df_cleaned = df.drop_duplicates(subset='Detail')



# Display the cleaned DataFrame before removing rows with section items in detail
print("Before removing rows with section items in detail:")
# print(df_cleaned)

# Step 3: Remove rows where any item in 'Section' appears in the 'Detail' column
sections = list(set(df_cleaned['Section']))
print(sections)
section_detail_mask = df_cleaned.apply(lambda row: any(section in row['Detail'] for section in sections), axis=1)
df_cleaned = df_cleaned[~section_detail_mask]

# Display the final cleaned DataFrame
print("\nFinal cleaned DataFrame:")

df_cleaned = df_cleaned[df_cleaned.Detail.str.strip().isin(sections) == False]
print(df_cleaned)
df_cleaned.to_csv("df_cleaned2.csv")
