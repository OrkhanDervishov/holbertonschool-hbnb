class DevelopmentConfig:
    SECRET_KEY = "super-secret-key"
    JWT_SECRET_KEY = "super-secret-key"  # used by flask-jwt-extended
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False