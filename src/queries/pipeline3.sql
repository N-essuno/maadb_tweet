/* pipeline3 for each sentiment s find the words found in tweets of sentiment s, but not found in the lexical resources
   of sentiment s. */
SELECT tt.content
FROM tweettoken tt
JOIN tweet t ON t.id = tt.tweet
WHERE tt.content_type = 'word'
	AND t.sentiment = ?
	AND tt.content NOT IN(
		SELECT lrw.word AS content
		FROM lexicalresourceword lrw
		JOIN lexicalresource lr ON lrw.lexicalresource = lr.name
		WHERE lr.sentiment = ?
	);