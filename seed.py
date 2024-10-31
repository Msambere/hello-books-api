from app import create_app, db
from app.models.book import Book


my_app = create_app()
with my_app.app_context():
    db.session.add(Book(title= "10,000 Apples", description="When all you need is an orange... Now isn't that ironic? Don't you think?"))
    db.session.add(Book(title= "It's Not Easy Being an Orange", description="Limes and apples aren't the only ones with problems, you know!"))
    db.session.add(Book(title= "An Apple a Day", description="When Shay fell for a doctor, would a love of apples spell disaster for their happiness?"))
    db.session.add(Book(title= "Children of Blood and Bone", description="A fantasy novel set in Africa"))
    db.session.add(Book(title= "The Way of Kings", description="A fantasy novel by Brandon Sanderson"))
    db.session.add(Book(title= "The life of Nelson Mandela", description="A non-fiction book about one of Africa's greatest leaders"))
    # db.session.add(Book(title= "", description=""))
    # db.session.add(Book(title= "", description=""))
    db.session.commit()


    # curl -X POST -H 'Content-Type: application/json' -d '{"name":"Felix","color":"black and white","personality":"wonderful"}' 'http://localhost:5000/cats' | json_p