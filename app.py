from flask import Flask, request, jsonify, render_template
import http.client
import json

app = Flask(__name__)

# API headers
headers = {
    'x-rapidapi-key': "8c05f30b5dmsh937ab1dcaab7bcfp188d5djsn15ef45e13d38",
    'x-rapidapi-host': "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
}

@app.route('/')
def index():
    return render_template('Web.html')  # Serve the HTML file

@app.route('/search_teams', methods=['GET'])
def search_teams():
    team_name = request.args.get('name', '')
    if not team_name:
        return jsonify({'error': 'No team name provided'}), 400

    conn = http.client.HTTPSConnection("tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com")
    endpoint = f"/getNFLTeams?teamStatsSeason=2023"
    try:
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = res.read()
        teams = json.loads(data.decode("utf-8"))

        # Filter teams based on user query
        filtered_teams = [team for team in teams.get('teams', []) if team_name.lower() in team['name'].lower()]

        return jsonify(filtered_teams)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
