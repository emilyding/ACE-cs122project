
def hash_(args):
    city = args["city"]
    sum_ = []
    for letter in city:
        sum_.append(ord(letter))
    return (city, sum_)