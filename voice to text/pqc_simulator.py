import numpy as np
import time
import hashlib
from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import io
import base64

class PQCSimulator:
    def __init__(self, n=256, q=7681, sigma=3.2):
        self.n = n  # Lattice dimension
        self.q = q  # Modulus
        self.sigma = sigma  # Gaussian noise parameter
        
    def generate_keys(self):
        """Generate LWE public and private keys"""
        # Private key: random binary vector
        s = np.random.randint(0, 2, self.n)
        
        # Public key: random matrix A and vector b = As + e
        A = np.random.randint(0, self.q, (self.n, self.n))
        e = np.random.normal(0, self.sigma, self.n).astype(int) % self.q
        b = (A @ s + e) % self.q
        
        return {'A': A, 'b': b}, s
    
    def encrypt(self, message_bit, public_key):
        """Encrypt a single bit using LWE"""
        A, b = public_key['A'], public_key['b']
        
        # Random vector r
        r = np.random.randint(0, 2, self.n)
        
        # Ciphertext
        u = (A.T @ r) % self.q
        v = (b @ r + message_bit * (self.q // 2)) % self.q
        
        return u, v
    
    def decrypt(self, ciphertext, private_key):
        """Decrypt using private key"""
        u, v = ciphertext
        s = private_key
        
        # Compute v - s^T * u
        result = (v - s @ u) % self.q
        
        # Decode bit
        if result > self.q // 2:
            return 1
        else:
            return 0
    
    def bch_encode(self, data, redundancy=3):
        """Simple BCH-like error correction encoding"""
        encoded = []
        for bit in data:
            # Add redundancy bits
            encoded.extend([bit] * redundancy)
        return encoded
    
    def bch_decode(self, encoded_data, redundancy=3):
        """Simple BCH-like error correction decoding"""
        decoded = []
        for i in range(0, len(encoded_data), redundancy):
            chunk = encoded_data[i:i+redundancy]
            # Majority voting
            decoded.append(1 if sum(chunk) > redundancy//2 else 0)
        return decoded
    
    def add_noise(self, data, error_rate=0.1):
        """Add transmission errors"""
        noisy_data = data.copy()
        for i in range(len(noisy_data)):
            if np.random.random() < error_rate:
                noisy_data[i] = 1 - noisy_data[i]  # Flip bit
        return noisy_data
    
    def simulate_full_process(self, message="Hello PQC!", error_rate=0.1):
        """Complete simulation of PQC with error correction"""
        results = {}
        
        # Convert message to bits
        message_bits = []
        for char in message:
            bits = format(ord(char), '08b')
            message_bits.extend([int(b) for b in bits])
        
        results['original_message'] = message
        results['message_bits'] = len(message_bits)
        
        # Key generation
        start_time = time.time()
        public_key, private_key = self.generate_keys()
        results['keygen_time'] = time.time() - start_time
        
        # Error correction encoding
        start_time = time.time()
        encoded_bits = self.bch_encode(message_bits)
        results['encoding_time'] = time.time() - start_time
        
        # Encryption
        start_time = time.time()
        ciphertexts = []
        for bit in encoded_bits:
            ciphertext = self.encrypt(bit, public_key)
            ciphertexts.append(ciphertext)
        results['encryption_time'] = time.time() - start_time
        
        # Decryption (simulate transmission)
        start_time = time.time()
        decrypted_bits = []
        for u, v in ciphertexts:
            decrypted_bit = self.decrypt((u, v), private_key)
            decrypted_bits.append(decrypted_bit)
        results['decryption_time'] = time.time() - start_time
        
        # Add transmission noise
        noisy_bits = self.add_noise(decrypted_bits, error_rate)
        errors_introduced = sum(1 for i in range(len(decrypted_bits)) 
                              if decrypted_bits[i] != noisy_bits[i])
        results['errors_introduced'] = errors_introduced
        
        # Error correction decoding
        start_time = time.time()
        corrected_bits = self.bch_decode(noisy_bits)
        results['decoding_time'] = time.time() - start_time
        
        # Reconstruct message
        recovered_message = ""
        for i in range(0, len(corrected_bits), 8):
            if i + 7 < len(corrected_bits):
                byte_bits = corrected_bits[i:i+8]
                char_code = sum(bit * (2 ** (7-j)) for j, bit in enumerate(byte_bits))
                if 32 <= char_code <= 126:  # Printable ASCII
                    recovered_message += chr(char_code)
        
        results['recovered_message'] = recovered_message
        results['success'] = message == recovered_message
        results['error_correction_rate'] = (errors_introduced - sum(1 for i in range(len(message_bits)) if i < len(corrected_bits) and message_bits[i] != corrected_bits[i])) / max(1, errors_introduced) if errors_introduced > 0 else 1.0
        results['ciphertext_size'] = len(ciphertexts) * 2 * self.n * 4  # bytes
        
        return results

# Flask app for PQC simulation
app_pqc = Flask(__name__)

@app_pqc.route('/pqc')
def pqc_home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Post-Quantum Cryptography Simulator</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .input-group { margin: 20px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #0056b3; }
            .results { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 5px; }
            .metric { display: inline-block; margin: 10px; padding: 10px; background: white; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
            .success { color: green; } .error { color: red; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Post-Quantum Cryptography Simulator</h1>
            <p><strong>Lattice-Based Encryption + Code-Based Error Correction</strong></p>
            
            <div class="input-group">
                <label>Message to Encrypt:</label>
                <textarea id="message" rows="3" placeholder="Enter your message here...">Hello PQC World!</textarea>
            </div>
            
            <div class="input-group">
                <label>Error Rate (0.0 - 1.0):</label>
                <input type="number" id="errorRate" value="0.1" min="0" max="1" step="0.01">
            </div>
            
            <button onclick="runSimulation()">🚀 Run PQC Simulation</button>
            
            <div id="results" class="results" style="display:none;">
                <h3>Simulation Results</h3>
                <div id="metrics"></div>
                <div id="messages"></div>
            </div>
        </div>

        <script>
            function runSimulation() {
                const message = document.getElementById('message').value;
                const errorRate = parseFloat(document.getElementById('errorRate').value);
                
                fetch('/pqc/simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message, error_rate: errorRate })
                })
                .then(response => response.json())
                .then(data => {
                    displayResults(data);
                })
                .catch(error => {
                    alert('Error: ' + error.message);
                });
            }
            
            function displayResults(data) {
                const resultsDiv = document.getElementById('results');
                const metricsDiv = document.getElementById('metrics');
                const messagesDiv = document.getElementById('messages');
                
                metricsDiv.innerHTML = `
                    <div class="metric"><strong>Key Generation:</strong> ${(data.keygen_time * 1000).toFixed(2)} ms</div>
                    <div class="metric"><strong>Encryption:</strong> ${(data.encryption_time * 1000).toFixed(2)} ms</div>
                    <div class="metric"><strong>Decryption:</strong> ${(data.decryption_time * 1000).toFixed(2)} ms</div>
                    <div class="metric"><strong>Encoding:</strong> ${(data.encoding_time * 1000).toFixed(2)} ms</div>
                    <div class="metric"><strong>Decoding:</strong> ${(data.decoding_time * 1000).toFixed(2)} ms</div>
                    <div class="metric"><strong>Errors Introduced:</strong> ${data.errors_introduced}</div>
                    <div class="metric"><strong>Error Correction Rate:</strong> ${(data.error_correction_rate * 100).toFixed(1)}%</div>
                    <div class="metric"><strong>Ciphertext Size:</strong> ${data.ciphertext_size.toFixed(0)} bytes</div>
                `;
                
                const successClass = data.success ? 'success' : 'error';
                messagesDiv.innerHTML = `
                    <h4>Message Recovery:</h4>
                    <p><strong>Original:</strong> "${data.original_message}"</p>
                    <p><strong>Recovered:</strong> <span class="${successClass}">"${data.recovered_message}"</span></p>
                    <p><strong>Status:</strong> <span class="${successClass}">${data.success ? '✅ SUCCESS' : '❌ FAILED'}</span></p>
                `;
                
                resultsDiv.style.display = 'block';
            }
        </script>
    </body>
    </html>
    '''

@app_pqc.route('/pqc/simulate', methods=['POST'])
def simulate_pqc():
    data = request.get_json()
    message = data.get('message', 'Hello PQC!')
    error_rate = data.get('error_rate', 0.1)
    
    simulator = PQCSimulator()
    results = simulator.simulate_full_process(message, error_rate)
    
    return jsonify(results)

if __name__ == '__main__':
    app_pqc.run(debug=True, port=5001)