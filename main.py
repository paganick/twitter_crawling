import authenticate as auth
import csv
from user import User
import pandas as pd

class Data:
    
    def __init__(self):
        #self.seed_nodes = ['NicoloPagan']
        self.seed_nodes = []
        self.name_list = []
        self.NO_name_list = []
        self.keywords = ['social networks', 'complex networks', 'complex systems', 'network science']
        self.folder = 'complex_network_test/'
        self.tweets_filename = self.folder+'tweets_list.csv'
        self.nodes_filename = self.folder+'nodes_list.csv'
        self.all_nodes_filename = self.folder+'all_nodes_list.csv'
        self.edges_filename = self.folder+'edges_list.csv'
        self.n_nodes = 0
        self.n_edges = 0
    
    def prepare_files(self):
        tweets_data = pd.DataFrame(columns=['id', 'tweet_id', 'author', 'text'])
        tweets_data.to_csv(self.tweets_filename, mode='w', index=False)
        
        self.node_header_row = ['id', 'Label', 'description']
        for keyword in self.keywords:
            self.node_header_row.append(keyword)
        self.node_header_row.append('tot_count')
        self.node_header_row.append('number_of_tweets')
        nodes_data = pd.DataFrame(columns=self.node_header_row)
        nodes_data.to_csv(self.nodes_filename, mode='w', index=False)
        all_nodes_data = pd.DataFrame(columns=self.node_header_row)
        all_nodes_data.to_csv(self.all_nodes_filename, mode='w', index=False)

        edges_data = pd.DataFrame(columns=['Source', 'Target'])
        edges_data.to_csv(self.edges_filename, mode='w', index=False)
        
    
    def read_data(self):
        print('Reading old data:')
        tweets_data = pd.read_csv(self.tweets_filename)
        
        nodes_data = pd.read_csv(self.nodes_filename)
        self.node_header_row = list(nodes_data.columns.values)
        self.keywords = self.node_header_row[3:-2]
        self.name_list = nodes_data['Label'].to_list()
        
        edges_data = pd.read_csv(self.edges_filename)
        self.n_edges = len(edges_data.index)
        if edges_data.shape[0]>0:
            last_node_id = edges_data.iloc[-1]['Target']
            index = nodes_data.index[nodes_data['id'] == last_node_id].tolist()
            self.n_nodes = index[0]+1
       
        all_nodes_data = pd.read_csv(self.all_nodes_filename)
        self.NO_name_list = all_nodes_data['Label'].to_list()
        for name in self.name_list:
            self.NO_name_list.remove(name)
        
# Define `main()` function
def main():
    api = auth.authenticate()
    data = Data()
    
    if len(data.seed_nodes)>0:
        data.prepare_files()
        for name in data.seed_nodes:
            node = User(api, name)
            if (node.error == False):
                if node.analyze(api, data.keywords, data.node_header_row, data.all_nodes_filename) == True:
                    node.write_node(data.node_header_row, data.nodes_filename)
                    node.write_tweets(data.tweets_filename)
                    data.name_list.append(name)
        
    else:
        data.read_data()
        print('Total number of interesting nodes found:', len(data.name_list))
        print('Interesting nodes found:')
        print (data.name_list)
        print('*************************************')
        print('Not Interesting nodes found:')
        print (data.NO_name_list)
        print('Total number of analyzed nodes:', len(data.name_list)+len(data.NO_name_list))
        print('Number of edges:', data.n_edges)
    
    
    for name in data.name_list[data.n_nodes:]:
        node = User(api, name)
        data.n_nodes+=1
        if (node.error == False):
            print('*****************')
            print('Processing node number ', data.n_nodes, ':', node.screen_name)
            #if node.analyze(api, data.keywords, data.node_header_row, data.all_nodes_filename) == True:
            node.process_followers(api, data.keywords, data.node_header_row, data.name_list, data.NO_name_list, data.nodes_filename, data.all_nodes_filename, data.tweets_filename)
            for name in node.interesting_followers_list:
                data.name_list.append(name)
            for name in node.not_interesting_followers_list:
                data.NO_name_list.append(name)
            node.process_friends(api, data.keywords, data.node_header_row, data.name_list, data.NO_name_list, data.nodes_filename, data.all_nodes_filename, data.tweets_filename)
            for name in node.interesting_friends_list:
                data.name_list.append(name)
            for name in node.not_interesting_friends_list:
                data.NO_name_list.append(name)
            node.write_edges(data.edges_filename)
            data.n_edges+= node.get_number_edges()
            print('Total number of interesting nodes found:', len(data.name_list))
            print('Total number of analyzed nodes:', len(data.name_list)+len(data.NO_name_list))
            print('Number of edges:', data.n_edges)
            if len(data.name_list)> 10000:
                break
                
# Execute `main()` function
if __name__ == '__main__':
    main()
