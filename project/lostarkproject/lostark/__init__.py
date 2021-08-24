from flask import Flask


def create_app():
    app = Flask(__name__)

    # bluePrint
    from .views import auction_views, status_views, main_views
    app.register_blueprint(auction_views.bp)
    app.register_blueprint(status_views.bp)
    app.register_blueprint(main_views.bp)

    return app

