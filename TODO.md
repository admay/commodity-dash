# TODO

1. Update `./view.py/create_values` to be more performant.
2. Update the table at the bottom of the page to look nicer/have more data on screen for the users.
3. Come up with a bit of a slicker data model approach. My lack of pandas knowledge hurt me a bit here.
4. Write more generative unit tests for better coverage.
5. Look into async generation of graph and table.
6. Actually cache the table.
7. Error handling.
8. Update app to use [redis cache][0]
  - [Redis docker][1]
  - [Docker Compose][2]
  
-----
[0]: https://dash.plot.ly/performance
[1]: https://hub.docker.com/r/bitnami/redis/
[2]: https://docs.docker.com/compose/
