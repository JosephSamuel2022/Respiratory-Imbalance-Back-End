# flask_project/app.py

from flask import (
    Flask,
    jsonify,
    request,
    session,
    render_template,
    redirect,
    url_for,
    flash,
)
from flask_cors import CORS

from pymongo import MongoClient
import pickle
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
import base64
import io
from datetime import date


app = Flask(__name__)
CORS(
    app
)  # Allow requests from any origin (you can restrict this to the React app's URL)

app.config["SECRET_KEY"] = "predictingrespimbalance"
model = pickle.load(open("model.pkl", "rb"))
app.secret_key = "predictingrespimbalance"

MONGODB_URI = "mongodb+srv://josephsamuelm2021:Samenoch%4074@cluster0.itztqvl.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)
db = client["patients"]


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    pid = data.get("pid")
    password = data.get("password")

    user = db.patient_details.find_one({"pid": pid, "password": password})

    if user is not None:
        result = "true"
    else:
        result = "false"
    return render_template("loginresult.html", result=result)


@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    pid = data.get("pid")
    dob_with_time = data.get("dob")  # e.g., "2023-07-19T18:30:00.000Z"
    dob = dob_with_time.split("T")[0]  # Get the date part only, e.g., "2023-07-19"
    dateobj = datetime.strptime(dob, "%Y-%m-%d")
    gender = data.get("gender")
    password = data.get("password")
    name = data.get("name")

    # Check if patient id already exists
    existing_patient = db.patient_details.find_one({"pid": pid})

    if existing_patient:
        # If patient ID already exists, return a response indicating it
        return render_template("loginresult.html", result="no")

    # Insert user's data into database
    db.patient_details.insert_one(
        {
            "pid": pid,
            "name": name,
            "dob": dateobj,
            "gender": gender,
            "password": password,
        }
    )

    return "", 200  # Return an empty response with status code 200


@app.route("/api/info", methods=["POST"])
def info():
    data = request.get_json()
    pid = data.get("pid")

    patient = db.patient_details.find_one({"pid": pid})
    name = patient.get("name")
    gender = patient.get("gender")
    dob = patient.get("dob")
    today = datetime.utcnow()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    tdate = date.today()
    today_str = tdate.strftime("%Y-%m-%d")

    return render_template(
        "info.html", name=name, gender=gender, age=age, today_str=today_str
    )


@app.route("/api/forgot", methods=["POST"])
def forgot():
    data = request.get_json()
    patient_id = data.get("patientId")
    dob_with_time = data.get("dob")  # e.g., "2023-07-19T18:30:00.000Z"
    dob = dob_with_time.split("T")[0]  # Get the date part only, e.g., "2023-07-19"
    dateobj = datetime.strptime(dob, "%Y-%m-%d")

    new_password = data.get("newPassword")

    # Check if the patient_id exists in the database

    existing_patient = db.patient_details.find_one({"pid": patient_id, "dob": dateobj})

    if existing_patient:
        # If patient_id exists, update the password and return "yes"
        db.patient_details.update_one(
            {"pid": patient_id}, {"$set": {"password": new_password}}
        )
        return render_template("forgotpassword.html", result="yes")

    else:
        return render_template(
            "forgotpassword.html", result="Incorrect Patient Id or Date of Birth"
        )


