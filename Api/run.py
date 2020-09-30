from api import create_app

app = create_app()
app.app_context().push()

ENV= 'dev'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

if __name__ == '__main__':
    app.run(debug=True)