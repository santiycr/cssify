#!/usr/bin/python

import re
import sys
from optparse import OptionParser

sub_regexes = {
    "tag": "([a-zA-Z][a-zA-Z0-9]{0,10}|\*)",
    "attribute": "[.a-zA-Z_:][-\w:.]*(\(\))?)",
    "value": "\s*[\w/:][-/\w\s,:;.]*"
}

validation_re = (
    "(?P<node>"
      "("
        "^id\([\"\']?(?P<idvalue>%(value)s)[\"\']?\)" # special case! id(idValue)
      "|"
        "(?P<nav>//?)(?P<tag>%(tag)s)" # //div
        "(\[("
          "(?P<matched>(?P<mattr>@?%(attribute)s=[\"\'](?P<mvalue>%(value)s))[\"\']" # [@id="bleh"] and [text()="meh"]
        "|"
          "(?P<contained>contains\((?P<cattr>@?%(attribute)s,\s*[\"\'](?P<cvalue>%(value)s)[\"\']\))" # [contains(text(), "bleh")] or [contains(@id, "bleh")]
        ")\])?"
        "(\[(?P<nth>\d)\])?"
      ")"
    ")" % sub_regexes
)

prog = re.compile(validation_re)


class XpathException(Exception):
    pass


def cssify(xpath):
    """
    Get your XPATHs translated to css automatically! (don't go to crazy on what
    you want to translate, this script is smart but won't do your breakfast).
    """

    css = ""
    position = 0

    while position < len(xpath):
        node = prog.match(xpath[position:])
        if node is None:
            raise XpathException("Invalid or unsupported Xpath: %s" % xpath)
        log("node found: %s" % node)
        match = node.groupdict()
        log("broke node down to: %s" % match)

        if position != 0:
            nav = " " if match['nav'] == "//" else " > "
        else:
            nav = ""

        tag = "" if match['tag'] == "*" else match['tag'] or ""

        if match['idvalue']:
            attr = "#%s" % match['idvalue'].replace(" ", "#")
        elif match['matched']:
            if match['mattr'] == "@id":
                attr = "#%s" % match['mvalue'].replace(" ", "#")
            elif match['mattr'] == "@class":
                attr = ".%s" % match['mvalue'].replace(" ", ".")
            elif match['mattr'] in ["text()", "."]:
                attr = ":contains(^%s$)" % match['mvalue']
            elif match['mattr']:
                if match["mvalue"].find(" ") != -1:
                    match["mvalue"] = "\"%s\"" % match["mvalue"]
                attr = "[%s=%s]" % (match['mattr'].replace("@", ""),
                                    match['mvalue'])
        elif match['contained']:
            if match['cattr'].startswith("@"):
                attr = "[%s*=%s]" % (match['cattr'].replace("@", ""),
                                     match['cvalue'])
            elif match['cattr'] == "text()":
                attr = ":contains(%s)" % match['cvalue']
        else:
            attr = ""

        if match['nth']:
            nth = ":nth-of-type(%s)" % match['nth']
        else:
            nth = ""

        node_css = nav + tag + attr + nth

        log("final node css: %s" % node_css)

        css += node_css
        position += node.end()
    else:
        css = css.strip()
        return css

if __name__ == "__main__":
    usage = "usage: %prog [options] XPATH"
    parser = OptionParser(usage)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")

    (options, args) = parser.parse_args()

    if options.verbose:
        def log(msg):
            print("> %s" % msg)
    else:
        def log(msg):
            pass

    if len(args) != 1:
        parser.error("incorrect number of arguments")
    try:
        print(cssify(args[0]))
    except XpathException as e:
        print(e)
        sys.exit(1)
else:
    def log(msg):
        pass
