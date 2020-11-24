from Api import create_app, db, io, app

app = create_app()
app.app_context().push()

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

if __name__ == '__main__':
    io.run(app, debug=True, port=5000)
    #db.drop_all(app=create_app())
    #db.create_all(app=create_app())
