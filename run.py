from flaskserver import create_app, db
from sqlalchemy.exc import OperationalError
from psycopg2 import OperationalError as Psycopg2OperationalError

app = create_app()

@app.errorhandler(OperationalError)
def handle_db_disconnect(exception):
    if isinstance(exception.orig, Psycopg2OperationalError):
        # Log the disconnect here, if desired
        # Attempt to dispose the current pool and create a new one
        db.engine.dispose()
        # Depending on your needs, you may wish to return a custom response or raise the exception again
        return "Database connection refreshed", 500
    else:
        # If it's not a disconnection error, propagate the exception
        raise exception

if __name__ == '__main__':
    app.run(port=8000, debug=True)