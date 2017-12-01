# README #

This is the crawler component of Buzzbang search.

# Setup #

1. Create intermediate crawl database
```
cd setup
./bsbang-setup-sqlite.py
```

2. Queue URLs for Bioschemas JSON-LD extraction by adding them directly and crawling sitemaps
```
cd ..
./bsbang-crawl.py
```

3. Extract Bioschemas JSON-LD from webpages and insert into the crawl database.
```
./bsbang-extract.py
```

4. Install Solr.

5. Create a Solr core named 'bsbang' 
```
cd $SOLR/bin
./solr create -c bsbang
```

6. Run Solr setup
```
cd $BSBANG/setup
./bsbang-setup-solr.py
```

7. Index the extracted Bioschemas JSON-LD in Solr
```
cd ..
./bsbang-index.py
```

# Frontend #

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
