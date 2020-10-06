from base import create_app

app = create_app()
app.app_context().push()

ENV= 'dev'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

if __name__ == '__main__':
    app.run(host="127.1.1.4", debug=True)