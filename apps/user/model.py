from app import db
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import UUID
import re
import enum
from apps.recipe.model import Recipe

class GenderType(enum.Enum):
    m = 1
    f = 2
    a = 3
    o = 4

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'core'}

    _id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'), nullable=False)
    _auth_id = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    is_user_verified = db.Column(db.Boolean, default=False)
    gender = db.Column(db.Enum(GenderType, name='gender_type'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.text('transaction_timestamp()'), nullable=False)

    recipes = db.relationship('Recipe', backref='core.users', lazy=True)

    def __init__(self, _auth_id, email, username, first_name, last_name, dob, is_user_verified = False, gender = None):
        self._auth_id = _auth_id
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.is_user_verified = is_user_verified
        self.gender = gender
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    def as_dict(self):
        """Returns a dict representation of the user"""
        return {
            col.name: getattr(self, col.name).name
            if isinstance(getattr(self, col.name), enum.Enum)
            else getattr(self, col.name)
            for col in self.__table__.columns
        }
    def as_discreet_dict(self, *discluded_columns):
        """Returns a dict representation of the user without sensitive information"""
        return {
            col.name: getattr(self, col.name).name
            if isinstance(getattr(self, col.name), enum.Enum)
            else getattr(self, col.name) if col.name not in list(discluded_columns) else None
            for col in self.__table__.columns
            if col.name not in list(discluded_columns)
        }

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        acceptable_characters = re.compile(r"^[A-Za-zÁáÀàÂâĂăÄäÅåÃãǍǎÆæÇçĆćĈĉĊċČčÐðÉéÈèÊêËëĚěĔĕĖėȨȩĘęẼẽĜĝĞğĠġĢģĤĥĦħÍíÌìÎîÏïĨĩĪīĬĭĮįĲĳĴĵĶķĹĺĻļĽľŁłḸḹḼḽŃńŇňÑñŅņǸǹŊŋÓóÒòÔôÖöÕõŐőǑǒØøǾǿŒœŔŕŘřŚśŜŝŞşŠšŢţŤťŦŧÚúÙùÛûÜüŨũŪūŬŭŮůŰűŲųẂẃẀẁŴŵÝýỲỳŶŷŸÿŹźŻżŽž]+(?:[ -][A-Za-zÁáÀàÂâĂăÄäÅåÃãǍǎÆæÇçĆćĈĉĊċČčÐðÉéÈèÊêËëĚěĔĕĖėȨȩĘęẼẽĜĝĞğĠġĢģĤĥĦħÍíÌìÎîÏïĨĩĪīĬĭĮįĲĳĴĵĶķĹĺĻļĽľŁłḸḹḼḽŃńŇňÑñŅņǸǹŊŋÓóÒòÔôÖöÕõŐőǑǒØøǾǿŒœŔŕŘřŚśŜŝŞşŠšŢţŤťŦŧÚúÙùÛûÜüŨũŪūŬŭŮůŰűŲųẂẃẀẁŴŵÝýỲỳŶŷŸÿŹźŻżŽž]+)*$")

        if not value:
            raise AssertionError('Names cannot be empty.')

        if len(value) < 2:
            raise AssertionError('First name or Last name should be at least 2 characters long.')

        if not acceptable_characters.match(value):
            raise AssertionError('Names should only contain letters.')
        
        return value
    
    @validates('username')
    def validate_username(self, key, value):
        acceptable_characters = re.compile(r"^[a-z0-9_-]{3,15}$")

        if not value:
            raise AssertionError('Names cannot be empty.')

        if not acceptable_characters.match(value):
            raise AssertionError('Username should only contain letters, numbers, and underscores and should be between 3 and 15 characters.')

        return value
    
    @validates('email')
    def validate_email(self, key, value):
        acceptable_characters = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        if not value:
            raise AssertionError('Email cannot be empty.')

        if not acceptable_characters.match(value):
            raise AssertionError('Email is not valid.')
        
        return value    
    def validate_gender(self, key, value):  
        # if value is not in GenderType
        if value not in GenderType.__members__:
            raise AssertionError('Gender is not valid.')
        
        return value


    
