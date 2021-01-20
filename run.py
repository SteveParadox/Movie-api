from dev import create_app, db


app = create_app()
app.app_context().push()

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False
    threaded = True


if __name__ == '__main__':
    app.run(debug=True)
    #db.drop_all(app=create_app())
    #db.create_all(app=create_app())
