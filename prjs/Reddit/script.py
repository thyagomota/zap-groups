import praw
import credentials as cred
import emoji
import shutil
import directory as dir

def main():
    reddit = praw.Reddit(client_id = cred.my_id,
                         client_secret = cred.my_secret,
                         password = cred.my_password,
                         username = cred.my_username,
                         user_agent = cred.my_agent)
    posts = []

    num = input('Enter the number of posts that you would like. ')
    # Prints the top # of posts in the group WApals
    wa_groups = reddit.subreddit('WApals').hot(limit=int(num))
    for post in wa_groups:
        print(post.title)
        print(give_emoji_free_text(post.selftext))
        posts.append(give_emoji_free_text(post.title))
        posts.append(give_emoji_free_text(post.selftext))

    user_input = input("Would you like a text file or a csv file (txt or csv). ")
    file_type(posts, user_input)
    shutil.move(filename, dir.my_directory)

# Ignores emojis within a string
def give_emoji_free_text(text):
    return emoji.get_emoji_regexp().sub(r'', text)

# Creates a file either txt or csv
def file_type(my_posts, my_input):
    print("The date should be in the form of: mm-dd-yyyy")
    date = input('Choose the date. ')
    filename = 'Reddit_Output_' + date + '.' + my_input
    with open(filename, 'w') as new_file:
        for post in my_posts:
            new_file.write(post)

if __name__ == '__main__':
    main()

# Getting specific comments from that subreddit
#submission = reddit.submission(id="goohym")
#for top_level in submission.comments:
#    print(top_level.body)
