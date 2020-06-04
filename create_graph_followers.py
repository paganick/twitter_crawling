import tweepy
import authenticate as auth
import csv
import pandas as pd
from user import User

def main():
    api = auth.authenticate()
    folder = 'complex_network_test3/'
    nodes_filename = folder+'nodes_list.csv'
    graph_filename = folder+'graph_followers.csv'
    indegree_filename = folder+'indegree.csv'
    nodes_data = pd.read_csv(nodes_filename)
    
    name_list = nodes_data['Label'].to_list()
    id_list = nodes_data['id'].to_list()
    
    number_of_nodes = len(name_list)
    print ('Found:', number_of_nodes, 'nodes.')
    edge_list = []
    indegree = [0]*number_of_nodes

    edges_data = pd.DataFrame(columns=['Source', 'Target'])
    indegree_data = pd.DataFrame(columns=['id','Label','indegree'])
    #edges_data = pd.DataFrame(edge_list, columns=['Source', 'Target'])
    edges_data.to_csv(graph_filename, mode='w', index=False)
    
    
    for source in range(number_of_nodes):
        indeg = 0
        edges_data = pd.DataFrame(columns=['Source', 'Target'])
        indegree_data = pd.DataFrame(columns=['id','Label','indegree'])
        node = User(api, name_list[source])
        if (node.error == False):
        #if False:
        #if (node.number_of_friends> number_of_nodes):
        #    for target in range(source+1, len(name_list)):
        #        f = api.show_friendship(source_screen_name = name_list[source], target_screen_name = name_list[target])
                #if (f[0].followed_by==True):
                #    edge_list.append([id_list[target], id_list[source]])
                #    indegree[source]+=1
       #         if (f[0].following==True):
       #             edge_list.append([id_list[target], id_list[source]])
       #             indegree[target]+=1
       #         if (target % 10 == 0):
       #             print(target, 'target nodes checked.')
        #else:
            try:
                for page in tweepy.Cursor(api.followers_ids, screen_name=name_list[source]).pages():
                    followers = []
                    followers.extend(page)
                    for follower_id in followers:
                        if follower_id in id_list:
                            edge_list.append([follower_id, id_list[source]])
                            edge = pd.DataFrame([[follower_id, id_list[source]]], columns=['Source', 'Target'])
                            edges_data = pd.concat([edges_data, edge], ignore_index=True)
                            indegree[source]+=1
            except tweepy.TweepError:
                print ('Error checking followers of node', name_list[source])
        indegree_row = pd.DataFrame([[id_list[source], name_list[source], indegree[source]]])
        indegree_data = pd.concat([indegree_data, indegree_row], ignore_index = True)
        print (source, 'source nodes checked.')
        print (len(edge_list), 'edges found.')
        edges_data.to_csv(graph_filename, mode='a', header=False, index=False)
        indegree_data.to_csv(indegree_filename, mode='a', header=False, index=False)
        edges_data.iloc[0:0]
        indegree_data.iloc[0:0]

    
# Execute `main()` function
if __name__ == '__main__':
    main()
