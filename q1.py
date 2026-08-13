## Convert a ratings string into a list of (title, rating) tuples.
def parse_ratings(data: str) -> list:
    ratings = []

    for entry in data.split(","):
        title, rating = entry.split(":")
        ratings.append((title.strip(), int(rating.strip())))

    return ratings

## average rating of one movie
def average_rating(ratings, title) -> float:
    movie_ratings = [rating for movie, rating in ratings if movie == title]

    if not movie_ratings:
        return 0.0

    return round(sum(movie_ratings) / len(movie_ratings), 1)

## title with the highest average
def best_movie(ratings) -> str:
    titles = {movie for movie, _ in ratings} ## set 

    best_title = ""
    best_avg = -1

    for title in titles:
        avg = average_rating(ratings, title)
        if avg > best_avg:
            best_avg = avg
            best_title = title

    return best_title

## how many ratings each movie received
def rating_counts(ratings) -> dict:
    counts = {}

    for title, _ in ratings:
        counts[title] = counts.get(title, 0) + 1

    return counts

data = "Dune:8, Dune:9, Barbie:7, Dune:10, Barbie:9, Oppenheimer:9, Barbie:6"

ratings = parse_ratings(data)

print("Demo... ")

print("Parsed ratings:", ratings)
print("Average rating for Dune:", average_rating(ratings, "Dune"))
print("Average rating for Barbie:", average_rating(ratings, "Barbie"))
print("Average rating for Oppenheimer:", average_rating(ratings, "Oppenheimer"))
print("Average rating for None:", average_rating(ratings, "None"))
print("Best movie:", best_movie(ratings))
print("Rating counts:", rating_counts(ratings))
