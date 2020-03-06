#!/usr/bin/python

import re
import sys
from optparse import OptionParser

sub_regexes = {
    "tag": r"([a-zA-Z][a-zA-Z0-9]{0,10}|\*)",
    "attribute": r"[.a-zA-Z_:][-\w:.]*(\(\))?)",
    "value": r"\s*[\w/:][-/\w\s,:;.]*"
}

validation_re = (
    r"(?P<node>"
    r"("
    r"^id\([\"\']?(?P<idvalue>{value})[\"\']?\)"  # special case! id(idValue)
    r"|"
    r"(?P<nav>//?)(?P<tag>{tag})"  # //div
    r"(\[("
    r"(?P<matched>(?P<mattr>@?{attribute}=[\"\'](?P<mvalue>{value}))[\"\']"  # [@id="bleh"] and [text()="meh"]
    r"|"
    r"(?P<contained>contains\((?P<cattr>@?{attribute},\s*[\"\'](?P<cvalue>{value})[\"\']\))"  # [contains(text(), "bleh")] or [contains(@id, "bleh")]
    r")\])?"
    r"(\[(?P<nth>\d)\])?"
    r")"
    r")").format(**sub_regexes)

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
            raise XpathException(
                "Invalid or unsupported Xpath: {}".format(xpath))
        log("node found: {}".format(node))
        match = node.groupdict()
        log("broke node down to: {}".format(match))

        if position != 0:
            nav = " " if match['nav'] == "//" else " > "
        else:
            nav = ""

        tag = "" if match['tag'] == "*" else match['tag'] or ""

        if match['idvalue']:
            attr = "#{}".format(match['idvalue'].replace(" ", "#"))
        elif match['matched']:
            if match['mattr'] == "@id":
                attr = "#{}".format(match['mvalue'].replace(" ", "#"))
            elif match['mattr'] == "@class":
                attr = ".{}".format(match['mvalue'].replace(" ", "."))
            elif match['mattr'] in ["text()", "."]:
                attr = ":contains(^{}$)".format(match['mvalue'])
            elif match['mattr']:
                if match["mvalue"].find(" ") != -1:
                    match["mvalue"] = "\"{}\"".format(match["mvalue"])
                attr = "[{}={}]".format(match['mattr'].replace("@", ""),
                                        match['mvalue'])
        elif match['contained']:
            if match['cattr'].startswith("@"):
                attr = "[{}*={}]".format(match['cattr'].replace("@", ""),
                                         match['cvalue'])
            elif match['cattr'] == "text()":
                attr = ":contains({})".format(match['cvalue'])
        else:
            attr = ""

        if match['nth']:
            nth = ":nth-of-type({})".format(match['nth'])
        else:
            nth = ""

        node_css = nav + tag + attr + nth

        log("final node css: {}".format(node_css))

        css += node_css
        position += node.end()
    else:
        css = css.strip()
        return css


if __name__ == "__main__":
    usage = "usage: %prog [options] XPATH"
    parser = OptionParser(usage)
    parser.add_option("-v",
                      "--verbose",
                      action="store_true",
                      dest="verbose",
                      default=False,
                      help="print status messages to stdout")

    (options, args) = parser.parse_args()

    if options.verbose:

        def log(msg):
            print("> {}".format(msg))
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
