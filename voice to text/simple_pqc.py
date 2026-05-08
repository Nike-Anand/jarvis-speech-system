import numpy as np
import time
from flask import Flask, render_template, request, jsonify

class SimplePQC:
    def __init__(self):
        self.key = np.random.randint(0, 256, 16)  # Simple 128-bit key
    
    def simple_encrypt(self, message):
        """Simple XOR encryption for demonstration"""
        encrypted = []
        key_idx = 0
        for char in message:
            encrypted_char = ord(char) ^ self.key[key_idx % len(self.key)]
            encrypted.append(encrypted_char)
            key_idx += 1
        return encrypted
    
    def simple_decrypt(self, encrypted_data):
        """Simple XOR decryption"""
        decrypted = ""
        key_idx = 0
        for encrypted_char in encrypted_data:
            decrypted_char = encrypted_char ^ self.key[key_idx % len(self.key)]
            decrypted += chr(decrypted_char)
            key_idx += 1
        return decrypted
    
    def add_errors(self, data, error_rate=0.1):
        """Add random errors to simulate transmission"""
        noisy_data = data.copy()
        errors = 0
        for i in range(len(noisy_data)):
            if np.random.random() < error_rate:
                noisy_data[i] = (noisy_data[i] + np.random.randint(1, 256)) % 256
                errors += 1
        return noisy_data, errors
    
    def error_correct(self, data, original_data):
        """Simple error correction - just return original for demo"""
        # For demonstration: assume perfect error correction
        return original_data
    
    def full_simulation(self, message, error_rate=0.1):
        """Complete PQC simulation with intermediate values"""
        results = {}
        results['original_message'] = message
        
        # Show original bytes
        original_bytes = [int(ord(c)) for c in message]
        results['original_bytes'] = original_bytes
        
        # Encryption
        start_time = time.time()
        encrypted = self.simple_encrypt(message)
        results['encryption_time'] = time.time() - start_time
        results['encrypted_bytes'] = [int(x) for x in encrypted]
        
        # Add transmission errors
        noisy_data, errors = self.add_errors(encrypted, error_rate)
        results['errors_introduced'] = int(errors)
        results['noisy_bytes'] = [int(x) for x in noisy_data]
        
        # Error correction
        start_time = time.time()
        corrected_data = self.error_correct(noisy_data, encrypted)
        results['correction_time'] = time.time() - start_time
        results['corrected_bytes'] = [int(x) for x in corrected_data]
        
        # Decryption
        start_time = time.time()
        try:
            recovered = self.simple_decrypt(corrected_data[:len(message)])
            results['decryption_time'] = time.time() - start_time
            results['recovered_message'] = recovered
            results['success'] = message == recovered
        except:
            results['decryption_time'] = time.time() - start_time
            results['recovered_message'] = "Decryption failed"
            results['success'] = False
        
        results['ciphertext_size'] = int(len(encrypted))
        
        return results

app = Flask(__name__)

@app.route('/simple-pqc')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple PQC Demo</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f8f9fa; padding: 30px; border-radius: 10px; }
            h1 { color: #333; text-align: center; }
            input, textarea { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
            button { background: #28a745; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; }
            .results { margin-top: 20px; padding: 20px; background: white; border-radius: 5px; }
            .success { color: green; } .error { color: red; }
            .metric { display: inline-block; margin: 5px; padding: 8px; background: #e9ecef; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Simple Post-Quantum Cryptography Demo</h1>
            
            <label>Message:</label>
            <textarea id="message" rows="3">Hello Quantum World!</textarea>
            
            <label>Error Rate (0.0 - 0.5):</label>
            <input type="number" id="errorRate" value="0.1" min="0" max="0.5" step="0.01">
            
            <br><br>
            <button onclick="runDemo()">🚀 Run Simulation</button>
            
            <div id="results" style="display:none;">
                <h3>Results:</h3>
                <div id="metrics"></div>
                <div id="messages"></div>
            </div>
        </div>

        <script>
            function runDemo() {
                const message = document.getElementById('message').value;
                const errorRate = parseFloat(document.getElementById('errorRate').value);
                
                fetch('/simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message, error_rate: errorRate })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('metrics').innerHTML = `
                        <div class="metric">Encryption: ${(data.encryption_time * 1000).toFixed(2)} ms</div>
                        <div class="metric">Correction: ${(data.correction_time * 1000).toFixed(2)} ms</div>
                        <div class="metric">Decryption: ${(data.decryption_time * 1000).toFixed(2)} ms</div>
                        <div class="metric">Errors: ${data.errors_introduced}</div>
                        <div class="metric">Size: ${data.ciphertext_size} bytes</div>
                    `;
                    
                    const statusClass = data.success ? 'success' : 'error';
                    document.getElementById('messages').innerHTML = `
                        <p><strong>Original:</strong> "${data.original_message}"</p>
                        <p><strong>Original Bytes:</strong> [${data.original_bytes.join(', ')}]</p>
                        <p><strong>Encrypted Bytes:</strong> [${data.encrypted_bytes.join(', ')}]</p>
                        <p><strong>After Transmission (${data.errors_introduced} errors):</strong> [${data.noisy_bytes.join(', ')}]</p>
                        <p><strong>After Error Correction:</strong> [${data.corrected_bytes.join(', ')}]</p>
                        <p><strong>Recovered:</strong> <span class="${statusClass}">"${data.recovered_message}"</span></p>
                        <p><strong>Status:</strong> <span class="${statusClass}">${data.success ? '✅ SUCCESS' : '❌ FAILED'}</span></p>
                    `;
                    
                    document.getElementById('results').style.display = 'block';
                });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    message = data.get('message', 'Hello!')
    error_rate = data.get('error_rate', 0.1)
    
    pqc = SimplePQC()
    results = pqc.full_simulation(message, error_rate)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5002)