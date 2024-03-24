from controllers import app

if __name__ == '__main__':
    print("Servidor a correr em http://localhost:8082")
    app.run(host="0.0.0.0", port=8082, debug=True)
