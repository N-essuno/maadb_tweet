/* pipeline3 for each sentiment s find the words found in tweets of sentiment s, but not found in the lexical resources
   of sentiment s. */
SELECT w.content
FROM token w
JOIN tweettoken tt ON w.content = tt.content AND w.content_type = tt.content_type
JOIN tweet t ON t.id = tt.tweet
WHERE w.content_type = 'word'
	AND t.sentiment = ?
	AND w.content NOT IN(
		SELECT content
		FROM lexicalresourceword lrw
		JOIN lexicalresource lr ON lrw.lexicalresource = lr.name
		JOIN tweettoken tt ON tt.content = lrw.word
		WHERE lr.sentiment = ?
	);