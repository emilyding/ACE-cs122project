#generate graph
import matplotlib.pyplot as plt
import yelp_sql
example_query = {"city": "chicago"}

def gen_query_piechart(city):
    query = {"city" : city}
    return query

def gen_piechart(query):
    '''
    price_rate = yelp_sql.price_ratings(query)
    labels = ['$', '$$', '$$$', '$$$$']
    sizes = [price_rate['$'][1], price_rate['$$'][1], price_rate['$$$'][1], price_rate['$$$$'][1]]
    print(sizes)
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=0)
    plt.axis('equal')
    plt.show()
    '''
    price_rate = yelp_sql.price_ratings(query)
    prices = ["$", "$$", "$$$", "$$$$"]
    sizes = []
    labels = []
    for dollar_signs in prices:
        sizes.append(price_rate[dollar_signs][1])
    for i in  range(len(sizes)):
        labels.append((i+1)*"\$")
    print(labels)
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
 
    # Plot
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=0)
 
    plt.axis('equal')
    plt.show()