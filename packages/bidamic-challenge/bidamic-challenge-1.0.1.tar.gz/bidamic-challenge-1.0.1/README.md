# <font color=darkgreen>BIDAMIC READ ME CODING CHALLENGE</color>

There are several methods that can be used in the bidamic.py file. These include:

- get_processed_df
- show_arr
- show_data
- get_columns
- save_csv_file
- search_multi_word_term
- search_one_word_term

### Steps on how to use Bidamic python package
1. Ensure you have the coding_challenge_data.csv file
2. Put the string path of the coding_challenge_data.csv file, into Bidamic(file_path), and create an instance.
3. Instance, b = Bidamic(file_path)
4. Using search_one_word_term method. This allows only 1 word used to search for in the .csv file.
5. Say you type in "spiderman", then a .csv file is generated with a timestamp as its file name, and stored in:

 =====> processed/currency/search_terms/timestamp

6. The search_multi_word_term allows for multiple words, e.g. "spiderman suit". This will generate a .csv file with the ROAS calculated only for rows where both "spiderman" and "suit" were contained in the search term column of the coding_challenge_data.csv file.


### Dependencies
- NumPy
- Pandas
- OS






### Recommended packages to use with Bidamic.py

- Matplotlib for data visualization
- Reportlab to generate PDF reports
- Flask for creating an interactive web site
- Flask-SQLAlchemy to store the data in a database as opposed to a csv file.


```python

```
