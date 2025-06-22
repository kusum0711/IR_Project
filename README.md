# QuerySuggest

QuerySuggest is a Django-based web application that allows users to search for content stored in Elasticsearch and provides additional search suggestions using random city names from a local SQLite database. The project also uses NLTK to fetch synonyms, definitions, and related terms for enhanced query insights.

## Features

- **Search Functionality:** Search for content stored in Elasticsearch.
- **Suggested Cities:** Displays three random city names from the database as additional search suggestions.
- **Enhanced Query Information:** Provides synonyms, definitions, and related terms using NLTK's WordNet.
- **Custom 404 Page:** Handles non-existent URLs with a user-friendly error page.

## Requirements

- Python 3.8+
- Elasticsearch (Ensure Elasticsearch is running locally)
- Django 5.1+
- NLTK library

## Installation and Setup

Follow the steps below to set up and run the project from scratch:

1. Clone the repository:
   ```bash
   git clone https://github.com/rohann-xd/QuerySuggest.git
   cd QuerySuggest
   ```

2. Start Elasticsearch manually on your PC.

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

6. Index data in Elasticsearch:
   ```bash
   python index_data.py
   ```

7. Run migrations to create the database:
   ```bash
   python manage.py migrate
   ```

8. Populate the database with city names:
   ```bash
   python manage.py import_cities
   ```

9. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

2. Enter a query into the search bar and view the results.

3. Explore additional search suggestions and query insights.

4. If an invalid URL is accessed, the custom 404 page will be displayed.

## Directory Structure

```
|data              # Folder containing text files for city names
|QuerySuggest/
|-- search/             # Django app for the search functionality
|   |-- templates/      # HTML templates for the app
|   |-- models.py       # City model definition
|   |-- views.py        # Search and result logic
|   |-- import_cities.py # Script to populate the database with city names
|
|-- configuration/      # Django project folder
|-- static/             # Static files (CSS, JS, etc.)
|-- db.sqlite3          # SQLite database file
|-- manage.py           # Django's management script
|-- index_data.py       # Script to index data in Elasticsearch
```

## Additional Notes

- Ensure Elasticsearch is running before starting the Django server.
- The city names are fetched from text files located in the `data/` folder during the `import_cities` command.
- Data is indexed in Elasticsearch using the `index_data.py` script.
- You can customize the search logic in `views.py` or enhance the city dataset as needed.

## License

This project is licensed under the [MIT License](LICENSE).

---

Enjoy using QuerySuggest! Feel free to contribute or raise issues if you encounter any problems.
