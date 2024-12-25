from flask import Flask, jsonify, render_template
import pymongo
import os

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["x_data"]
collection = db["trending_topics"]

# Absolute path to your templates folder
absolute_template_path = r"D:\Project\Stir_Assignments\templates"

app = Flask(__name__, template_folder=absolute_template_path)

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/api/trending', methods=['GET'])
def get_trending():
    try:
        # Query MongoDB to fetch the most recent trending topics
        record = collection.find().sort("timestamp", pymongo.DESCENDING).limit(1)
        trending_data = list(record)  # Convert the cursor to a list

        if trending_data:
            trending_topics = trending_data[0]["trending_topics"]  # Fetch the trending topics from the most recent record
            return jsonify({"trending_topics": trending_topics})
        else:
            return jsonify({"error": "No trending topics found in the database"})

    except Exception as e:
        return jsonify({"error": "Error fetching data from MongoDB", "details": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
