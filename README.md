# AramGO

A Django project creating a simple op.gg clone for fetching ARAM match history. It uses the Riot Games API to fetch matches, champions, and items. The application parses the relevant data and stores the information in a database. 

## Features
- Fetch real-time match data from the Riot Games API.
- Store match history in a SQLite database.
- Display match information using Django's view logic and templates.
- User-friendly and responsive interface.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/framarqu001/aramgoproto.git
    cd aramgoproto
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Django development server:
    ```bash
    python manage.py runserver
    ```

## Usage

1. Open your web browser and navigate to `http://localhost:8000`.
2. Enter a League of Legends summoner name to fetch and display their ARAM match history.

## Screenshots

### Match History View
![test](https://github.com/framarqu001/aramgoproto/assets/119390184/a897134e-8b4f-4d26-b507-9abcea9a9998)
*Displays detailed match history for a user.*

### Database Schema
![test2](https://github.com/framarqu001/aramgoproto/assets/119390184/027e3d4b-d02a-4db5-85ea-7c07926b678d)
*Shows the database schema used for storing match data.*

## Technologies Used
- Django
- Riot Games API
- SQLite
- HTML/CSS/JavaScript

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.




