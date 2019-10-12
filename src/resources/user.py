from flask_restful import Resource, reqparse

from app import db
from utils import json_serialize
from models import User


class UserListApi(Resource):
    """API Endpoint for listing and creating Users"""
    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("fname", type=str, required=True, help="No First Name Provided", location="json")
        self.parser.add_argument("lname", type=str, required=True, help="No First Name Provided", location="json")
        self.parser.add_argument("credit_score", type=int, required=False, help="Invalid Credit Score Provided", location="json")
        return super().__init__(*args, **kwargs)

    def get(self):
        """API Endpoint for getting all user instances"""
        return json_serialize(User.query.all())

    def put(self):
        """API Endpoint for creating user instance"""
        args = self.parser.parse_args()
        user = User(
            fname=args['fname'],
            lname=args['lname']
        )
        if args['credit_score']:
            user.credit_score = args['credit_score']
        db.session.add(user)
        db.session.commit()
        return json_serialize(user)
        

class UserApi(Resource):
    """API Endpoint for working with User instances"""
    def __init__(self, *args, **kwargs):
        """Initializer extension provides an argument parser for all methods to use at will"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("fname", type=str, required=False, help="No First Name Provided", location="json")
        self.parser.add_argument("lname", type=str, required=False, help="No First Name Provided", location="json")
        self.parser.add_argument("credit_score", type=int, required=False, help="Invalid Credit Score Provided", location="json")
        return super().__init__(*args, **kwargs)

    def get(self, user_id):
        """API Endpoint for getting user instance"""
        user = User.query.get_or_404(user_id)
        return json_serialize(user)

    def post(self, user_id):
        """API Endpoint for updating user instance"""
        user = User.query.get_or_404(user_id)
        args = self.parser.parse_args()
        for prop in ["fname", "lname", "credit_score"]:
            if prop in args:
                setattr(user, prop, args[prop])
        db.session.commit()
        return json_serialize(user)

    def delete(self, user_id):
        """API Endpoint for deleting user instance"""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return json_serialize(user)
        
