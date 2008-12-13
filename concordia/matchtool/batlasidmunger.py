"""
batlasidmunger.py

"""

from lxml import etree

fieldnames = ['id', 'mapnum', 'type', 'gridsquare', 'citation', 'locdesc', 'label', 'geogname']

def munge(batlas):
    return batlas
    
def loadxml(fn):
    result = []
    d = etree.parse(fn)
    root = d.getroot()
    for r in root.xpath("//*[local-name()='record']"):
        rvals = {}
        rgnames = []
        for k in r.getchildren():
            if k.get('name') == 'geognames':
                rgnames = [gn.text for gn in k.getchildren()]
            else:
                rvals[k.get('name')] = k.text
        ll = []
        if len(rgnames) > 0:            
            for gn in rgnames:
                l = []
                for n in fieldnames:
                    if n != 'geogname':
                        try:
                            l.append(rvals[n])
                        except KeyError:
                            l.append(None)
                l.append(gn)
                t = tuple(l)
                ll.append(t)
        else:
            l = []
            for n in fieldnames:
                if n != 'geogname':
                    try:
                        l.append(rvals[n])
                    except KeyError:
                        l.append(None)
            l.append(None) # the non-existent geogname
            t = tuple(l)
            ll.append(t)
        result.extend(ll)
    return (result)
    