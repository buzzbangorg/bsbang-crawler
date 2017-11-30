# README #

This is the crawler component of Buzzbang search.

# Usage #

Use bsbang-crawl.py to crawl a webpage, a site or a list of URLs.  The crawled JSON-LD is stored in an sqlite3 database 
in data/crawl.db

```
$ bsbang-crawl.py conf/default-targets.txt
```

Then use bsbang-index.py to insert the JSON-LD into a Solr instance.

```
$ bsbang-index.py
```

See https://github.com/justinccdev/bsbang-frontend for a frontend project to the index.

# Tests #

```
$ python3 -m unittest discover
```

# Hacking #

Contributions welcome!  Please

* Make pull requests to the dev branch.
* Conform to the PEP 8 style guide.

Thanks!
