#Project Flask MVC

__author__ = "stormy0611"
__version__ = "1"
__email__ = "devstar0611@gmail.com"

from project import app
from project.utiles.scrape import scraper
import os

# @app.teardown_appcontext
# def cleanup(error):
#     # Perform cleanup tasks here
#     print("sdfsdf")
#     scraper.del_driver()
#     if not scraper.is_driver_quitted():
#         if not scraper.quit_driver_process():
#             scraper.remove_all_chrome_process()

if __name__ == '__main__':
    scraper.create_driver(False, 2)
    scraper.check_lang_location('https://www.google.com/maps')
    app.run(host="localhost", port=8000, debug=True, use_reloader=False)
