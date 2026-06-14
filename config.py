class Config:

    APP_Name = "SherpaBuddy"

    #Secret key for session management
    SECRET_KEY = "trekking-project-secret"

    #Database configuration
    SQLALCHEMY_DATABASE_URI = "sqlite:///trek.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "static/uploads"
    TREKS_PER_PAGE = 10
    
    #admin creds
    ADMIN_USERNAME = "admin"
    ADMIN_EMAIL = "admin@sherpabuddy.com"

    BACKGROUND_IMAGE = "images/Background.png"