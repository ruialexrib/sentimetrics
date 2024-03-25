# Sentimetrics - Turning Words into Sentiments

Sentimetrics is a simple web application developed in Flask for sentiment analysis in text. It allows users to add new reviews and view existing reviews along with their sentiment polarity (positive, negative, or neutral). The sentiment analysis model is powered by a pipeline that processes the data and performs classification.

## Application Details

### Key Features:

1. **Add Reviews:** Users can submit new reviews via the form on the home page.
2. **View Reviews:** Added reviews are displayed on the home page along with their sentiment polarity.
3. **Reset Reviews:** There's an option to clear all existing reviews.

### Code Structure:

- **`app.py`:** Contains the main code of the Flask application. Defines routes, interacts with the sentiment analysis model, and renders HTML templates.
- **`model.py`:** Provides the data structure to store reviews.
- **`pipeline.py`:** Implements the sentiment analysis pipeline, including model loading, sentiment prediction, and training a new model.
- **`data/data.csv`:** CSV file containing training data for the sentiment analysis model.

### Routes:

- **`/`:** Home page that displays all existing reviews and allows users to add new reviews.
- **`/add_review`:** Route to add a new review. Form data is processed, and sentiment polarity is predicted by the model.
- **`/reset`:** Route to clear all existing reviews.
- **`/train/<model_name>`:** Route to train the model with a new dataset. The model is trained with the provided data and replaces the existing model.

### Docker and Docker Compose:

The project includes a Dockerfile and a docker-compose.yml file to facilitate deploying the application in Docker containers.

### License:

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for more details.

## Running the Application

1. Ensure you have Python installed on your system.
2. Install project dependencies using `pip install -r requirements.txt`.
3. Run the `app.py` file using Python: `python app.py`.
4. Access the application in your browser at `http://localhost:8082`.

## Contribution and Support

Contributions are welcome! Feel free to open issues or send pull requests with improvements.

If you have any questions or need support, please open an issue in this repository.