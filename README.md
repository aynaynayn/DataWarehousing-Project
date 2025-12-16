LIBRARIES NEEDED TO INSTALL:

praw (Python Reddit API Wrapper)
textblob
pandas
rapidfuzz
tqdm

paste on command prompt, make sure to have python set up
pip install praw textblob pandas rapidfuzz tqdm

* praw: For accessing Reddit posts and comments via Reddit API
* textblob: For sentiment analysis
* pandas: For data manipulation and CSV export
* rapidfuzz: For fuzzy string matching (book title verification)
* tqdm: For progress bars during processing


Python Version used: 3.11
RAN FROM COMMAND PROMPT


HOW TO SET UP PRAW:
(although fetch_reddit_data.py already has credentials)

1. go to https://www.reddit.com/prefs/apps
2. Scroll down to Developed Applications
3. Click Create App 
4. Fill in the form
	App type: script
	Redirect URL: http://localhost:8080
5. Create App
6. Use credentials (client_id, client_secret, user_agent)

  reddit = praw.Reddit(
    client_id="your_client_id",
    client_secret="your_client_secret",
    user_agent="your_user_agent"
  )



Running from command prompt:
(py files can be run anywhere, however this project 
was run on command prompt)

1. Navigate to project folder: reddit_project
	cd reddit_project

2. Running python files: 
	py <filename.py>
		or
	python <filename.py>

	py fetch_reddit_posts.py
		or
	python fetch_reddit_posts.py



RUNNING THE Python FILES

1. Fetching reddit r/booksuggestions posts:
run in cmd:
	py fetch_reddit_posts.py
-needs praw credentials to work
-IF EMPTY RESULTS THEN IT MEANS RATE LIMIT OR INCORRECT SUBREDDIT/QUERY
-needs textblob for sentiment analysis
-output file name: reddit_booksuggestions_non_relational.json



2. Data Cleaning reddit_booksuggestions_non_relational.json
run in cmd:
	py clean_reddit_data.py

-needs reddit_booksuggestions_non_relational.json to work
-output file name: reddit_booksuggestions_cleaned.json



3. Extracting and verifying book titles from reddit_booksuggestions_cleaned.json
run in cmd:
	py extractandverify.py

-takes around 1-4 hours
-uses the books.csv (local reference) dataset file to verify books
-Expected inputs are reddit_booksuggestions_cleaned.json & books.csv
-output file name: verified_books_offline.csv & verified_books_offline.json

This project contains the source codes, outputs of each source, documentation in pdf and word format, and the diagrams from Power BI. 
