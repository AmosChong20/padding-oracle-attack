# Padding Oracle Attack Project

## Overview

This project implements a Padding Oracle Attack on AES-CBC with PKCS#7 padding. It includes a challenge server that acts as a padding oracle and an attack client that exploits the oracle to decrypt ciphertext without the encryption key.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AmosChong20/padding-oracle-attack.git
cd padding-oracle-attack
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

- **On Windows:**

```bash
venv\Scripts\activate
```

- **On macOS and Linux:**

```bash
source venv/bin/activate
```

### 4. Install Required Dependencies

```bash
pip install requirements.txt
```

### 5. Running the Server

```bash
python challenge_server.py
```

The server will start listening for incoming connections.

### 6. Running the Client

```bash
python attack_client.py
```

### 7. Deactivating the Virtual Environment

```bash
deactivate
```

## Project Structure

```
padding-oracle-attack/
│
├── challenge_server.py    # Server implementation for the padding oracle
├── attack_client.py       # Client implementation for the padding oracle attack
├── shared_constants.py    # Contains shared constants for server and client
```
