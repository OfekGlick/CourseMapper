from courseMapper import *
from data_scraping import *

if __name__ == '__main__':
    df = build_db()
    G_course = build_graph(df)
    print(what_can_i_take(['234117'], G_course))
