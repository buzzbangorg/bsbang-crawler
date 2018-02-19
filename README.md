# README #

This is the crawler component of Buzzbang search.

# Setup #

These instructions are for Linux.  Windows is not supported.

1. Create the intermediate crawl database
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

# TODO #
Future possibilities include:

* Possibly switch to using a 3rd party crawler or components rather than this custom-built one. 
Please see https://github.com/justinccdev/bsbang-crawler/issues/5
* Make crawler periodically re-crawl.
* Understand much more structure (e.g. DataSet elements within DataCatalog).
* Parse other Bioschemas and schema.org types used by life sciences websites (e.g. Organization, Service, Product)
* Instead of using Sqlite as intermediate crawl store, use something more scalable (perhaps mongodb, cassandra, etc.).
But also see the item where we may want to replace parts/most of crawling infrastructure with a third party project,
which will already have solved some, if not all, of the scalability issues.
* Crawl and understand PhysicalEntity/BioChemEntity/ResearchEntity once this matures further.

Any other suggestions welcome as Github issues for discussion or as pull requests.

# Hacking #

Contributions welcome!  Please

* Make pull requests to the dev branch.
* Conform to the PEP 8 style guide.

Thanks!
