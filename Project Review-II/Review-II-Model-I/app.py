from flask import Flask, render_template, request, redirect, send_file
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

# Generate a key
key = Fernet.generate_key()
cipher = Fernet(key)

# Routes
@app.route('/')
def index():
    encrypted_files = [filename for filename in os.listdir('.') if filename.endswith('.enc')]
    return render_template('index.html', encrypted_files=encrypted_files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)

    encrypted_file = file.filename + '.enc'

    # Encrypt the uploaded file
    with open(encrypted_file, 'wb') as f:
        f.write(cipher.encrypt(file.read()))

    return redirect('/')

@app.route('/download/<filename>')
def download(filename):
    if not filename.endswith('.enc'):
        return "Invalid file format."

    decrypted_file = filename[:-4]  # Remove '.enc' extension

    if not os.path.exists(filename):
        return "File not found."

    # Decrypt the file
    decrypted_data = cipher.decrypt(open(filename, 'rb').read())

    # Write decrypted data to a new file
    with open(decrypted_file, 'wb') as f:
        f.write(decrypted_data)

    return send_file(decrypted_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
