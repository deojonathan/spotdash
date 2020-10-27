import sqlalchemy
from sqlalchemy.ext import declarative

_base = declarative.declarative_base()

class OAuth2Token(_base):
  __tablename__ = 'AuthTokens'

  id = sqlalchemy.Column(
    sqlalchemy.Integer,
    primary_key=True,
    autoincrement=True
  )
  username = sqlalchemy.Column(
    sqlalchemy.String(255),
    nullable=True
  )
  email = sqlalchemy.Column(
    sqlalchemy.String(255),
    nullable=True
  )
  access_token = sqlalchemy.Column(
    sqlalchemy.String(255),
    nullable=True
  )
  refresh_token = sqlalchemy.Column(
    sqlalchemy.String(255),
    nullable=True
  )
  token_type = sqlalchemy.Column(
    sqlalchemy.String(255),
    nullable=True
  )
  expires_at = sqlalchemy.Column(
    sqlalchemy.String(255),
    nullable=True,
  )

  def __iter__(self):
    yield 'access_token', self.access_token
    yield 'refresh_token', self.refresh_token
    yield 'token_type', self.token_type
    yield 'expires_at', self.expires_at

  def __repr__(self):
    return (f"<OAuth2Token(id={self.id}, username={self.username}, "
            f"email={self.email}, access_token={self.access_token}, "
            f"refresh_token={self.refresh_token}, "
            f"token_type={self.token_type}, expires_at={self.expires_at})>")
