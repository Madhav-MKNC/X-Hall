# helper functions

# for unique usernames
unique_username = 1
def get_username():
    global unique_username
    unique_username += 1
    return "user{unique_username}"
