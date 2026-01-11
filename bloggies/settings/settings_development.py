from .base import *


DEBUG = True
SECRET_KEY = "pzm!wg763dggm*8#f!vi$jp&gp^l!2%j55gqyb^9t&sgwcn^53"
AUTH_PASSWORD_VALIDATORS = []

ALLOWED_HOSTS = ["*", "bloggies.test", ".bloggies.test"]
CSRF_TRUSTED_ORIGINS = []

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# CORS settings for local development (relaxing security)
CORS_ALLOW_CREDENTIALS = True  # Allow credentials (cookies, auth headers) in CORS requests
# CORS_ALLOW_ORIGINS = ["dev.localhost.com"]  # Only allow requests from this domain
CORS_ALLOW_ALL_ORIGINS = True  # WARNING: Allows all domains (disable in production!)

# Security settings for development (disable strict HTTPS enforcement)
SECURE_SSL_REDIRECT = False  # HTTPS redirection disabled (needed for local HTTP access)
CSRF_COOKIE_SECURE = False  # CSRF cookies allowed over HTTP (enable in production)
SESSION_COOKIE_SECURE = False  # Session cookies allowed over HTTP (enable in production)

SESSION_COOKIE_DOMAIN = ".bloggies.test"  # Cookies will be shared accross subdomains
CSRF_COOKIE_DOMAIN = ".bloggies.test"

LOGGING = {
    "version": 1,  # Version of the logging configuration (always 1)
    "disable_existing_loggers": False,  # Ensures that Django’s default loggers are not disabled

    # Define the format of log messages
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },

    # Define where the log messages are sent
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",  # Use the "verbose" formatter for console logs
        },
    },

    # Define the loggers themselves
    "loggers": {
        "aerobox": {
            "handlers": ["console"],  # Send logs to console
            "level": "DEBUG",  # Log everything, including info messages
            "propagate": False,
        },
    },
}

# Utils
SITE_DOMAIN = "bloggies.test:8000"
SITE_SCHEME = "http"
