from app.app import create_app
from app.settings import DevConfig, ProdConfig, os

CONFIG = DevConfig if os.environ.get('FLASK_DEBUG') == '1' else ProdConfig

app = create_app(config_object=CONFIG)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=True)
