#Better Reddit Search

##Forward
Better Reddit Search was a final project for my data mining class. Due to time constraints much of the code is currently lacking in elegance as well as performance. I hope to rectify this in the coming months. Below is the original paper I submitted for the class. It is subject to change as I go back through, clean up the code, make performance improvements, and add more features.

##Introduction
The goal of Improved Reddit Search was to design an IR system that could produce more relevant results than the system Reddit already has in place. Reddit is a social news website where users can post links and other users can comment and vote on these submissions. Reddit is divided into sections called “subreddits,” each dedicated to different subjects such as r/technology, r/gaming, or r/pics.

Reddit’s current search implementation only searches for exact query matches in post titles. For example, if a post is named “Google unveils new hi-tech glasses,” it will match the query “Google,” but not the query “Google Glass.” Due to these restrictions, Reddit search is widely considered to be absolutely useless.

For the purposes of this implementation, we have chosen to use the technology subreddit. r/technology receives a reasonable amount of posts per day, allowing it to be easily indexed, as well as a relatively high quality community, making it an ideal place to test our search implementation.
##Analytical Question

We believe that Reddit’s search implementation could be vastly improved by removing the exact query matching restrictions as well as taking comments into account during the indexing process.

Since a post’s title is a very small document, with a very limited set of keywords, we theorize that by looking into the comments, we can get a better idea what the post is actually about and make it appear under a more diverse set of keywords. Returning to the “Google Glass” query example above, it is likely that in the comments of a post titled “Google unveils new hi-tech glasses,” someone will refer to Google Glass by name. By looking into the comments, we can take this into account, and make this result rank more highly in the search results.

By loosening title matching restrictions, as well as incorporating comments, the goal of Better Reddit Search is to sacrifice some amount of precision for greater gains to recall.

##Analytical Methods

The primary analytical methods used were a modified version of TF-IDF keyword weighting, cosine similarity, and Wilson score. To get a better understanding of how each of these methods were used, we will take a step-by-step look at how posts were indexed and retrieved.

The indexing program takes post comments and titles, performs tokenization, stopword removal, and stemming on them, and then builds and inserts a frequency distribution into the database.

![Database diagram](https://docs.google.com/drawings/image?id=s62mp2KXf3MZRtVznCq3Hbg&w=617&h=366&rev=1&ac=1)

Figure 1: Database diagram

Notice that the original text of the comments is not preserved, this is because comments are handled in a special way and their content does not need to be returned on a search.

Reddit uses Wilson score in order to rank their comments. This measure allows them to predict the quality of a comment with only a limited number of upvotes and downvotes. When we ask the Reddit API for comments on a post, we ask for them to be sorted in this order, and take only, at most, the best 25 top level comments. It is much more difficult to determine comment quality on comment replies. This is because comments are often “hijacked” by other users to make an irrelevant point in hopes that their comment is more likely to be seen. To avoid this, we chose to look exclusively at the top level comments.

When a post’s comments are indexed, we store them as a single document to improve query performance, but we also wanted to give higher quality comments a larger weight. In order to do this, we calculate every comment’s Wilson score and added it to the word’s term frequency. This means that a given word in a comment has a term frequency of tf * (1 + Wilson score).
When a query is made, we initially filter our results by ensuring similarity calculations are only run on documents containing one or more of the query terms. We then do two separate similarity calculations for each post, one for the title and one for the comments. This allows us to apply a modifier to the post title similarity to ensure title matches are weighted more heavily than comment matches.

The final similarities are then multiplied by the Wilson score of the post itself, sorted, and returned to the user.
##Results

Once Better Reddit Search was posted for public access, each search was tracked and users were instructed to mark items as either relevant or irrelevant. Our average precision came out to be 75.6% vs. Reddit’s 95.9%, but we also returned 37.3% more relevant posts. We also noticed that our most relevant results we often not at the top of our results, but unfortunately, we did not officially track the position of results we received feedback on, so this is simply an observation.
##Conclusions

Based on the data we believe that Better Reddit Search is a great start on improving Reddit search, but is far from complete. Feedback we received says that our increase in recall did not entirely make up for our sacrifice in precision. Moving forward, weightings could be tweaked to improve ranking order, as well as higher thresholds placed on comment term frequencies, which seemed to be the largest contributing factor to our precision decrease.