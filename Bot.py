import random

# All the bot functions
def alice(a, b = None): 
    return "I think {} sounds awesome!".format(a + "ing") 

def bob(a, b = None): 
    if b is None: 
        return "Not sure about {}. Don't I get a choice?".format(a + "ing") 
    return "Sure, both {} and {} seems ok to me".format(a, b + "ing") 

def dora(a, b = None): 
    alternatives = ["coding", "singing", "sleeping", "fighting"] 
    b = random.choice(alternatives) 
    res = f"Yea, {a}ing is an option. Or we could do some {b}." 
    return res 

def chuck(a, b = None): 
    action = a + "ing" 
    bad_things = ["fighting", "bickering", "yelling", "complaining"] 
    good_things = ["singing", "hugging", "playing", "working", "eating", "crying", "sleeping", "coding"] 
 
    if action in bad_things: 
        return "YESS! Time for {}".format(action) 
    elif action in good_things: 
        return "What? {} sucks. Not doing that.".format(action) 
    return "I don't care!"


def user(a, b = None):                                                                                      # User function that allows user to communicate with the bots
    return input("What is your response?: ")