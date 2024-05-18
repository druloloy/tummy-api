from app import db
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import UUID, JSON
from urllib.parse import urlparse

class Recipe(db.Model):
    __tablename__ = 'recipes'
    __table_args__ = {'schema': 'core'}

    _id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'), nullable=False)
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('core.users._id'), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(200))
    ingredients = db.Column(JSON, nullable=False)
    procedure = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.text('transaction_timestamp()'), nullable=False)
    

    def __init__(self, _id, owner_id, title, description, ingredients, procedure, image_url = None):
        self._id = _id
        self.owner_id = owner_id
        self.title = title
        self.description = description
        self.ingredients = ingredients
        self.procedure = procedure
        self.image_url = image_url

    def __repr__(self):
        return '<Recipe %r>' % self.title
    
    def as_dict(self):
        """Returns a dict representation of the recipe"""
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }
    
    @validates('image_url')
    def validate_uri(self, key, value):
        """
        Validates the given URI for the 'image_url' attribute.

        Parameters:
            key (str): The key of the attribute being validated.
            value (str): The value of the attribute being validated.

        Returns:
            str: The validated URI if it is valid, otherwise raises an AssertionError.

        Raises:
            AssertionError: If the URI is invalid.

        Notes:
            This function uses the `urlparse` function from the `urllib.parse` module to parse the URI.
            It checks if both the scheme and netloc (domain) are present in the parsed URI.
            If the URI is valid, it returns the original value.
            Otherwise, it raises an AssertionError with the message 'Invalid image URI.'.
        """
        try:
            result = urlparse(value)
            if all([result.scheme, result.netloc]):
                return value
            else:
                raise AssertionError
        except:
            raise AssertionError('Invalid image URI.')