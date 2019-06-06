import enum
from sqlalchemy.inspection import inspect
from datetime import datetime
from baro import db


class PersonType(enum.Enum):
    worker = 1
    professor = 2
    student = 3


class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Request(db.Model, Serializer):
    __tablename__ = "request"
    __table_args__ = {"mysql_collate": "utf8_general_ci"}

    id = db.Column(db.Integer, primary_key=True)
    person_type = db.Column(db.Enum(PersonType))
    keyword = db.Column(db.String(128))
    url = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    email = db.Column(db.String(64))
    name = db.Column(db.String(32))
    group = db.Column(db.String(32))
    ip_address = db.Column(db.String(41))

    is_approved = db.Column(db.Boolean, default=0)
    disapproved_reason = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(
        self,
        keyword,
        url,
        title,
        description,
        person_type,
        email,
        name,
        group,
        ip_address,
    ):
        self.keyword = keyword
        self.url = url
        self.title = title
        self.description = description
        self.person_type = person_type
        self.email = email
        self.name = name
        self.group = group
        self.ip_address = ip_address

        self.is_approved = 0
        self.disapproved_reason = None

    def serialize(self):
        d = Serializer.serialize(self)
        del d["person_type"]
        return d


class Url(db.Model, Serializer):
    __tablename__ = "url"
    __table_args__ = {"mysql_collate": "utf8_general_ci"}

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(128))
    url = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    hit_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, keyword, url, title, description):
        self.keyword = keyword
        self.url = url
        self.title = title
        self.description = description
        self.hit_count = 0

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Log(db.Model):
    __tablename__ = "log"
    __table_args__ = {"mysql_collate": "utf8_general_ci"}

    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey("url.id"))
    url = db.relationship("Url")
    referrer = db.Column(db.Text, nullable=True)
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(41))
    country_code = db.Column(db.String(2), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, url_id, referrer, user_agent, ip_address, country_code):
        self.url_id = url_id
        self.referrer = referrer
        self.user_agent = user_agent
        self.ip_address = ip_address
        self.country_code = country_code
