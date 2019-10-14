from utils import json_serialize
from flask_restful import Resource, reqparse

from app import db
from models import Bank, BankBranch, Staff, User


_bank_parser = reqparse.RequestParser()
_bank_parser.add_argument(name="name", type=str, required=True, help="No Bank Name Provided", location="json")


class BankListApi(Resource):
    """API Endpoint for accessing all banks and for adding new banks
    """
    def get(self):
        """API Endpoint for getting all banks"""
        return json_serialize(Bank.query.all())

    def put(self):
        """API Endpoint for creating new bank
        """
        args = _bank_parser.parse_args()
        bank = Bank(name=args['name'])
        db.session.add(bank)
        db.session.commit()
        return json_serialize(bank)


class BankApi(Resource):
    """API Endpoint for interacting with specific banks
    """

    def get(self, bank_id):
        """API Endpoint for getting individual bank
        """
        return json_serialize(Bank.query.get_or_404(bank_id))

    def post(self, bank_id):
        """API Endpoint for changing bank instance data
        """
        args = _bank_parser.parse_args()
        bank = Bank.query.get_or_404(bank_id)
        bank.update(args)
        db.session.commit()
        return json_serialize(bank)

    def delete(self, bank_id):
        """API Endpoint for Deleting bank instance
        """
        bank = Bank.query.get_or_404(bank_id)
        db.session.delete(bank)
        db.session.commit()
        return json_serialize(bank)


_branch_parser = reqparse.RequestParser()
_branch_parser.add_argument(name="name", type=str, required=True, help="No Branch Name Provided", location="json")


class BranchListApi(Resource):
    """API Endpoint for interacting with all bank branches at a specific bank
    """

    def get(self, bank_id):
        """API Endpoint for getting all branches for a given bank
        """
        bank = Bank.query.get_or_404(bank_id)
        branches = BankBranch.query.filter_by(bank=bank).all()
        return json_serialize(branches)

    def put(self, bank_id):
        """API Endpoint for adding a branch to a given bank
        """
        args = _branch_parser.parse_args()
        bank = Bank.query.get_or_404(bank_id)
        branch = BankBranch(name=args['name'], bank=bank)
        db.session.add(branch)
        db.session.commit()
        return json_serialize(branch)


class BranchApi(Resource):
    """API Endpoint for interacting with all bank branches at a specific bank.
    """
    def get(self, bank_id, branch_id):
        """API Endpoint for getting branch instance
        """
        bank = Bank.query.get_or_404(bank_id)
        branch = BankBranch.query.filter_by(bank=bank, id=branch_id).first_or_404()
        return json_serialize(branch)

    def post(self, bank_id, branch_id):
        """API Endpoint for modifying branch instance
        """
        args = _branch_parser.parse_args()
        bank = Bank.query.get_or_404(bank_id)
        branch = BankBranch.query.filter_by(bank=bank, id=branch_id).first_or_404()
        branch.update(args)
        db.session.commit()
        return json_serialize(branch)

    def delete(self, bank_id, branch_id):
        """API Endpoint for deleting branch instance
        """
        bank = Bank.query.get_or_404(bank_id)
        branch = BankBranch.query.filter_by(bank=bank, id=branch_id).first_or_404()
        db.session.delete(branch)
        db.session.commit()
        return json_serialize(branch)


_staff_create_parser = reqparse.RequestParser()
_staff_create_parser.add_argument("user_id", type=int, required=True, help="No User Id Provided", location="json")
_staff_create_parser.add_argument("role", type=int, required=True, help="No Role Provided", location="json")


class StaffListApi(Resource):
    """API Endpoint for getting and adding staff at a given bank branch
    """
    def get(self, bank_id, branch_id):
        """API Endpoint for getting all staff for a branch instance
        """
        bank = Bank.query.get_or_404(bank_id)
        branch = BankBranch.query.filter_by(bank=bank, id=branch_id).first_or_404()
        staff = branch.staff
        return json_serialize(staff)

    def put(self, bank_id, branch_id):
        """API Endpoint for adding staff to a branch instance
        """
        args = _staff_create_parser.parse_args()
        bank = Bank.query.get_or_404(bank_id)
        branch = BankBranch.query.filter_by(bank=bank, id=branch_id).first_or_404()
        user = User.query.get_or_404(args['user_id'])
        staff = Staff(branch=branch, user=user, role=args['role'])
        user.staff = staff
        db.session.add(staff)
        db.session.commit()
        return json_serialize(staff)


_staff_update_parser = reqparse.RequestParser()
_staff_update_parser.add_argument("role", type=int, required=True, help="No Role Provided", location="json")


class StaffApi(Resource):
    """API Endpoint for managing staff instances
    """
    def get(self, bank_id, branch_id, staff_id):
        """API Endpoint for getting staff instance
        """
        staff = Staff.query.get_or_404(staff_id)
        return json_serialize(staff)

    def post(self, bank_id, branch_id, staff_id):
        """API Endpoint for updating staff instance
        """
        args = _staff_update_parser.parse_args()
        staff = Staff.query.get_or_404(staff_id)
        staff.update(args)
        db.session.commit()
        return json_serialize(staff)

    def delete(self, bank_id, branch_id, staff_id):
        """API Endpoint for deleting staff instance
        """
        staff = Staff.query.get_or_404(staff_id)
        db.session.delete(staff)
        db.session.commit()
        return json_serialize(staff)

