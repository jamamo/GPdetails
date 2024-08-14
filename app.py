from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Define the path to the data folder
data_folder = os.path.join(app.root_path, 'data')

# Specify the paths to the Excel files
file1 = os.path.join(data_folder, "Stockport GP Practice_generic email addresses_4.10.2019.xlsx")
file2 = os.path.join(data_folder, "Preston & Chorley GPs.xlsx")
file3 = os.path.join(data_folder, "Manchester GPs.xlsx")

# Load the Excel files into DataFrames
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)
df3 = pd.read_excel(file3)

# Combine the dataframes into a single dataframe
combined_df = pd.concat([df1, df2, df3], ignore_index=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ""
    results = None
    if request.method == 'POST':
        query = request.form['query']
        if query:
            # Perform the search across all columns
            mask = combined_df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
            results = combined_df[mask]
            # Drop any columns that are completely NaN
            results = results.dropna(how='all', axis=1)
            # Drop any rows that are completely NaN
            results = results.dropna(how='all', axis=0)
            # If results are empty, set it to None for easier template handling
            if results.empty:
                results = None

    return render_template('index.html', query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

