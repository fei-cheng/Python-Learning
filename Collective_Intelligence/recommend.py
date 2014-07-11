# A dictionary of movie critics and their ratings of a small set of movies
critics = {
    'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5}, 
    'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0}, 
    'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
    'Toby': {'Snakes on a Plane':4.5, 'You, Me and Dupree':1.0, 'Superman Returns':4.0}
    }

from math import sqrt

def tansformDict(critics):
    transformed_dict = {}
    for person in critics:
        for item in critics[person]:
            transformed_dict.setdefault(item, {})
            transformed_dict[item][person] = critics[person][item]
    return transformed_dict

def sim_distance(prefs, person1, person2):
    """
        Returns a distance-based similarity score for person1 and person2.
    """
    for person in [person1, person2]:
        if person not in prefs:
            print 'Does not exist information of ', person
            raise
    sum_of_squares = 0
    for item in prefs[person1]: 
        if item in prefs[person2]:
            sum_of_squares += (prefs[person1][item] - prefs[person2][item]) ** 2
  # if they have no ratings in common, return 0
    if sum_of_squares == 0:
        return 0
    return 1 / (1 + sqrt(sum_of_squares))

def sim_pearson(prefs, p1, p2):
    """
        Returns the Pearson correlation coefficient for p1 and p2.
        See: http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
    """
    for person in [p1, p2]:
        if person not in prefs:
            print 'Does not exist information of ', person
            raise
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]: 
        if item in prefs[p2]:
            si[item] = 1
            
    # if they are no ratings in common, return 0
    if len(si) == 0:
        return 0
        
    # Sum calculations
    n = len(si)
  
    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
  
    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
  
    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
  
    # Calculate r (Pearson score)
    num = n * pSum - sum1 * sum2
    den = sqrt( (n * sum1Sq - pow(sum1, 2)) * (n * sum2Sq - pow(sum2, 2)) )
    if den == 0:
        return 0
    return num / den
    
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    """
        Returns the top n who have the most similar rating to a specified person.
    """
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    
    scores.sort()
    scores.reverse()
    return scores[:n]
    
def getRecommendations(prefs, person, similarity=sim_pearson):
    """
        Returns the items calculated from weighted sum of others' ratings.
    """
    simSum = {}
    scoreSum = {}
    
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue    # ignore those who have non-positive similarity
        
        for item in prefs[other]:
            if (item not in prefs[person]) or (prefs[person][item] == 0):
                simSum.setdefault(item, 0)
                scoreSum.setdefault(item, 0)
                simSum[item] += sim
                scoreSum[item] += prefs[other][item] * sim
                
    rankings = [(scoreSum[item]/simSum[item], item) for item in simSum]
    
    rankings.sort()
    rankings.reverse()
    return rankings
    
def calculateSimilarItems(itemPrefs, n=10, similarity=sim_distance):
    """
        Here, itemPrefs = tansformDict(prefs).
    """
    result = {}
    for item in itemPrefs:
        scores = topMatches(itemPrefs, item, n, similarity)
        result[item] = scores
    return result

def getRecommendedItems(prefs, itemMatch, user):
    totalSim = {}
    totalScore = {}
    userRatings = prefs[user]
    
    for (item, rating) in userRatings.items():
        for (similarity, sim_item) in itemMatch[item]:
            if sim_item in userRatings:
                continue
                
            totalSim.setdefault(sim_item, 0)
            totalSim[sim_item] += similarity
            
            totalScore.setdefault(sim_item, 0)
            totalScore[sim_item] += similarity * rating
            
    rankings = [(score/totalSim[item], item) for (item, score) in totalScore.items()]
    
    rankings.sort()
    rankings.reverse()
    return rankings

if __name__ == '__main__':
    print getRecommendedItems(critics, calculateSimilarItems(tansformDict(critics)), 'Toby')
