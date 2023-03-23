# Film Pitch Bot V2
A simple bot that uses data from [TMBd's free API](https://www.themoviedb.org/) to randomly generate a movie title, description, and cast members based on simple text prediction. 

Movie title and description are then reworded with [OpenAI](https://platform.openai.com) and a movie poster is generated via [DALL·E](https://labs.openai.com/). Sometimes these image requests are rejected due to offensive language in the generated movie description.

These movies are then posted to [Twitter](https://twitter.com/FilmPitchBotV2).
