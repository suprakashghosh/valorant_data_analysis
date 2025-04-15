# valorant_data_analysis

This project aims to provide tools and scripts for analyzing Valorant match data obtained from the Valorant API. It includes data extraction, transformation, and loading (ETL) processes to store the data in a PostgreSQL database, as well as analytical queries and visualizations to gain insights from the data.

The schema used can be found here- https://dbdiagram.io/d/Valorant-Match-API-67c9232e263d6cf9a0644929

### Project Structure

The project is structured as follows:

-   `pydantic_models`: Contains Pydantic models for data validation and serialization.
-   `sqlalchemy_models`: Contains SQLAlchemy models for defining the database schema.
-   `loading.py`: Contains functions for loading and transforming data from the Valorant API into the database.
-   `logs`: Contains log files for monitoring the application.
-   `requirements.txt`: Lists the project dependencies.

### License

This project is licensed under the [MIT License](LICENSE).
