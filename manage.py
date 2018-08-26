from app.app import create_app
from app.settings import DevConfig, ProdConfig, os


def start_server():
    config = DevConfig if os.environ.get('FLASK_DEBUG') == '1' else ProdConfig
    app = create_app(config_object=config, name='server')
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)


if __name__ == '__main__':
    start_server()
