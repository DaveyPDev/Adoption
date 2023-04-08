from flask_sqlalchemy import SQLAlchemy

GENERIC_IMAGE = "https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif"

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    with app.app_context():
        # db.session.query(Pet).delete()
        db.create_all()


class Pet(db.Model):
    """ Adopt a Pet """

    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)

    def image_url(self):
        """ Image for Pet """

        return self.photo_url or GENERIC_IMAGE





