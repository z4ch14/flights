from flask import Flask, jsonify, request, render_template
import pandas as pd
app = Flask(__name__)

"""
this function get an dataframe of flights and sort it by the arrival time and fill the "success" column
    input: dataframe of all the flights
    output: dataframe of all the flights sorted with the column "success"
"""
def process_flight_data(df):
    df = df.sort_values('Arrival')
    daily_success = 0
    for index, row in df.iterrows():
        time_diff = pd.to_datetime(row['Departure']) - pd.to_datetime(row['Arrival'])
        time_diff_minutes = time_diff.total_seconds() / 60

        if time_diff_minutes >= 180 and daily_success < 20:
            df.loc[index, 'success'] = 'success'
            daily_success += 1
        else:
            df.loc[index, 'success'] = 'fail'
    return df


"""
this API get an flight id and return the information about this flight or send an error if this flight
    doesn't exist
    input: flight id
    output: information about the flight
"""
@app.route('/flights/<flight_id>', methods=['GET'])
def get_flight_info(flight_id):
    df = pd.read_csv('flights.csv')
    flight_data = df[df['flight ID'] == flight_id]
    if not flight_data.empty:
        return jsonify(flight_data.to_dict(orient='records'))
    else:
        return jsonify({'error': 'Flight not found'}), 404

"""
this API get flights and merge them with the csv of all the flight and sort the new csv.
    input: information about new flights
"""
@app.route('/flights', methods=['GET'])
def update_flights_get():
    return render_template('form.html')

@app.route('/flights', methods=['POST'])
def update_flights_post():
    if request.content_type == 'application/json':
        flight_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
        flight_data = [{'flight ID': data["flight_ID"], 'Arrival': data["Arrival"],
                        'Departure': data["Departure"], 'success': ''}]
    else:
        return jsonify({'error': 'Unsupported Content-Type'}), 400

    new_df = pd.DataFrame(flight_data)
    df = pd.read_csv('flights.csv')
    df = pd.concat([df, new_df], ignore_index=True)

    new_flights = process_flight_data(df)
    new_flights.to_csv('flights.csv', index=False)
    return jsonify({'message': 'Flights updated successfully'})


if __name__ == '__main__':
    app.run(debug=True)