from courseMapper import *
from data_scraping import *

if __name__ == '__main__':
    # df = build_db()
    import pandas as pd
    df = pd.read_csv("CourseData.csv")
    G_course = build_graph(df)
    print(what_can_i_take(['234117', '094345', '104031', '104166'], G_course))
