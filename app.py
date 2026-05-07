from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_cors import CORS
import pandas as pd  # For handling Excel files
from scraper import search_keyword

# Initialize Flask app
app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/')
def home():
    return "Hello, World!"

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define database models
class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(100), nullable=False)

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# API Resources
class SiteResource(Resource):
    def get(self):
        sites = Site.query.all()
        return jsonify([{'id': s.id, 'name': s.name, 'domain': s.domain} for s in sites])

    def post(self):
        data = request.get_json()
        if not data.get('name') or not data.get('domain'):
            return jsonify({'error': 'Name and domain are required!'}), 400

        new_site = Site(name=data['name'], domain=data['domain'])
        db.session.add(new_site)
        db.session.commit()
        return jsonify({'message': 'Site added successfully!'}), 201

class KeywordResource(Resource):
    def get(self):
        keywords = Keyword.query.all()
        return jsonify([{'id': k.id, 'keyword': k.keyword, 'site_id': k.site_id} for k in keywords])

    def post(self):
        data = request.get_json()
        if not data.get('keyword') or not data.get('site_id'):
            return jsonify({'error': 'Keyword and site_id are required!'}), 400

        site = Site.query.get(data['site_id'])
        if not site:
            return jsonify({'error': 'Associated site not found!'}), 404

        new_keyword = Keyword(keyword=data['keyword'], site_id=data['site_id'])
        db.session.add(new_keyword)
        db.session.commit()
        return jsonify({'message': 'Keyword added successfully!'}), 201

class RunScraperResource(Resource):
    def get(self):
        try:
            results = search_keywords()
            for result in results:
                db.session.add(Result(**result))
            db.session.commit()
            return jsonify({'message': 'Scraper executed successfully!', 'results': results}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

class LogResource(Resource):
    def get(self):
        logs = Log.query.order_by(Log.timestamp.desc()).all()
        return jsonify([{'id': log.id, 'message': log.message, 'timestamp': log.timestamp} for log in logs])

# Add resources to API
api.add_resource(SiteResource, '/sites', '/sites/<int:site_id>')
api.add_resource(KeywordResource, '/keywords', '/keywords/<int:keyword_id>')
api.add_resource(RunScraperResource, '/run-scraper')
api.add_resource(LogResource, '/logs')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

