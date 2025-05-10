## 🌴 sqlalchemy-challenge
Welcome to the **Honolulu Climate Analysis** challenge! This repository contains a climate analysis of **Honolulu, Hawaii**, using **Python, SQLAlchemy, Pandas, and Matplotlib**, followed by the development of a **Flask API** to serve climate data.

## 📂 Repository Structure
```
qlalchemy-challenge/
├── SurfsUp/
│   ├── climate.ipynb       # Jupyter Notebook with data analysis
│   ├── app.py              # Flask application for API endpoints
│   ├── Resources/
│   │   └── hawaii.sqlite   # SQLite database file
├── README.md               # Documentation
```
## 🖥️ Technologies Used
- **Python** – Programming language for data analysis and API development.
- **SQLAlchemy** – Object-Relational Mapper (ORM) for database management.
- **SQLite** – Database storing climate-related data
- **Pandas** – Data manipulation and analysis.
- **Matplotlib** – Visualization library for plotting precipitation and temperature data.
- **Flask** – Micro-framework used to build the API.

## 📊 Climate Analysis (Jupyter Notebook)
In this analysis, we:
- **Connected** to an **SQLite database** using SQLAlchemy ORM.
- **Queried and visualized** precipitation trends over the past **12 months**.
- **Identified the most active weather stations** and analyzed temperature trends.

## 🚀 Flask API Endpoints
| Route                     | Description |
|---------------------------|-------------|
| `/`                       | Homepage, lists available API route or endpoints |
| `/api/v1.0/precipitation` | Last 12 months of precipitation |
| `/api/v1.0/stations`      | List of weather stations |
| `/api/v1.0/tobs`          | Last 12 months temperature observations for the most active station |
| `/api/v1.0/<start>`       | Min, Max, Avg temperatures from the given start date onward, date format:YYYY-MM-DD |
| `/api/v1.0/<start>/<end>` | Min, Max, Avg temperatures between the given start and end dates, date format:YYYY-MM-DD |

## 🛠 Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/geraldine1456/sqlalchemy-challenge.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask API:
   ```bash
   python app.py
   ```
4. Open your browser and visit:
   ```
   http://127.0.0.1:5000/
   ```

## 📖 References
- [Python Official Documentation](https://docs.python.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Microsoft Copilot](https://copilot.microsoft.com/) 
