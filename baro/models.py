import enum
from datetime import datetime
from baro import db


class RequestType(enum.Enum):
    Create = 1
    Edit = 2


class PersonType(enum.Enum):
    worker = 1
    professor = 2
    student = 3


class Request(db.Model):
    __tablename__ = "baro_request"
    __table_args__ = {"mysql_collate": "utf8_general_ci"}

    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.Enum(RequestType))
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
        self.request_type = RequestType.Create
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


class Url(db.Model):
    __tablename__ = "baro_url"
    __table_args__ = {"mysql_collate": "utf8_general_ci"}

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("baro_request.id"))
    request = db.relationship("Request")
    keyword = db.Column(db.String(128))
    url = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    click_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(
        self, keyword, url, title, description, email, name, group, ip_address
    ):
        self.keyword = keyword
        self.url = url
        self.title = title
        self.description = description
        self.email = email
        self.name = name
        self.group = group
        self.ip_address = ip_address

        self.click_count = 0


class Log(db.Model):
    __tablename__ = "baro_log"
    __table_args__ = {"mysql_collate": "utf8_general_ci"}

    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey("baro_url.id"))
    url = db.relationship("Url")
    referrer = db.Column(db.Text)
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(41))
    country_code = db.Column(db.String(2))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, url_id, referrer, user_agent, ip_address, country_code):
        self.referrer = referrer
        self.user_agent = user_agent
        self.ip_address = ip_address
        self.country_code = country_code
