from website import create_app

app = create_app() 

if __name__ == '__main__':
    #app.run(debug=True) #only want to run server if this file is run directly
    app.run(host='0.0.0.0', port=5000)

    