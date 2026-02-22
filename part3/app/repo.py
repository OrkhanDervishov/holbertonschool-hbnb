from app import db

class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.query.all()

    def get_by_id(self, id):
        return self.model.query.get(id)

    def add(self, instance):
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self):
        db.session.commit()

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()