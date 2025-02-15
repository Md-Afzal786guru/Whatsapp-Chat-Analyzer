from pandas.core.arrays import period
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor: URLExtract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Ensure there is data to analyze
    if df.empty:
        return 0, 0, 0, 0  # Return zeros if no messages

    num_messages = df.shape[0]
    words = df['message'].apply(lambda x: len(x.split())).sum()
    
    # Count media messages (e.g., messages containing 'Media omitted')
    num_media_messages = df[df['message'].str.contains('Media omitted', case=False, na=False)].shape[0]
    
    # Count messages containing URLs
    num_links = df[df['message'].str.contains(r'http', na=False)].shape[0]

    return num_messages, words, num_media_messages, num_links




def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'Name', 'count': 'Percent'})
    return x, df


def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_list(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emoji_list = []

    for message in df['message']:
        emoji_list.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))))

    return emoji_df


def monthly_timeline(selected_user, df):
    df['month_num'] = df['date'].dt.month
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['Day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['Month'].value_counts()


def activity_heatmap(selected_user, df):
    df['peroid'] = period
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


def most_active_hours(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Correct the column name from 'hour' to 'Hour'
    active_hours = df.groupby('Hour').size()

    return active_hours


