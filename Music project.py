#Получение данных

import pandas as pd
df = pd.read_csv('/datasets/music_project.csv')
df.head(10)
df.info()

#Предобработка данных

df.columns
df.set_axis(['user_id', 'track_name', 'artist_name', 'genre_name', 'city', 'time', 'weekday'], axis = 'columns', inplace = True)
list(df)
df.isnull().sum()
df['track_name'] = df['track_name'].fillna('unknown')
df['artist_name'] = df['artist_name'].fillna('unknown')
df.isnull().sum()
df.dropna(subset = ['genre_name'], inplace = True)
df.isnull().sum()
df.duplicated().sum()
df=df.drop_duplicates().reset_index(drop=True)
df.duplicated().sum()
genres_list = df['genre_name'].unique()

def find_genre(genre):
    k = 0
    for i in genres_list:
        if i == genre:
            k += 1
    return k

find_genre('hip')

find_genre('hop')

find_genre('hip-hop')

def find_hip_hop(df, incorrect):
    df['genre_name'] = df['genre_name'].replace(incorrect, 'hiphop')
    total = df.loc[df.loc[:,'genre_name'] == 'wrong']['genre_name'].count()
    return total

find_hip_hop(df, 'hip')
df.info()


#Проверка гипотезы:  в Москве и Санкт-Петербурге пользователи слушают музыку по-разному

df.groupby('city')['genre_name'].count()
df.groupby('weekday')['genre_name'].count()

def number_tracks(df, day, city):
    track_list=df[(df['weekday']==day) & (df['city']==city)]
    track_list_count = track_list['genre_name'].count()
    return track_list_count

number_tracks(df, 'Monday', 'Moscow')
number_tracks(df, 'Monday', 'Saint-Petersburg')

number_tracks(df, 'Wednesday', 'Moscow')
number_tracks(df, 'Wednesday', 'Saint-Petersburg')

number_tracks(df, 'Friday', 'Moscow')
number_tracks(df, 'Friday', 'Saint-Petersburg')

# <таблица с полученными данными>
data = [['Moscow', 15347, 10865, 15680],
       ['Saint-Petersburg', 5519, 6913, 5802]]
columns = ['city','monday','wednesday','friday']
table = pd.DataFrame(data = data, columns = columns)
table

# Какие жанры преобладают в разных городах в понедельник утром и в пятницу вечером

moscow_general = df[df['city'] == 'Moscow']
spb_general = df[df['city'] == 'Saint-Petersburg']


def genre_weekday(df, day, time1, time2):
    genre_list = df[(df['weekday'] == day) & (df['time'] > time1) & (df['time'] < time2)]
    genre_list_sorted = genre_list.groupby('genre_name')['genre_name'].count().sort_values(ascending = False).head(10)
    return genre_list_sorted

genre_weekday(moscow_general, 'Monday', '07:00:00', '11:00:00')
genre_weekday(spb_general, 'Monday', '07:00:00', '11:00:00')
genre_weekday(moscow_general, 'Friday', '17:00:00', '23:00:00')
genre_weekday(spb_general, 'Friday', '17:00:00', '23:00:00')

moscow_genres = moscow_general.groupby('genre_name')['genre_name'].count().sort_values(ascending = False)
moscow_genres.head(10)

spb_genres=spb_general.groupby('genre_name')['genre_name'].count().sort_values(ascending=False)
spb_genres.head(10)
