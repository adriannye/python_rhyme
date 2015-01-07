#!/usr/bin/python

import rhyme
import cgi
import sys
import string

sys.stderr = sys.stdout

cgidata = cgi.FieldStorage()

print "Content-type: text/html"
print

print("<html><head><title>Rhyming Dictionary Demo</title></head><body>")

print("<center><h1>Rhyming Dictionary Demo</h1></center>")

print("<form>")
print("Rhyme : ")
print("<input type=text name=rhyme>")
print("<br>")
print("<input type=submit>")
print("</form>")

print("<hr>")

if (cgidata.has_key("rhyme")):
    r = rhyme.Rhyme()

    try:
        rhymes = r.rhyme(cgidata["rhyme"].value)
        keys = rhymes.keys()
        keys.sort()
        print("<dl>")
        for key in keys:
            if (key != 1):
                print("<dt><b>%s syllables</b>" % (key))
            else:
                print("<dt><b>%s syllable</b>" % (key))
            values = rhymes[key]
            values.sort()
            print("<dd>%s" % (string.join(values, ", ")))
        print("</dl>")
    except rhyme.WordNotFound, w:
        print("word not found: \"%s\"" % (w))
else:
    pass

print("</body></html>")
