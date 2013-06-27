import sys
import xapian

try:
    database = xapian.Database('test/')
    enquire = xapian.Enquire(database)
    stemmer = xapian.Stem("english")
    terms = []
    for term in sys.argv[1:]:
        terms.append(stemmer(term.lower()))
    query = xapian.Query(xapian.Query.OP_OR, terms)
    print "Performing query `%s'" % query.get_description()

    enquire.set_query(query)
    matches = enquire.get_mset(0, 10)

    print "%i results found" % matches.get_matches_estimated()
    for match in matches:
        print "ID %i %i%% [%s]" % (match[xapian.MSET_DID], match[xapian.MSET_PERCENT], match[xapian.MSET_DOCUMENT].get_data())

except Exception, e:
    print >> sys.stderr, "Exception: %s" % str(e)
    sys.exit(1)