from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from models import Session, Ads

app = Flask('app')


class HttpError(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


def get_ads(session, ads_id):
    ads = session.get(Ads, ads_id)
    if ads is None:
        raise HttpError(404, 'user not found')
    return ads


class AdsView(MethodView):
    # получать объявление
    def get(self, ads_id):
        with Session() as session:
            ads = get_ads(session, ads_id)
        return jsonify({
            'id': ads.id,
            'title': ads.title,
            'description': ads.description,
            'owner': ads.owner,
            'creation_time': ads.creation_time.isoformat()
        })

    # создавать объявление
    def post(self):
        validated_json = request.json
        with Session() as session:
            ads = Ads(**validated_json)
            session.add(ads)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'user already exists')
            return jsonify({
                'id': ads.id
            })

    # удалять объявление
    def delete(self, ads_id):
        with Session() as session:
            ads = get_ads(session, ads_id)
            session.delete(ads)
            session.commit()
            return jsonify({
                'status': 'success'
            })


ads_view = AdsView.as_view('adss')
app.add_url_rule('/ads/<int:ads_id>',
                 view_func=ads_view,
                 methods=['GET', 'DELETE'])
app.add_url_rule('/ads/',
                 view_func=ads_view,
                 methods=['POST'])

if __name__ == "__main__":
    app.run()
