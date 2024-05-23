import pandas as pd

columns = ['job','country','number_of_pages','unique_url']
data = pd.read_csv('./data/urls_for_job_in_country.csv', delimiter='\t')

print(data['unique_url'][7])