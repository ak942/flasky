import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.crystal import Crystal


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
		#creating an app object used in app/_init, TESTING is true to access testing db

    @request_finished.connect_via(app) #only runs when request is completed
    def expire_session(sender, response, **extra):
        db.session.remove()
	#code above makes sure that the tests are checkin the database for updates,etc.

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()
#after the testing is done, then the data is removed to restart for next test

#this is a dummy client that is used in the test env
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def make_two_crystals(app):
    crystal_1 = Crystal(
        name = "pearl",
        color = "white",
        powers = "pretty"
    )
    crystal_2 = Crystal(
        name = "garnet",
        color = "red",
        powers = "Awesomeness + protection against disasters"
    )
    db.session.add_all([crystal_1, crystal_2])
    db.session.commit()
