change-my-view-corpus

Note -- this data in convokit format can be found at: https://drive.google.com/drive/folders/1xZewEwlYKWfKSyjhVt_f1nCO6aKaO27S?usp=sharing
The data available was originally used in the following paper:


Title: Winning Arguments: Interaction Dynamics and Persuasion Strategies in Good-faith Online Discussions

Authors: Chenhao Tan and Vlad Niculae and Cristian Danescu-Niculescu-Mizil and Lillian Lee

Year: 2016

Proceedings of WWW
 


This corpus was created in conjunction with Cornell University Course: CS/INFO 6742 Natural Language Processing and Social Interaction, Fall 2019 (instructor: Cristian Danescu-Niculescu-Mizil)


Contents of this README:

A) Brief description

B) Data description

C) Details on the collection procedure

D) Contact


A) Brief description:

This corpus contains a metadata-rich collection of conversations made in the ChangeMyView subreddit. The chief parameter of interest is the 'success' metadata for each Utterance (see data description below). Each convokit conversation in this dataset is the corresponding full comment thread of an original post made to changemyview. Within each full thread are comments made by Redditors (with the objective of the subreddit to change the opinion of the original post). 

To see the original posts in this data, note that the 'root' metadata of an Utterance (i.e. Reddit comment) would be the same as the 'id' metadata (this only holds true for original posts).
To see successful and unsuccessful arguments (i.e. those measured in Section 4 of the cited paper), note the Utterance metadata field 'success' -- remember: there are two conversant in these arguments, the original poster (OP) and the respondent.

- Summary_statistics:

	Number of Users: 29997
	Number of Utterances: 242360
	Number of Conversations: 2509





B) Data description:

- The main indicator of interest in this data is whether an argument succeeded in changing the original poster's (OP's) view. '
- To denote a successful argument: the "success" field of an utterance takes the value of 1 (these utterances were the comments in the original post that succeeded in changing OP's mind), or the "success" field takes the value of 0 (this collection of utterances were a comment thread that are similar in nature to a successful argument in the full thread(matched on pair_id), but this argument failed to change OP's mind -- See section 4 of the cited paper for selection criteria of successful/unsuccessful arguments.
- The original data compiled by the authors only included the challenger replies. To extract the full argument (i.e. a conversation between OP and the challenger), we selected the comments by OP for inclusion in a successful or unsuccessful argument (i.e. "success" = 1 or 0) by collecting all OP replies to any of the corresponding successful/unsuccessful comments by the challenger. This is a conservative measure of the overall "arugment." It does not include comments made in response to the challenger's posts by other individuals nor include comments made by OP if he replied to those outside individuals. All other comments in the thread (including separate comments made by OP) have the "success" field taking the value of None.
- If you are interested in expanding the 'arguments' to ensure all conversants are included, then I would suggest the following method:

    1. Collect all originally provided successful and unsuccessful comments (collected at the Utterance-level conditioning on both "success" = 1 or 0 and user_id != the OP's user_id).
    2. Collect all comments made by the OP.
    3. Using the reply_to identifier, recur up the comments made in the full comment thread for each original post; collecting every comment thread that OP has made a comment in.
    4. Select any comment thread from step 3 for inclusion in a successful/unsuccessful argument if the challenger has also made a comment in that thread. 

- Overall, I believe the conservative measurement of 'argument' that I have used is better because the second method (above) would include argument threads where a challenger is only minimally relevant.
- Note for pair_ids: the successful-unsuccessful argument pairs originally compiled by the authors are not unique at the Conversation-level nor Utterance-level (i.e. the original posts to the ChangeMyView subreddit can have multiple successful-unsuccessful comment pairs in their full-comment threads **and** some comments can have multiple opposing pairs -- see the relevant metadata fields at Conversation-level and Utterance-level below).


- User-level:
	- contains information about each user (i.e. Redditor)
	- fields: 
		- meta: empty dict (note: the original 'all' data file may have more information on individual Redditors, but the authors' pair_data only had comment-level data, therefore, we included the User-level data because each Redditor has a unique identifier: their Reddit username)

- Utterance-level:
	- contains information about every comment posted in the changemyview subreddit posts that were collected for successful/unsuccessful arguments in Section 4 of the cited paper above
	- fields:
		- id, unique comment identification provided by Reddit
		- user, unique user id (i.e. Reddit username)
		- root, comment identifier of the original post in the thread that this comment was posted in
		- reply_to, unique identifier of the comment that this comment was in direct response to
		- timestamp, comment post time provided by Reddit API
		- text, the full text (in string) of the comment
		- meta:
			- success, an indicator taking the value of 1 if the comment was part of a successful argument thread (i.e. an argument thread that changed the OP's mind), 0 if unsuccessful, and None if not part of either a successful or unsuccessful thread.
			- pair_ids, every successful-unsuccessful argument pair originally compiled by the authors has a unique pair_id. However, it is important to note that not every argument is unique (i.e. a single negative argument within a conversation could have two opposing positive arguments, which necessitates two corresponding pair_ids. Therefore, pair_ids is a list).
			- replies, for the OP post in the thread I constructed this by selecting all comment ids with a "reply_to" field equal to the original post id (I used this construction method because the original data provided by the authors did not include all the children of the OP post in their data format). For all comments besides the original post, the "replies" field was originally provided by Reddit API.
			- originally provided by Reddit API: author_flair_text, author_flair_css_class, banned_by, controversiality, edited, distinguished, user_reports, ups, downs, subreddit_id, subreddit, score_hidden, score, saved, report_reasons, mod_reports,  num_reports, likes, gilded,approved_by,  
		

- Conversation-level
	- fields:
		- _owner: Corpus object: the 'Change My View Corpus'
		- _id: unique comment identifier of the original post, which started the conversation thread
		- _utterance_ids: unique comment identifiers of every Utterance (i.e. comment) in the Reddit thread
		- _meta:
			- op-userID, the Reddit username of the original poster (OP)
			- op-text-body, the text of OP's first post (starting the conversation)
			- op-title, the title of OP's first post 
			- pair_ids, a list of all the successful-unsuccessful pairs in the conversation (to subset the successful from unsuccessful Utterances, refer to the "success" metadata indicator in Utterance-level meta (above))


- Corpus-level
	- fields:
		- meta:
			- name, 'Change My View Corpus'


C) Details on the collection procedure:

We started from the data collected by the Winning Arguments paper (cited above). The data was collected from their host at this blog:
https://chenhaot.com/pages/changemyview.html (note: data used in this corpus is from the original data collection -- NOT the updated data on 11/11/16) 

Note: we originally intended to only convert their pair_data into Convokit format (i.e. the data they use in Section 4 of the paper, which looks at differences between arguments that were convincing/unconvincing to the OP in changing their mind). However, the pair_data only included the replies to the original post (not OP's other comments in the thread -- so there was no conversation, nor did they have all comments in the thread). Therefore, we matched the OP posts in the pair_data with the same observation in their 'all' data, from which we collected all comments for each thread.


To convert the data yourself, please note the 'convert.ipynb' file in the repository.
If there are questions about the original data, please note the paper and readme file hosted on the blog linked above.


D) Contact:
Corpus translated into ConvoKit format by Andrew Szmurlo and Meir Friedenberg
Please email any questions to: as3934@cornell.edu (Andrew Szmurlo)