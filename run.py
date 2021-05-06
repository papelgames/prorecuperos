from app import app, db, mail


if __name__ == "__main__":
    db.create_all()
    app.run()