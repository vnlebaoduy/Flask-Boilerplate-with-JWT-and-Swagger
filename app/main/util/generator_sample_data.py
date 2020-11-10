from datetime import date, datetime
import logging
from app.main import db
from app.main.model.role import Role, RolePermission
from app.main.model.user import User, UserRole
from app.main.model.permission import Permission
import uuid
import os
import json


class Seed:
    @staticmethod
    def gen_role():
        logging.info("Generating Role ...")
        os.chdir(os.path.dirname(__file__))
        path = os.getcwd()
        with open(os.path.join(path, 'sample/role.json')) as json_file:
            data = json.load(json_file)
            for p in data:
                role = Role(name=p['name'], description=p['description'])
                db.session.add(role)
            try:
                db.session.commit()
                logging.info("Generate Role Completed !")
            except Exception as e:
                db.session.rollback()
                logging.error("Generate Role Failure !")
                logging.error(str(e))

    @staticmethod
    def gen_user():
        logging.info("Generating User ...")
        os.chdir(os.path.dirname(__file__))
        path = os.getcwd()
        with open(os.path.join(path, './sample/user.json')) as json_file:
            data = json.load(json_file)
            for p in data:
                user = User(full_name=p['full_name'], email=p['email'], username=p['username'],
                            password=p['password'], registered_on=datetime.utcnow(), public_id=str(uuid.uuid4()),
                            is_active=True)
                db.session.add(user)
            try:
                db.session.commit()
                logging.info("Generate User Completed !")
            except Exception as e:
                db.session.rollback()
                logging.error("Generate User Failure !")
                logging.error(str(e))

    @staticmethod
    def gen_user_role():
        logging.info("Generating User Role ...")
        os.chdir(os.path.dirname(__file__))
        path = os.getcwd()
        with open(os.path.join(path, './sample/user_role.json')) as json_file:
            data = json.load(json_file)
            try:
                for p in data:
                    sql = 'INSERT INTO user_role (role_id, user_id,created_at) VALUES (:role_id, :user_id,:created_at)'
                    db.engine.execute(sql, {
                        "role_id": p['role_id'],
                        "user_id": p['user_id'],
                        "created_at": datetime.utcnow()
                    })
                logging.info("Generate User Role Completed !")
            except Exception as e:
                db.session.rollback()
                logging.error("Generate User Role Failure !")
                logging.error(str(e))

    @staticmethod
    def gen_permission():
        logging.info("Generating Permission ...")
        os.chdir(os.path.dirname(__file__))
        path = os.getcwd()
        with open(os.path.join(path, './sample/permission.json')) as json_file:
            data = json.load(json_file)
            for p in data:
                permission = Permission(name=p['name'], description=p['description'])
                db.session.add(permission)
            try:
                db.session.commit()
                logging.info("Generate Permission Completed !")
            except Exception as e:
                db.session.rollback()
                logging.error("Generate Permission Failure !")
                logging.error(str(e))

    @staticmethod
    def gen_role_permission():
        logging.info("Generating Role Permission ...")
        os.chdir(os.path.dirname(__file__))
        path = os.getcwd()
        with open(os.path.join(path, './sample/role_permission.json')) as json_file:
            data = json.load(json_file)
            try:
                for p in data:
                    sql = 'INSERT INTO role_permission (role_id, permission_id, created_at) ' \
                          'VALUES (:role_id, :permission_id, :created_at)'
                    db.engine.execute(sql, {
                        "role_id": p['role_id'],
                        "permission_id": p['permission_id'],
                        "created_at": datetime.utcnow()
                    })
                logging.info("Generate Role Permission Completed !")
            except Exception as e:
                db.session.rollback()
                logging.error("Generate Role Permission Failure !")
                logging.error(e)
