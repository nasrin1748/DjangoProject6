from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Web Terminal</title>
        <style>
            body { font-family: monospace; margin: 20px; }
            #output { background: black; color: white; padding: 10px; min-height: 200px; }
            #command { width: 100%; padding: 5px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div id="output"></div>
        <input type="text" id="command" placeholder="Enter command...">

        <script>
            const commandInput = document.getElementById('command');
            const output = document.getElementById('output');

            commandInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    const command = this.value;
                    fetch('/execute', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({command: command})
                    })
                    .then(response => response.json())
                    .then(data => {
                        output.innerHTML += `<div>$ ${command}</div>`;
                        output.innerHTML += `<div>${data.output}</div>`;
                        this.value = '';
                    });
                }
            });
        </script>
    </body>
    </html>
    '''


@app.route('/execute', methods=['POST'])
def execute_command():
    command = request.json.get('command')
    try:
        # Execute command and capture output
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout or result.stderr
    except Exception as e:
        output = str(e)

    return jsonify({'output': output})


if __name__ == '__main__':
    app.run(debug=True)