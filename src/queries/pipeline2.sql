SELECT COUNT(lrw.word)
	FROM lexicalresource lr
	JOIN lexicalresourceword lrw ON lr.name = lrw.lexicalresource
	WHERE EXISTS (
		SELECT DISTINCT tok.content AS word
		FROM tweet AS tw
		JOIN tweettoken tt ON tt.tweet = tw.id
		JOIN token AS tok ON tt.content = tok.content AND tt.content_type = tok.content_type
		WHERE tw.sentiment = ?
		AND tok.content = lrw.word);