import tweepy
import csv
import numpy as np
import pandas as pd

class User:
    """
    Requires:
    api
    screen_name
    """
   
      
    def __init__(self, api, screen_name):
        self.error = True
        trials = 0
        max_trials = 10
        while (self.error == True and trials<max_trials):
            trials+=1
            try:
                self.user = api.get_user(screen_name)
                self.screen_name = self.user.screen_name
                self.id = self.user.id
                self.description = self.user.description
                self.number_of_followers = self.user.followers_count
                self.number_of_friends   = self.user.friends_count
                self.real_number_of_followers = 0
                self.real_number_of_friends   = 0
                self.number_of_tweets         = 0
                self.keywords_tot_count       = 0
                self.max_n_tweets             = 300
                self.tweet_list               = []
                self.interesting              = False
                self.error = False
            except tweepy.TweepError:
                  self.error = True
        if (trials>=max_trials):
            print('Cannot access information of user id:', screen_name)
        
    def check_keywords(self, text, keywords):
        i = 0
        interesting = False
        for keyword in keywords:
            if text.find(keyword)!=-1:
                self.keywords_count[i]+=1
                interesting = True
            i+=1
        return interesting

    def process_description(self, api, keywords):
        text = str(self.description.encode('ascii','ignore'))
        self.check_keywords(text, keywords)
        
    def process_tweets(self, api, keywords):
        self.tweets_list = []
        self.number_of_tweets = 0
        try:
            for tweet in (tweepy.Cursor(api.user_timeline,id=self.id).items(self.max_n_tweets)):
                self.number_of_tweets+=1
                text = str(tweet.text.encode('ascii', 'ignore'))
                if (self.check_keywords(text, keywords) == True):
                    self.tweet_list.append(tweet)
        except tweepy.TweepError:
            error = True
            #print('Account is protected.')

    def analyze(self, api, keywords, header_row, all_nodes_filename):
        #print('Analyzing: ', self.screen_name)
        if self.interesting == True:
            return True
        else:
            self.compute_keywords_tot_count(api, keywords, header_row, all_nodes_filename)
            if (self.keywords_tot_count >0):
                self.interesting = True
                return True
            else:
                return False
    
    def compute_keywords_tot_count(self, api, keywords, header_row, all_nodes_filename):
        self.keywords_tot_count = 0
        self.keywords_count = np.zeros((len(keywords),), dtype=int)
        self.process_description(api, keywords)
        self.process_tweets(api, keywords)
        for i in self.keywords_count:
            self.keywords_tot_count+= i
        self.write_node(header_row, all_nodes_filename)
    
    def get_tweets(self):
        return self.tweet_list
        
    def write_tweets(self, filename):
        self.tweets_df = pd.DataFrame(columns=['id', 'author', 'text'])
        for tweet in self.tweet_list:
            new_tweet = pd.DataFrame([[tweet.id, self.screen_name, tweet.text.encode('ascii', 'ignore')]], columns=['id', 'author', 'text'])
            self.tweets_df = pd.concat([self.tweets_df, new_tweet], ignore_index=True)
        self.tweets_df.to_csv(filename, mode='a', header=False, index=False)
            
    def write_node(self, header_row, filename):
        row = [self.id, self.screen_name, self.description]
        for i in self.keywords_count:
            row.append(i)
        row.append(self.keywords_tot_count)
        row.append(self.number_of_tweets)
        node_df = pd.DataFrame([row], columns=header_row)
        node_df.to_csv(filename, mode='a', header=False, index=False)
        
    
    def process_friends(self, api, keywords, header_row, name_list, NO_name_list, nodes_filename, all_nodes_filename, tweets_filename):
        self.interesting_friends_list = []
        self.not_interesting_friends_list = []
        self.friends_edge_list = []
        print('Processing friends:', self.number_of_friends)
        friends_count = 0
        for page in (tweepy.Cursor(api.friends_ids, screen_name=self.screen_name)).pages():
            friends = []
            friends.extend(page)
            for friend_id in friends:
                friend = User(api, friend_id)
                friends_count+=1
                if (friend.error == False):
                    friend_name = friend.screen_name
                    if friend_name not in NO_name_list:
                        if friend_name not in name_list:
                            if friend.analyze(api, keywords, header_row, all_nodes_filename) == True:
                                self.interesting_friends_list.append(friend_name)
                                self.friends_edge_list.append([self.id, friend.id])
                                friend.write_node(header_row, nodes_filename)
                                friend.write_tweets(tweets_filename)
                                print('New interesting friend found:', friend_name)
                                print('Friends checked:', friends_count, 'out of', self.number_of_friends)
                            else:
                                self.not_interesting_friends_list.append(friend_name)
                        else:
                            self.friends_edge_list.append([self.id, friend.id])
                            print('Old interesting friend found:', friend_name)
                            print('Friends checked:', friends_count, 'out of', self.number_of_friends)

                        
    def process_followers(self, api, keywords, header_row, name_list, NO_name_list, nodes_filename, all_nodes_filename, tweets_filename):
        self.interesting_followers_list = []
        self.not_interesting_followers_list = []
        self.followers_edge_list = []
        print('Processing followers:', self.number_of_followers)
        followers_count = 0
        for page in (tweepy.Cursor(api.followers_ids, screen_name=self.screen_name)).pages():
            followers = []
            followers.extend(page)
            for follower_id in followers:
                follower = User(api, follower_id)
                followers_count+=1
                if (follower.error == False):
                    follower_name = follower.screen_name
                    if follower_name not in NO_name_list:
                        if follower_name not in name_list:
                            if follower.analyze(api, keywords, header_row, all_nodes_filename) == True:
                                self.interesting_followers_list.append(follower_name)
                                self.followers_edge_list.append([follower.id, self.id])
                                follower.write_node(header_row, nodes_filename)
                                follower.write_tweets(tweets_filename)
                                print('New interesting follower found:', follower_name)
                                print('Followers checked:', followers_count, 'out of', self.number_of_followers)
                            else:
                                self.not_interesting_followers_list.append(follower_name)
                        else:
                            self.followers_edge_list.append([follower.id, self.id])
                            print('Old interesting follower found:', follower_name)
                            print('Followers checked:', followers_count, 'out of', self.number_of_followers)

                
    def write_edges(self, filename):
        self.edges_df = pd.DataFrame(columns=['Source', 'Target'])
        for edge in self.friends_edge_list:
            new_edge = pd.DataFrame([edge], columns=['Source', 'Target'])
            self.edges_df = pd.concat([self.edges_df, new_edge], ignore_index=True)
        for edge in self.followers_edge_list:
          new_edge = pd.DataFrame([edge], columns=['Source', 'Target'])
          self.edges_df = pd.concat([self.edges_df, new_edge], ignore_index=True)
        self.edges_df.to_csv(filename, mode='a', header=False, index=False)
        
    def get_number_edges(self):
        return len(self.followers_edge_list)+len(self.friends_edge_list)
        
