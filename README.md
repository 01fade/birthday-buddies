# Birthday buddies

WIP. Experiment for a fun little website to display the people you share your birthday with.

## Code base

Code based on https://github.com/sveltejs/template, includes more info on how Svelte is structured/used and how to build/deploy, also see `package.json`. `/public` contains the files to deploy.

## Data base

Check `/wikidata` for python script(s) to query and process data. Because Wikidata queries are slow, the best solution seems to be to query data frequently and then save as a csv (folder contains some examples/experiments). However, with this approach one would have to limit the results somehow to avoid the page getting to heavy on first load. So e.g. only show people that have 30 or more sitelinks (# of language Wikipedias that have an article about this person) or separate results in various csv files and only load when the reader scrolled further down the result list. There are probably other ways to optimize performance.