    import os
    import csv
    import tweepy
    import json
    import pandas as pd
    from dmin import read_data
    from datetime import datetime

    # Set up Twitter API credentials
    consumer_key = "AAA" 
    consumer_secret = "BBB" 
    access_token = "CCC" 
    access_token_secret = "DDD" 


    def authenticate_twitter_app() -> tweepy.API:
        """Authenticate the Tweepy library with Twitter API credentials."""
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.wait_on_rate_limit = True
        api.wait_on_rate_limit_notify = True
        return api


    def search_twitter_profile(api: tweepy.API, query: str) -> dict:
        """
        Search for the best match of a Twitter profile based on the input query.

        Args:
            api (tweepy.API): An authenticated Tweepy API object.
            query (str): The name of the deputy to search for.

        Returns:
            dict: A dictionary containing the best match profile information.
        """
        users = api.search_users(query, count=1)
        if users:
            user_data = users[0]._json
            return user_data
        else:
            return None


    def find_twitter_accounts(_file: str) -> pd.DataFrame:
        """
        Find Twitter accounts for deputies listed in the  file.

        Args:
            _file (str): The path to the  file containing the deputy names.

        Returns:
            pd.DataFrame: A DataFrame containing the information of the found Twitter accounts.
        """
        api = authenticate_twitter_app()

        # Read the  file into a pandas DataFrame
        data = read_data(_file)

        # Create a new DataFrame to store the results
        results = pd.DataFrame(columns=['deputy_name', 'screen_name', 'description',
                            'location', 'friends_count', 'followers_count', 'statuses_count', 'url'])

        # Iterate over the rows of the DataFrame
        for index, row in data.iterrows():
            # Access the data in each column by the column name
            deputy_name = row['nm_urna_candidato']

            best_match = search_twitter_profile(api, deputy_name)

            # Initialize the result dictionary with deputy_name
            result = {'deputy_name': deputy_name}

            if best_match:
                # print(json.dumps(best_match, indent=2))

                # Add the relevant data to the result dictionary
                result.update({
                    'screen_name': best_match['screen_name'],
                    'description': best_match['description'],
                    'location': best_match['location'],
                    'friends_count': best_match['friends_count'],
                    'followers_count': best_match['followers_count'],
                    'statuses_count': best_match['statuses_count'],
                    'url': best_match['url']
                })

                # Append the result dictionary to the results DataFrame
                results = results.append(result, ignore_index=True)

            else:
                print(f"No profile found for {deputy_name}.")

        results.to_csv('data/sp_profiles.csv', index=False)
        return results


    def count_status():
        df = pd.read_csv('data/2018/sp_profiles.csv')
        print(df['statuses_count'])
        total_statuses = df['statuses_count'].sum()
        print(total_statuses)


    def store_tweet(row, tweet):
        with open('data/2018/sp_tweets.csv', mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow([
                row['deputy_name'],
                tweet['content'].replace('\n', ' '),
                tweet['url'],
                tweet['date']
            ])


    def get_tweets_since(api, screen_name, since_date, row):
        tweets = []
        since_datetime = datetime.strptime(since_date, '%Y-%m-%d')
        for status in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended').items():
            status_created_at_naive = status.created_at.replace(tzinfo=None)
            if since_datetime <= status_created_at_naive:
                print(status.id)
                tweet = {
                    'author': screen_name,
                    'content': status.full_text,
                    'url': f"https://twitter.com/{screen_name}/status/{status.id}",
                    'date': status_created_at_naive
                }
                store_tweet(row, tweet)
                tweets.append(tweet)
            elif status_created_at_naive < since_datetime:
                break
        return tweets

    def store_tweets(api):
        csv_file = 'data/2018/sp_profiles.csv'
        data = pd.read_csv(csv_file)

        output_file = 'data/2018/sp_tweets.csv'

        # Check if the output file does not exist, then create the header
        if not os.path.exists(output_file):
            with open(output_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(['deputy_name', 'content', 'url', 'date'])

        # Iterate over the rows of the DataFrame starting from row number 11
        start_row = 5
        for index in range(start_row, len(data)):
            row = data.iloc[index]
            deputy_name = row['deputy_name']
            screen_name = row['screen_name']
            since_date = '2019-02-01'
            get_tweets_since(api, screen_name, since_date, row)


    def main():
        api = authenticate_twitter_app()
        # find_twitter_accounts("data/sp_voting_type.csv")
        # count_status()
        store_tweets(api)


    if __name__ == "__main__":
        main()
