from flask import Flask, request, render_template, jsonify
import agent


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/agent-make-move', methods=['POST'])
def agentMakeMove():
    data = request.json
    board = data['board']
    num_cols = data['num_cols']
    num_rows = data['num_rows']
    inrow = data['inrow']

    return jsonify({
        "move": agent.move(board, num_cols, num_rows, inrow)
    })
    

if __name__ == '__main__':
    app.run(debug=True)