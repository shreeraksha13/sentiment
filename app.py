
import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
from datetime import datetime, timedelta, date, time
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns




accessToken = "1329099166715236353-IEfFmwEi2d6FXoxTvs5eBE3eN9qUqB"
accessTokenSecret = "WlahjHrZJ4JBTJGO2ve0CeH6y4ypEdWGVzouyailZMnYQ"
consumerKey = "SPHz5LTAdlydvGk3wW4GcfoLm"
consumerSecret = "u69QUVkLG9rvCH2SDoTFBCw8rVxJCQf31Yxk5vU0dkRE3jbBTj"

#Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
    
# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret) 
    
# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)















#plt.style.use('fivethirtyeight')










def app():
	page_bg_img = '''
	<style>
	.reportview-container {
	background: #D6EAF8;
  	background-size: 1800px 800px;
	background-repeat: no-repeat;
	color: #21618C;	
	font-weight: bold;
	font-family: Trebuchet MS;
	font-size: 150%;
	flex-direction: row-reverse;

	}
	header > .toolbar {
      	flex-direction: row-reverse;
      	left: 1rem;
      	right: auto;
   	 }

    	.sidebar .sidebar-collapse-control,
    	.sidebar.--collapsed .sidebar-collapse-control {
      	left: auto;
      	right: 0.5rem;
   	 }
	.sidebar .sidebar-content {
		background-image: linear-gradient(black,black);
    		color: black;
        	background: #F2D7D5;
		transition: margin-right .3s, box-shadow .3s
	
    	}
	.sidebar.--collapsed .sidebar-content {
      	margin-left: auto;
      	margin-right: -21rem;
    	}
	.Widget>label {
    	color: #34495E;
    	font-family: Trebuchet MS;
	font-size: 16.5px;
	}
	[class^="st-b"]{
    	color: black;
    	font-family: monospace;
	}
	.st-bb {
    	background-color: #EBF5FB;
	}
	.st-at {
    	background-color: #EBF5FB;
	}
	footer {
    	font-family: monospace;
	}
	.reportview-container .main footer, .reportview-container .main footer a {
    	color: black;
	}
	header .decoration {
    	background-image: none;
	}

    	@media (max-width: 991.98px) {
      	.sidebar .sidebar-content {
        	margin-left: auto;
      		}
	}
	</style>
	'''

	st.markdown(page_bg_img, unsafe_allow_html=True)

	st.markdown('<style>h1{color: #C0392B;  text-decoration: underline; font-family: Segoe Print; font-size:24px;border-radius:10%;}</style>', unsafe_allow_html=True)
	st.markdown('<style>p{color:  #8E44AD;   font-family: Segoe Script; font-weight: bold;}</style>', unsafe_allow_html=True)

	st.title(' Sentiment Analysis on Tweets :bird:')


	activities=["Tweet Analyzer","Generate Twitter Data"]

	choice = st.sidebar.selectbox("Select Your Task",activities)

	

	if choice=="Tweet Analyzer":

		st.subheader("USING MACHINE LEARNING TECHNIQUES")


		raw_text = st.text_area(" Enter the Search Query ")
		
		Max_tweets = st.slider("Enter Maximum Tweets to Scrape:", 0, 100, 5)

		Filter_Retweets = st.sidebar.checkbox("Filter Retweets:")
		if Filter_Retweets:
  			raw_text = raw_text + ' -filter:retweets'  # to exclude retweets

		st.sidebar.subheader("Filter By Date Range")
		
		Start_date = st.sidebar.date_input('start date')
		End_date = st.sidebar.date_input('end date')
		
                

		

		Analyzer_choice = st.selectbox("Select the Task",  ["Display Recent Tweets","Generate WordCloud" ,"Visualize the Sentiment Analysis"])

		
		if st.button("Explore"):

			
			if Analyzer_choice == "Display Recent Tweets":

				st.success("Fetching Recent Tweets")

				
				def Show_Recent_Tweets(raw_text):

					# Extract 100 tweets from the twitter
					posts = api.search(q=raw_text, count = Max_tweets, lang ="en", tweet_mode="extended", max_id="Start_date", since_id="End_date")

					
					def get_tweets():

						l=[]
						i=1
						for tweet in posts[:Max_tweets]:
							l.append(tweet.full_text)
							i= i+1
						return l

					recent_tweets=get_tweets()		
					return recent_tweets

				recent_tweets= Show_Recent_Tweets(raw_text)

				st.write(recent_tweets)



			elif Analyzer_choice=="Generate WordCloud":

				st.success("Generating Word Cloud")

				def gen_wordcloud():

					posts = api.search(q=raw_text, count = Max_tweets, lang ="en", tweet_mode="extended")


					# Create a dataframe with a column called Tweets
					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
					# word cloud visualization
					allWords = ' '.join([twts for twts in df['Tweets']])
					wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
					plt.imshow(wordCloud, interpolation="bilinear")
					plt.axis('off')
					plt.savefig('WC.jpg')
					img= Image.open("WC.jpg") 
					return img

				img=gen_wordcloud()

				st.image(img)



			else :



				
				def Plot_Analysis():

					st.success("Generating Visualisation for Sentiment Analysis")

					


					posts = api.search(q=raw_text, count = Max_tweets, lang ="en", tweet_mode="extended")

					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


					
					# Create a function to clean the tweets
					def cleanTxt(text):
					 text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
					 text = re.sub('#', '', text) # Removing '#' hash tag
					 text = re.sub('RT[\s]+', '', text) # Removing RT
					 text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
					 
					 return text


					# Clean the tweets
					df['Tweets'] = df['Tweets'].apply(cleanTxt)


					def getSubjectivity(text):
					   return TextBlob(text).sentiment.subjectivity

					# Create a function to get the polarity
					def getPolarity(text):
					   return  TextBlob(text).sentiment.polarity


					# Create two new columns 'Subjectivity' & 'Polarity'
					df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
					df['Polarity'] = df['Tweets'].apply(getPolarity)


					def getAnalysis(score):
					  if score < 0:
					    return 'Negative'
					  elif score == 0:
					    return 'Neutral'
					  else:
					    return 'Positive'
					    
					df['Analysis'] = df['Polarity'].apply(getAnalysis)


					return df



				df= Plot_Analysis()



				st.write(sns.countplot(x=df["Analysis"],data=df))


				st.pyplot(use_container_width=True)

			

	

	else:

		st.subheader("USING MACHINE LEARNING TECHNIQUES")

		






		user_name = st.text_area("Enter the Search Query")
		Max_tweets = st.slider("Enter Max Tweets to Scrape: ", 0, 100, 5)
		Filter_Retweets = st.sidebar.checkbox("Filter Retweets:")
		if Filter_Retweets:
  			raw_text = raw_text + ' -filter:retweets'  # to exclude retweets

		st.sidebar.subheader("Filter By date Range")
		
		start_date = st.sidebar.date_input('start date')
		end_date = st.sidebar.date_input('end date')
		

		st.markdown("")
		Analyzer_choice = st.selectbox("Select the Task",  ["Generate Data", "Histograph"])


		if st.button("Visualize Data"):

			
			if Analyzer_choice == "Generate Data":

				st.success("Fetching recent Tweets")

				def get_data(user_name):
		

					posts = api.search(q = user_name, count = Max_tweets+1, lang ="en", tweet_mode="extended", max_id="start_date", since_id="end_date")

					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

					def cleanTxt(text):
						text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
						text = re.sub('#', '', text) # Removing '#' hash tag
						text = re.sub('RT[\s]+', '', text) # Removing RT
						text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
						return text

					# Clean the tweets
					df['Tweets'] = df['Tweets'].apply(cleanTxt)


					def getSubjectivity(text):
						return TextBlob(text).sentiment.subjectivity

						# Create a function to get the polarity
					def getPolarity(text):
						return  TextBlob(text).sentiment.polarity


						# Create two new columns 'Subjectivity' & 'Polarity'
					df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
					df['Polarity'] = df['Tweets'].apply(getPolarity)

					def getAnalysis(score):
						if score < 0:
							return 'Negative'

						elif score == 0:
							return 'Neutral'


						else:
							return 'Positive'

		
						    
					df['Analysis'] = df['Polarity'].apply(getAnalysis)
					return df
				df=get_data(user_name)

				st.write(df)


			else:

				def Plot_Analysis():

					st.success("Generating Histograph for polarity and subjectivity")

					


					posts = api.search(q = user_name, count = Max_tweets+1, lang ="en", tweet_mode="extended", max_id="start_date", since_id="end_date")

					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


					
					# Create a function to clean the tweets
					def cleanTxt(text):
					 text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
					 text = re.sub('#', '', text) # Removing '#' hash tag
					 text = re.sub('RT[\s]+', '', text) # Removing RT
					 text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
					 
					 return text


					# Clean the tweets
					df['Tweets'] = df['Tweets'].apply(cleanTxt)


					def getSubjectivity(text):
					   return TextBlob(text).sentiment.subjectivity


					# Create a function to get the polarity
					def getPolarity(text):
					   return  TextBlob(text).sentiment.polarity


					# Create two new columns 'Subjectivity' & 'Polarity'
					
					df['Polarity'] = df['Tweets'].apply(getPolarity)
					df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)

					def getAnalysis(score):
					  if score < 0:
					    return 'Negative'
					  elif score == 0:
					    return 'Neutral'
					  else:
					    return 'Positive'
					    
					df['Analysis'] = df['Polarity'].apply(getAnalysis)


					return df



				df= Plot_Analysis()



				st.write(sns.countplot(x=df["Analysis"],data=df))

				df.hist()
				plt.show()

				st.pyplot(use_container_width=True)
				





	st.markdown('<p>                Built By :  Batch B2            <p>',unsafe_allow_html=True)


			

				


























if __name__ == "__main__":
	app()