@app.route("/api/pastdata", methods=["POST"])
def pastdata():
    data = request.get_json()
    patient_id = data.get("patientId")

    # 3.Heart rate vs time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    heart_rates = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        heart_rates.append(doc["Heart_Rate"])

    # Create a new figure and axis object
    fig, ax3 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax3.plot(dates, heart_rates, color="blue", marker="o")

    # Add labels and title to the plot
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Heart Rate")
    ax3.set_title("Heart Rate over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    heart_rate_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 4.Pulse Rate vs Time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    pulse_rates = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        pulse_rates.append(doc["Pulse"])

    # Create a new figure and axis object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax4.plot(dates, pulse_rates, color="blue", marker="o")

    # Add labels and title to the plot
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Pulse Rate")
    ax4.set_title("Pulse Rate over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    pulse_rate_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 5.Temperature vs Time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    temperatures = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        temperatures.append(doc["Temperature"])

    # Create a new figure and axis object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax4.plot(dates, temperatures, color="blue", marker="o")

    # Add labels and title to the plot
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Temperature")
    ax4.set_title("Temperature over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    temperature_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 6.Respiratory Rate vs Time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    res_rates = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        res_rates.append(doc["Respiratory_Rate"])

    # Create a new figure and axis object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax4.plot(dates, res_rates, color="blue", marker="o")

    # Add labels and title to the plot
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Respiratory Rate")
    ax4.set_title("Respiratory Rate over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    respiratory_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 7.Oxygen Saturation vs Time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    oxy_saturation = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        oxy_saturation.append(doc["Oxygen_Saturation"])

    # Create a new figure and axis object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax4.plot(dates, oxy_saturation, color="blue", marker="o")

    # Add labels and title to the plot
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Oxygen Saturation")
    ax4.set_title("Oxygen Saturation over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    saturation_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 8.pH vs Time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    phr = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        phr.append(doc["PH"])

    # Create a new figure and axis object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax4.plot(dates, phr, color="blue", marker="o")

    # Add labels and title to the plot
    ax4.set_xlabel("Date")
    ax4.set_ylabel("pH")
    ax4.set_title("pH over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    pH_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 9. Word Cloud

    diagnosis_list = []

    cursor = db.medicalhistory.find({"pid": patient_id})
    for doc in cursor:
        diagnosis_list.append(doc["Prediction"])

    # Create a dictionary with the frequency of each diagnosis
    freq_dict = {}
    for diagnosis in diagnosis_list:
        freq_dict[diagnosis] = freq_dict.get(diagnosis, 0) + 1

    # Create a WordCloud object with the frequencies of each diagnosis
    wordcloud = WordCloud(
        width=800, height=600, background_color="white"
    ).generate_from_frequencies(freq_dict)

    colormap = "viridis"

    # Create a matplotlib figure and axis for the WordCloud object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    ax4.imshow(wordcloud, interpolation="bilinear", cmap=colormap)

    # ax4.set_xticks([])
    # ax4.set_yticks([])

    ax4.axis("off")

    ax4.set_title("Frequency of Respiratory Imbalance Levels")

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode memory buffer to base64 string and pass to template
    wordcloud_data = base64.b64encode(buffer.read()).decode("utf-8")
    return render_template(
        "pastdata.html",
        heart_rate_data=heart_rate_data,
        pulse_rate_data=pulse_rate_data,
        temperature_data=temperature_data,
        respiratory_data=respiratory_data,
        saturation_data=saturation_data,
        pH_data=pH_data,
        wordcloud_data=wordcloud_data,
    )


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    patient_id = data.get("patientId")  # Get the patientId from the JSON data

    # Exclude "patientId" from the keys used to create int_features
    int_features = [float(data.get(key)) for key in data.keys() if key != "patientId"]
    final_features = [np.array(int_features)]
    predictiona = model.predict(final_features)
    prediction = np.array_str(predictiona)
    result = prediction[2:-2]

    # Insert
    tdate = date.today()
    today_str = tdate.strftime("%Y-%m-%d")

    Dehydration = data.get("dehydration")
    Medicine_Overdose = data.get("medicineOverdose")
    Acidious = data.get("acidious")
    Cold = data.get("cold")
    Cough = data.get("cough")
    Temperature = data.get("temperature")
    Heart_Rate = data.get("heartRate")
    Pulse = data.get("pulseRate")
    BPSYS = data.get("bpsys")
    BPDIA = data.get("bpdia")
    Respiratory_Rate = data.get("respiratoryRate")
    Oxygen_Saturation = data.get("oxygenSaturation")
    pH = data.get("pH")

    db.medicalhistory.insert_one(
        {
            "tdate": today_str,
            "pid": patient_id,
            "Dehydration": Dehydration,
            "Medicine_Overdose": Medicine_Overdose,
            "Acidious": Acidious,
            "Cold": Cold,
            "Cough": Cough,
            "Temperature": Temperature,
            "Heart_Rate": Heart_Rate,
            "Pulse": Pulse,
            "BPSYS": BPSYS,
            "BPDIA": BPDIA,
            "Respiratory_Rate": Respiratory_Rate,
            "Oxygen_Saturation": Oxygen_Saturation,
            "PH": pH,
            "Prediction": result,
        }
    )

    # 1. respiratory rate vs temperature

    x = []
    # Iterate over the documents returned by the query
    cursor = db.medicalhistory.find({}, {"Temperature": 1, "_id": 0})
    for doc in cursor:
        # Extract the desired attribute and add it to the array
        x.append(doc["Temperature"])

    y = []
    # Iterate over the documents returned by the query
    cursor = db.medicalhistory.find({}, {"Respiratory_Rate": 1, "_id": 0})
    for doc in cursor:
        # Extract the desired attribute and add it to the array
        y.append(doc["Respiratory_Rate"])

    # Set the color for the selected point and the rest of the points
    selected_color = "r"
    rest_color = "b"

    # Create a list of colors for each point in the plot
    colors = [selected_color if i == len(x) - 1 else rest_color for i in range(len(x))]

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Respiratory Rate")
    ax.set_title("Respiratory Rate vs Temperature")
    ax.scatter(x, y, c=colors)

    # Show the plot

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode memory buffer to base64 string and pass to template
    plot_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 2.Frequency of symptoms

    symptoms = ["Dehydration", "Medicine_Overdose", "Acidious", "Cold", "Cough"]
    c = []
    for i in symptoms:
        co = 0

        cursor = db.medicalhistory.find({i: 1})
        for doc in cursor:
            co += 1
        c.append(co)
        # Extract the desired attribute and add it to the array

    fig, ax2 = plt.subplots(figsize=(8, 6))
    ax2.bar(symptoms, c)
    plt.xlabel("Symptoms")
    plt.ylabel("Frequency")
    plt.title("Frequency of Symptoms")

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode memory buffer to base64 string and pass to template
    bar_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 3.Heart rate vs time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    heart_rates = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        heart_rates.append(doc["Heart_Rate"])

    # Create a new figure and axis object
    fig, ax3 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax3.plot(dates, heart_rates, color="blue", marker="o")

    # Add labels and title to the plot
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Heart Rate")
    ax3.set_title("Heart Rate over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    heart_rate_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 4.Pulse Rate vs Time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    pulse_rates = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        pulse_rates.append(doc["Pulse"])

    # Create a new figure and axis object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax4.plot(dates, pulse_rates, color="blue", marker="o")

    # Add labels and title to the plot
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Pulse Rate")
    ax4.set_title("Pulse Rate over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    pulse_rate_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 5.Temperature vs Time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    temperatures = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        temperatures.append(doc["Temperature"])

    # Create a new figure and axis object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax4.plot(dates, temperatures, color="blue", marker="o")

    # Add labels and title to the plot
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Temperature")
    ax4.set_title("Temperature over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    temperature_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 6.Respiratory Rate vs Time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    res_rates = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        res_rates.append(doc["Respiratory_Rate"])

    # Create a new figure and axis object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax4.plot(dates, res_rates, color="blue", marker="o")

    # Add labels and title to the plot
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Respiratory Rate")
    ax4.set_title("Respiratory Rate over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    respiratory_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 7.Oxygen Saturation vs Time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    oxy_saturation = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        oxy_saturation.append(doc["Oxygen_Saturation"])

    # Create a new figure and axis object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax4.plot(dates, oxy_saturation, color="blue", marker="o")

    # Add labels and title to the plot
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Oxygen Saturation")
    ax4.set_title("Oxygen Saturation over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    saturation_data = base64.b64encode(buffer.read()).decode("utf-8")

    # 8.pH vs Time

    cursor = db.medicalhistory.find({"pid": patient_id})
    dates = []
    phr = []
    # Extract the date and heart rate from each document and add them to the arrays
    for doc in cursor:
        dates.append(doc["tdate"])
        phr.append(doc["PH"])

    # Create a new figure and axis object
    fig, ax4 = plt.subplots(figsize=(8, 6))

    # Plot the heart rate data as a line chart
    ax4.plot(dates, phr, color="blue", marker="o")

    # Add labels and title to the plot
    ax4.set_xlabel("Date")
    ax4.set_ylabel("pH")
    ax4.set_title("pH over Time")

    # Save the plot to a buffer and convert it to a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    pH_data = base64.b64encode(buffer.read()).decode("utf-8")

    return render_template(
        "predictionresult.html",
        result=result,
        plot_data=plot_data,
        bar_data=bar_data,
        heart_rate_data=heart_rate_data,
        pulse_rate_data=pulse_rate_data,
        temperature_data=temperature_data,
        respiratory_data=respiratory_data,
        saturation_data=saturation_data,
        pH_data=pH_data,
    )


if __name__ == "__main__":
    app.run(port=5000)
