from django.db import models
import string
import random

""" Let's just quickly discuss what a model actually is. So in a standard database, you would 
have a table. You would have rows and columns in those tables and well, that's how you would 
store information. That's no different in Django, but when we actually go ahead and create
a table, what we're going to be doing is creating a model instead. So what Django allows us 
to do is write Python code, and then it will interpret that Python code and automatically 
perform all of the database operations for us. So essentially it's just a layer of abstraction.
It makes it a lot easier for us as Python developers to write database related stuff. 

We want to have fat models and thin views
"""
# Generating random unique codes
def generate_unique_code(): 
    length = 6 

    while True: 
        # This will generate a random code that is of length k and only contains ascii_uppercase characters
        code = ''.join(random.choices(string.ascii_uppercase), k = length)
        # Filtering all room objects by code and if any code is == to code, and the count of that is 0, we konw have a unique code
        if Room.objects.filter(code=code).count() == 0:
            break

    return code 


# Create your models here.
# This is going to me a model (Inheritance)
class Room(models.Model):
    code = models.CharField(max_length = 8, default="", unique = True)
    host = models.CharField(max_length = 50, unique = True)
    #null = False means we must pass in a value
    guest_can_pause = models.BooleanField(null = False, default = False)
    votes_to_skip = models.IntegerField(null = False, default = 1)
    created_at = models.DateTimeField(auto_now_add = True)
