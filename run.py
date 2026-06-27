from project import app


if __name__ == "__main__":
    app.run(host=app.config["FLASK_RUN_HOST"], port=app.config["FLASK_RUN_PORT"], debug=app.config["FLASK_DEBUG"], use_reloader=False)
