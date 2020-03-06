## Further Feedback 

For client Tom and further team member's notice, we've collected further feedback after the 2nd User Survey.

The feedback comes from Audit 3 of Sem2, Showcase, team members and friends. 


1. Could use 'minutes ago', 'hours ago' instead of hard time display.

2. Website UI too plain, the design of search bar could be more attractive.

3. The meaning of 'up arrow' and 'twitter icon' is a bit vague. It is a bit difficult for people relate them to 'upvote' and 'twitter search'. 

4. Some of the users wish to have a down vote or remove unattractive news. 

5. Some users wish to have a personal recommendation. (But it depends on Tom's wish)

6. Maybe move the project from port (5000, 8080) to formal domain.

## Protential problems and handover
1. Current database design does not allow two extraction thread run at the same time (Upload_v0.py, UploadRSS_v0.py). It will cause duplicate newsid problem. This will reduce the speed of extraction. For now, Upload_v0 runs for about 5 minutes, UploadRSS_v0 runs for about 30 minutes. 

2. Current database design does not have a 'database clear' method. So the amount of news in the database will get bigger and bigger. To keep the website effective, we might need to remain the latest 1000 news in the database or so. 

3. Current score method for Global and Australia is using title only to avoid news sources with very short text always getting a very low score. But finally we might still need to transfer to using text as this would be more accurate. You can try to solve the problem by inspecting some specific news sources (ABC and SBS) getting very short text, or you can make some attempts to improve the ML model (like using title + first 3 sentences or so).

4. Current ML model is trained by fasttext. The version should be exactly 0.8.3. This is not the latest version. If you still wish to try fasttext, it could not be installed on virtual environment like anaconda, and it only works on linux system. The Training data is stored on the server /share. kosmos3.p contains 600,000+ full news info, annoheadlines.p contains 600,000+ news titles. 

5. The trained model could all be found on the server: /geo/Sem2Deploy/NewsAggregatorSem2/Rank/FastText/Output. Some of the models are too big so they are not pushed to github. We are using 300k_headline for now. It is trained using 300,000 news title only. 

6. If you wish to get access to what we have deployed in the previous semesters, you can use FileZilla. 

The first semester's thing is deployed to gpu.jkl.io:5000, under the routine /u6135925/PythonFlask

The second semester's thing is deployed to gpu.jkl.io:8080, under the routine /geo/Sem2Deploy/NewsAggregatorSem2

If you wish to do something related to process control, you may need to log in u6135925 or geo's account. Please contact zammberdi@gmail.com for the account and password, or turn to Tom for help.

7. The basic machine learning theory is as follows: 

We use cluster method (currently using HDBSCAN) to cluster news word vectors. We regard news that could be clustered as 'important' and label with 1, news that not be clustered as 'unimportant' and label with 0. Then we use the labeled news to train the machine learning model.

8. For frontend part, the website could be run using setup.py. To run it you need to install PythonFlask. 

9. To show news contents, you need to set up mongodb using the query in the /PythonFlask/Extraction/ExtractionV0/readme.md. There are 2 DataBase. Configure has a collection called config; NewsAggregator has a collection called news. You only need to set up config using the insert. There is no need to set up news. To fetch news you can use /PythonFlask/Extraction/ExtractionV0/Upload_v0.py or the RSS version.
