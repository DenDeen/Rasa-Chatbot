from py2neo import Graph,Node,Relationship
import pandas as pd
graph = Graph("http://localhost:7474",auth=("neo4j","12345"))
graph.delete_all()

restaurant_data = pd.read_csv("/home/noman/Documents/restaurant_graph_data.csv") 
hotel_data = pd.read_csv("/home/noman/Documents/hotel_graph_data.csv")

print(restaurant_data)
print(hotel_data)

# create Restaurant graph
for index, row in restaurant_data.iterrows():
    restaurant_node = {}
    
    Name = row["'name'"]
    Cuisine = row["'cuisine'"]
    Outside_seating = row["'outside-seating'"]
    Price_range = row["'price-range'"]
    
    restaurant_node = Node("Restaurant", id=index ,name=Name, cuisine=Cuisine, outside_seating=Outside_seating,
               price_range=Price_range)
    
    graph.create(restaurant_node)
    
# create Hotel graph    
for index, row in hotel_data.iterrows():
    hotel_node = {}
    
    Name = row["'name'"]
    Price_range = row["'price-range'"]
    Breakfast_included = row["'breakfast-included'"]
    City = row["'city'"]
    Free_wifi = row["'free-wifi'"]
    Rating = row["'star-rating'"]
    Swimming_pool = row["'swimming-pool'"]
    
    hotel_node = Node("Hotel", id=index ,name=Name, price_range=Price_range, 
                      breakfast_included=Breakfast_included,
                      city=City, free_wifi=Free_wifi, rating=Rating, swimming_pool=Swimming_pool)
    
    graph.create(hotel_node)    

print(graph.run("MATCH (r:Restaurant) RETURN r.name"))
print(graph.run("MATCH (r:Hotel) RETURN r.name"))