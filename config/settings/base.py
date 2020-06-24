"""
Base settings to build other settings files upon.
"""
from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
import environ
import os.path
from django_prices.utils.formatting import get_currency_fraction

def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e
    return default_value


ROOT_DIR = Path(__file__).parents[2]
# kda/)
APPS_DIR = ROOT_DIR / "kda"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Africa/Nairobi"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# DATABASES = {
#     "default": env.db("DATABASE_URL", default="postgres:///kda")
# }
# DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(ROOT_DIR, "db.sqlite3"),
    }
}
# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    'whitenoise.runserver_nostatic',
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",

]
THIRD_PARTY_APPS = [
    "crispy_forms",
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    "channels",
    "django_celery_beat",
    "rest_framework",
    "rest_framework.authtoken",

    # New Apps
    "graphene_django",
    "django_filters",
    "graphql_auth",
    "django_graphiql",


    "django_prices",
    "django_prices_openexchangerates",
    "django_prices_vatlayer",
    "mptt",
    "django_countries",
    "phonenumber_field",

    # refresh tokens are optional
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',

]

LOCAL_APPS = [
    # "kda.users.apps.UsersConfig",

    # custom apps go here

    "kda.core.apps.CoreConfig",
    "kda.account.apps.AccountConfig",
    "kda.order.apps.OrderConfig",
    "kda.graphql.apps.GraphqlConfig",
    "kda.trips.apps.TripsConfig",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
# MIGRATION_MODULES = {"sites": "kda.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "graphql_auth.backends.GraphQLAuthBackend",
    # "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "account.CustomUser"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
# LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
# LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise Middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        # 'APP_DIRS': True,
        "DIRS": [str(APPS_DIR / "templates")],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "kda.utils.context_processors.settings_context",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Lawrence Mathenge Kamau""", "lawrencekamau5@gmail.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "kda.account.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "kda.account.adapters.SocialAccountAdapter"

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}
# Your stuff...
# ------------------------------------------------------------------------------

#Versatile Image Field


VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "products": [
        ("product_gallery", "thumbnail__540x540"),
        ("product_gallery_2x", "thumbnail__1080x1080"),
        ("product_small", "thumbnail__60x60"),
        ("product_small_2x", "thumbnail__120x120"),
        ("product_list", "thumbnail__255x255"),
        ("product_list_2x", "thumbnail__510x510"),
    ],
    "background_images": [("header_image", "thumbnail__1080x440")],
    "user_avatars": [("default", "thumbnail__445x445")],
}

# VERSATILEIMAGEFIELD_SETTINGS = {
#     # Images should be pre-generated on Production environment
#     "create_images_on_demand": get_bool_from_env("CREATE_IMAGES_ON_DEMAND", DEBUG)
# }

PLACEHOLDER_IMAGES = {
    60: "images/placeholder60x60.png",
    120: "images/placeholder120x120.png",
    255: "images/placeholder255x255.png",
    540: "images/placeholder540x540.png",
    1080: "images/placeholder1080x1080.png",
}
# GRAPHENE = {
#     'SCHEMA': 'quickstart.schema.schema', # this file doesn't exist yet
#     'MIDDLEWARE': [
#         'graphql_jwt.middleware.JSONWebTokenMiddleware',
#     ],
# }
ENABLE_DEBUG_TOOLBAR = False
GRAPHENE = {
    "SCHEMA": "kda.graphql.api.schema",
    "RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST": True,
    "RELAY_CONNECTION_MAX_LIMIT": 100,
    # "MIDDLEWARE": [
    #     "kda.graphql.middleware.OpentracingGrapheneMiddleware",
    #     "kda.graphql.middleware.JWTMiddleware",
    #     "kda.graphql.middleware.app_middleware",
    # ],
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}
# PLAYGROUND_ENABLED = False
# Django GraphQL JWT settings
GRAPHQL_JWT = {
    "JWT_PAYLOAD_HANDLER": "kda.graphql.utils.create_jwt_payload",
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.VerifyToken",
        "graphql_auth.mutations.RefreshToken",
        "graphql_auth.mutations.RevokeToken",
        "graphql_auth.mutations.VerifySecondaryEmail",
    ],
}
if not DEBUG:
    GRAPHQL_JWT["JWT_VERIFY_EXPIRATION"] = True  # type: ignore
    GRAPHQL_JWT["JWT_LONG_RUNNING_REFRESH_TOKEN"] = True  # type: ignore

#     GraphQL Auth registration fields
ALLOW_LOGIN_NOT_VERIFIED = False

REGISTER_MUTATION_FIELDS = ["email", "username", "first_name", "last_name", "phone_number", "date_of_birth"]
UPDATE_MUTATION_FIELDS = ["first_name", "last_name"]
REGISTER_MUTATION_FIELDS_OPTIONAL = ["date_of_birth"]
USER_NODE_FILTER_FIELDS = {
    "email": ["exact", ],
    "username": ["exact", "icontains", "istartswith"],
    "is_active": ["exact"],
    "status__archived": ["exact"],
    "status__verified": ["exact"],
    "status__secondary_email": ["exact"],
}
USER_NODE_EXCLUDE_FIELDS = ["password", "is_superuser"]

ACTIVATION_PATH_ON_EMAIL = "/activate"
PASSWORD_RESET_PATH_ON_EMAIL = "/password-reset"
ACTIVATION_SECONDARY_EMAIL_PATH_ON_EMAIL = "/activate"


# GRAPHQL_JWT = {
#     "JWT_VERIFY_EXPIRATION": True,
#     "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
#     # optional
#     "JWT_ALLOW_ANY_CLASSES": [
#         "graphql_auth.mutations.Register",
#         "graphql_auth.mutations.VerifyAccount",
#         "graphql_auth.mutations.ResendActivationEmail",
#         "graphql_auth.mutations.SendPasswordResetEmail",
#         "graphql_auth.mutations.PasswordReset",
#         "graphql_auth.mutations.ObtainJSONWebToken",
#         "graphql_auth.mutations.VerifyToken",
#         "graphql_auth.mutations.RefreshToken",
#         "graphql_auth.mutations.RevokeToken",
#         "graphql_auth.mutations.VerifySecondaryEmail",
#     ],
# }

DEFAULT_COUNTRY = os.environ.get("DEFAULT_COUNTRY", "KE")
DEFAULT_CURRENCY = os.environ.get("DEFAULT_CURRENCY", "KES")
DEFAULT_DECIMAL_PLACES = get_currency_fraction(DEFAULT_CURRENCY)
DEFAULT_MAX_DIGITS = 12
DEFAULT_CURRENCY_CODE_LENGTH = 3



ASGI_APPLICATION = 'config.routing.application'

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    },
}

# Celery
# ------------------------------------------------------------------------------


if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = (
    os.environ.get("CELERY_BROKER_URL", os.environ.get("CLOUDAMQP_URL")) or ""
)
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", None)
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_TASK_ALWAYS_EAGER = not CELERY_BROKER_URL
# Change this value if your application is running behind a proxy,
# e.g. HTTP_CF_Connecting_IP for Cloudflare or X_FORWARDED_FOR
REAL_IP_ENVIRON = os.environ.get("REAL_IP_ENVIRON", "REMOTE_ADDR")

# The maximum length of a graphql query to log in tracings
OPENTRACING_MAX_QUERY_LENGTH_LOG = 2000

# Slugs for menus precreated in Django migrations
DEFAULT_MENUS = {"top_menu_name": "navbar", "bottom_menu_name": "footer"}

#  Sentry
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN, integrations=[CeleryIntegration(), DjangoIntegration()]
    )

PLAYGROUND_ENABLED = get_bool_from_env("PLAYGROUND_ENABLED", True)
ALLOWED_GRAPHQL_ORIGINS = os.environ.get("ALLOWED_GRAPHQL_ORIGINS", "*")