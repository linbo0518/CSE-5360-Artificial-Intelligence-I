import sys
import pandas as pd

training_data = sys.argv[1]
df = pd.read_csv(training_data, sep='     ', header=None)

df = df.rename(
    columns={
        0: 'baseball_game_on_TV',
        1: 'watch_TV',
        2: 'out_of_cat_food',
        3: 'feed_the_cat'
    })
# node baseball
num_days = len(df)
num_baseball = df['baseball_game_on_TV'].sum()
P_baseball = num_baseball / num_days
print(f"number of days: {num_days}".ljust(40),
      f"number of baseball: {num_baseball}".ljust(40),
      f"P(baseball): {P_baseball}")
# node out
num_out = df['out_of_cat_food'].sum()
P_out = num_out / num_days
print(f"number of days: {num_days}".ljust(40),
      f"number of out: {num_out}".ljust(40), f"P(out): {P_out}")
# node watch
num_watch_baseball = df[df['baseball_game_on_TV'] == 1]['watch_TV'].sum()
P_watch_baseball = num_watch_baseball / num_baseball
print(f"number of baseball: {num_baseball}".ljust(40),
      f"number of watch baseball: {num_watch_baseball}".ljust(40),
      f"P(watch|baseball):{P_watch_baseball}")
num_not_baseball = len(df[df['baseball_game_on_TV'] == 0])
num_watch_not_baseball = df[df['baseball_game_on_TV'] == 0]['watch_TV'].sum()
P_watch_not_baseball = num_watch_not_baseball / num_not_baseball
print(f"number of not baseball: {num_not_baseball}".ljust(40),
      f"number of watch not baseball: {num_watch_not_baseball}".ljust(40),
      f"P(watch|not baseball):{P_watch_not_baseball}")
# node feed
num_watch = len(df[(df['watch_TV'] == 1) & (df['out_of_cat_food'] == 1)])
num_feed_watch_out = df[(df['watch_TV'] == 1) &
                        (df['out_of_cat_food'] == 1)]['feed_the_cat'].sum()
P_feed_watch_out = num_feed_watch_out / num_watch
print(f"number of watch out: {num_watch}".ljust(40),
      f"number of feed watch out: {num_feed_watch_out}".ljust(40),
      f"P(feed|watch, out): {P_feed_watch_out}")

num_watch_not_out = len(df[(df['watch_TV'] == 1) &
                           (df['out_of_cat_food'] == 0)])
num_feed_watch_not_out = df[(df['watch_TV'] == 1) &
                            (df['out_of_cat_food'] == 0)]['feed_the_cat'].sum()
P_feed_watch_not_out = num_feed_watch_not_out / num_watch_not_out
print(f"number of watch not out: {num_watch_not_out}".ljust(40),
      f"number of feed watch not out: {num_feed_watch_not_out}".ljust(40),
      f"P(feed|watch, not out): {P_feed_watch_not_out}")

num_not_watch_out = len(df[(df['watch_TV'] == 0) &
                           (df['out_of_cat_food'] == 1)])
num_feed_not_watch_out = df[(df['watch_TV'] == 0) &
                            (df['out_of_cat_food'] == 1)]['feed_the_cat'].sum()
P_feed_not_watch_out = num_feed_not_watch_out / num_not_watch_out
print(f"number of not watch out: {num_not_watch_out}".ljust(40),
      f"number of feed not watch out: {num_feed_not_watch_out}".ljust(40),
      f"P(feed|not watch, out): {P_feed_not_watch_out}")

num_not_watch_not_out = len(df[(df['watch_TV'] == 0) &
                               (df['out_of_cat_food'] == 0)])
num_feed_not_watch_not_out = df[
    (df['watch_TV'] == 0) & (df['out_of_cat_food'] == 0)]['feed_the_cat'].sum()
P_feed_not_watch_not_out = num_feed_not_watch_not_out / num_not_watch_not_out
print(
    f"number of not watch not out: {num_not_watch_not_out}".ljust(40),
    f"number of feed not watch not out: {num_feed_not_watch_not_out}".ljust(40),
    f"P(feed|not watch, not out): {P_feed_not_watch_not_out}")
