import dbactions as dba
import osmtonetwork as om
import interpretnetwork as intnet
import tramnet


G = om.getcached("nov10")

#Salwator departure1
a = u'Salwator'
b = u'Salwator'
c = u'Komorowskiego'
na = G.node[2419732952]
nb = G.node[2419732954]
nodeA, nodeB, length, path = intnet.get_shortestpath(G, na, nb)
data = tramnet.build_segmentdefition(G, a, b, c, nodeA, nodeB, path, length )
ret = dba.set_segmentdefiniton(data)
print ret.inserted_id

#Salwator departure2
a = u'Salwator'
b = u'Komorowskiego'
c = u'Jubilat'
na = G.node[2419732954]
nb = G.node[2419720285]
nodeA, nodeB, length, path = intnet.get_shortestpath(G, na, nb)
data = tramnet.build_segmentdefition(G, a, b, c, nodeA, nodeB, path, length )
ret = dba.set_segmentdefiniton(data)
print ret.inserted_id

#Salwator arrival1
a = u'Komorowskiego'
b = u'Salwator'
c = u'Salwator'
na = G.node[2419720287]
nb = G.node[4557118642]
nodeA, nodeB, length, path = intnet.get_shortestpath(G, na, nb)
data = tramnet.build_segmentdefition(G, a, b, c, nodeA, nodeB, path, length )
ret = dba.set_segmentdefiniton(data)
print ret.inserted_id

#Salwator arrival2
a = u'Salwator'
b = u'Salwator'
c = ''
na = G.node[4557118642]
nb = G.node[2419732952]
nodeA, nodeB, length, path = intnet.get_shortestpath(G, na, nb)
data = tramnet.build_segmentdefition(G, a, b, c, nodeA, nodeB, path, length )
ret = dba.set_segmentdefiniton(data)
print ret.inserted_id



