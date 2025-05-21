import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# to read csv file
df = pd.read_csv("data.csv") 

# to specify features
features = ['price', 'area', 'room_count', 'year']  
X = df[features].values

# to normalization 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


model = NearestNeighbors(n_neighbors=10, metric='euclidean') 
model.fit(X_scaled)


target_id = int(input())
if target_id in df['id'].values:
    target_index = df.index[df['id'] == target_id][0]
    target_vector_scaled = X_scaled[target_index].reshape(1, -1)


    distances, indices = model.kneighbors(target_vector_scaled)
    

    similar_indices = [idx for idx in indices[0] if idx != target_index][:10]


    similar_links = [f"https://example.com/house/{int(df.loc[idx, 'id'])}" for idx in similar_indices]


    print("target house =", target_id)
    for link in similar_links:
        print(link)

else:
    print(f"There is no house like {target_id}.")
