SELECT tok.content, COUNT(tok.content) * SUM(tt.frequency)
     FROM tweet AS t
     JOIN	tweettoken AS tt ON t.id = tt.tweet
     JOIN	token tok ON tt.content = tok.content
         AND tt.content_type = tok.content_type
     WHERE t.sentiment = ?
         AND tok.content_type = ?
     GROUP BY tok.content
     ORDER BY COUNT(tok.content) * SUM(tt.frequency) DESC
     LIMIT ?;