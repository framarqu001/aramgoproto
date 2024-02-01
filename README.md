A Django project creating a simple op.gg clone for fetching Aram match history.
I Uses the Riot Games Api to fetch matches, champions, and Items. I parse through the releavant data and store the information in a database.
Searching for a username, pulls relevant infomration from the database. If the user is not in the database then calls are made to the riot api to get the relevant information.
Match history is shown using view logic and Django's templates


![test](https://github.com/framarqu001/aramgoproto/assets/119390184/a897134e-8b4f-4d26-b507-9abcea9a9998)

![test2](https://github.com/framarqu001/aramgoproto/assets/119390184/027e3d4b-d02a-4db5-85ea-7c07926b678d)
