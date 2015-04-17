from itemcatalogapp import app

if __name__ == '__main__':
        app.secret_key = 'super_secret_key' # for user session - usually super secure
        app.debug = True # server reloads itself every time there's a change
        app.run(host = '0.0.0.0', port = 5000) # 0.0.0.0 >> all public IP adresses (for debug purposes)
