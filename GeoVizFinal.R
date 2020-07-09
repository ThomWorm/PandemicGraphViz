library(igraph)
library(viridis)
library(matrixStats)
set.seed(1625)

setwd("~/Pandemics/GrapViz")







###########################
simpleTrade <- read.csv("Trade2000.csv", header=T, row.names=1)
simpleEdges <- simpleTrade
simpleEdges[simpleEdges < 90]  <- 0 
simpleEdges[simpleEdges >1]  <- 1 
simpleEdges <- as.matrix(simpleEdges)




simpleNodes <- simpleTrade[1]
colnames(simpleNodes) <- "cumuTrade"
simpleNodes$name <- rownames(simpleNodes)
rownames(simpleNodes) <- NULL
simpleNodes <- simpleNodes[,c(2,1)]
simpleNodes$cumuTrade <- rowSums(simpleTrade, dims =1)
simpleNodes$risk <- (simpleNodes$cumuTrade - min(simpleNodes$cumuTrade)) / ( max(simpleNodes$cumuTrade) - min(simpleNodes$cumuTrade))

simpleNodes

simpleNodes$phytoSan <- sample(c(0,1), replace =T, size = nrow(simpleNodes))
simpleNodes$presence <- sample(c(0,1), replace =T, size = nrow(simpleNodes))



simpleNet <- graph_from_adjacency_matrix(simpleEdges, "directed")


phytoSanDf <- rep(simpleNodes$phytoSan, times = nrow(simpleTrade))





E(simpleNet)$phyto <- phytoSanDf[1:length(E(simpleNet))]
E(simpleNet)$phyto              

E(simpleNet)$edgeColor <- ifelse(E(simpleNet)$phyto > 0,'#93b894','#b8939d')








#set node color based on risk
colrs <- viridis(105)
simpleNodes$color <- colrs[(simpleNodes$risk*100)+1  ]
simpleNodes$risk
simpleNodes$color

#set node boundary based on phytosanitary

#set node size based on total trade volume
simpleNodes$size <- log(simpleNodes$cumuTrade ) *5

#set edge weight based on trade volume
simpleNodes$size <- log(simpleNodes$cumuTrade )


simpleTrade[1]


E(simpleNet)$width <- (as.integer( runif(length(E(simpleNet)), min = 15, max =90))) /10
simpleTrade
E(simpleNet)$width

as.list(simpleTrade)

as.integer(E(simpleNet)$width)
simpleTrade
simpleNodes$frameCol <- ifelse(simpleNodes$phytoSan >0, "#96db00", 
                              "#fa055b")




#Plot
par(bg = "#141417")
plot(simpleNet, edge.arrow.size= .6, edge.color = E(simpleNet)$edgeColor, edge.width= E(simpleNet)$width , edge.curved=0,
     vertex.color=simpleNodes$color, vertex.size= (15 + simpleNodes$size)  , vertex.frame.color= simpleNodes$frameCol, vertex.label=simpleNodes$name, vertex.label.color="darkred",
     vertex.label.cex=1.5 ) 


list_of_v <- simpleNodes$name == "USA"
list_of_edges <- E(simpleNet)[to(list_of_v)]
subg <- subgraph.edges(simpleNet, list_of_edges)
phytoSanDf <- rep(simpleNodes$phytoSan, times = nrow(simpleTrade))





E(subg)$phyto <- phytoSanDf[1:length(E(subg))]
E(subg)$phyto              

E(subg)$edgeColor <- ifelse(E(subg)$phyto > 0,'#93b894','#b8939d')


write.csv(simpleNodes, "fullAttributes.csv")

write.csv(simpleTrade, "fullTrade.csv")






#set node color based on risk
colrs <- viridis(105)
simpleNodes$color <- colrs[(simpleNodes$risk*100)+1  ]
simpleNodes$risk
simpleNodes$color

#set node boundary based on phytosanitary

#set node size based on total trade volume
simpleNodes$size <- log(simpleNodes$cumuTrade ) *5

#set edge weight based on trade volume
simpleNodes$size <- log(simpleNodes$cumuTrade )


simpleTrade[1]


E(subg)$width <- (as.integer( runif(length(E(subg)), min = 15, max =90))) /10
simpleTrade
E(subg)$width

as.list(simpleTrade)

as.integer(E(subg)$width)
simpleTrade
simpleNodes$frameCol <- ifelse(simpleNodes$phytoSan >0, "#96db00", 
                               "#fa055b")




length(E(subg))




par(bg = "#141417")

plot(subg, edge.arrow.size= .6, edge.color = E(subg)$edgeColor, edge.width= E(subg)$width , edge.curved=0,
     vertex.color=simpleNodes$color, vertex.size= (15 + simpleNodes$size[1:length(E(subg))])  , vertex.frame.color= simpleNodes$frameCol[1:length(E(subg))], vertex.label=simpleNodes$name[1:length(E(subg))], vertex.label.color="darkred",
     vertex.label.cex=1.5 ) 
plot(subg)

list_of_edges

length(E(subg))

write.csv(simpleEdges, 'simpleEdges.csv')
write.csv(simpleNodes, 'simpleNodes.csv')

# Set node size based on audience size:
V(net)$size <- V(net)$audience.size*0.7

# The labels are currently node IDs.
# Setting them to NA will render no labels:
V(net)$label.color <- "black"
V(net)$label <- NA

# Set edge width based on weight:
E(net)$width <- E(net)$weight/6

#change arrow size and edge color:
E(net)$arrow.size <- .2
E(net)$edge.color <- "gray80"

plot(net) 

# We can also override the attributes explicitly in the plot:
plot(net, edge.color="orange", vertex.color="gray50") 


# We can also add a legend explaining the meaning of the colors we used:
plot(net) 
legend(x=-1.1, y=-1.1, c("Newspaper","Television", "Online News"), pch=21,
       col="#777777", pt.bg=colrs, pt.cex=2.5, bty="n", ncol=1)


# Sometimes, especially with semantic networks, we may be interested in 
# plotting only the labels of the nodes:

plot(net, vertex.shape="none", vertex.label=V(net)$media, 
     vertex.label.font=2, vertex.label.color="gray40",
     vertex.label.cex=.7, edge.color="gray85")


# Let's color the edges of the graph based on their source node color.
# We'll get the starting node for each edge with "ends()".
edge.start <- ends(net, es=E(net), names=F)[,1]
edge.col <- V(net)$color[edge.start]

plot(net, edge.color=edge.col, edge.curved=.1)


#  ------->> Network Layouts --------

# Network layouts are algorithms that return coordinates for each
# node in a network.

# Let's generate a slightly larger 80-node graph.

net.bg <- sample_pa(80, 1.2) 
V(net.bg)$size <- 8
V(net.bg)$frame.color <- "white"
V(net.bg)$color <- "orange"
V(net.bg)$label <- "" 
E(net.bg)$arrow.mode <- 0
plot(net.bg)

# You can set the layout in the plot function:
plot(net.bg, layout=layout_randomly)

# Or calculate the vertex coordinates in advance:
l <- layout_in_circle(net.bg)
plot(net.bg, layout=l)

# l is simply a matrix of x,y coordinates (N x 2) for the N nodes in the graph. 
# You can generate your own:
l
l <- cbind(1:vcount(net.bg), c(1, vcount(net.bg):2))
plot(net.bg, layout=l)

# This layout is just an example and not very helpful - thankfully
# igraph has a number of built-in layouts, including:

# Randomly placed vertices
l <- layout_randomly(net.bg)
plot(net.bg, layout=l)

# Circle layout
l <- layout_in_circle(net.bg)
plot(net.bg, layout=l)

# 3D sphere layout
l <- layout_on_sphere(net.bg)
plot(net.bg, layout=l)

# The Fruchterman-Reingold force-directed algorithm 
# Nice but slow, most often used in graphs smaller than ~1000 vertices. 
l <- layout_with_fr(net.bg)
plot(net.bg, layout=l)

# You will also notice that the layout is not deterministic - different runs 
# will result in slightly different configurations. Saving the layout in l
# allows us to get the exact same result multiple times.
par(mfrow=c(2,2), mar=c(1,1,1,1))
plot(net.bg, layout=layout_with_fr)
plot(net.bg, layout=layout_with_fr)
plot(net.bg, layout=l)
plot(net.bg, layout=l)
dev.off()

# By default, the coordinates of the plots are rescaled to the [-1,1] interval
# for both x and y. You can change that with the parameter "rescale=FALSE"
# and rescale your plot manually by multiplying the coordinates by a scalar.
# You can use norm_coords to normalize the plot with the boundaries you want.

# Get the layout coordinates:
l <- layout_with_fr(net.bg)
# Normalize them so that they are in the -1, 1 interval:
l <- norm_coords(l, ymin=-1, ymax=1, xmin=-1, xmax=1)

par(mfrow=c(2,2), mar=c(0,0,0,0))
plot(net.bg, rescale=F, layout=l*0.4)
plot(net.bg, rescale=F, layout=l*0.8)
plot(net.bg, rescale=F, layout=l*1.2)
plot(net.bg, rescale=F, layout=l*1.6)
dev.off()

# Another popular force-directed algorithm that produces nice results for
# connected graphs is Kamada Kawai. Like Fruchterman Reingold, it attempts to 
# minimize the energy in a spring system.

l <- layout_with_kk(net.bg)
plot(net.bg, layout=l)

# The LGL algorithm is for large connected graphs. Here you can specify a root - 
# the node that will be placed in the middle of the layout.
plot(net.bg, layout=layout_with_lgl)

# By default, igraph uses a layout called layout_nicely which selects
# an appropriate layout algorithm based on the properties of the graph. 

# Check out all available layouts in igraph:
?igraph::layout_

layouts <- grep("^layout_", ls("package:igraph"), value=TRUE)[-1] 
# Remove layouts that do not apply to our graph.
layouts <- layouts[!grepl("bipartite|merge|norm|sugiyama|tree", layouts)]

par(mfrow=c(3,3), mar=c(1,1,1,1))

for (layout in layouts) {
  print(layout)
  l <- do.call(layout, list(net)) 
  plot(net, edge.arrow.mode=0, layout=l, main=layout) }

dev.off()


-----------------------------------
# * TASK FOR WORKSHOP PARTICIPANTS:

# Plot the Zachary karate club network with four different layouts of your choice.

-----------------------------------

  

# ------->> Improving network plots --------

plot(net)

# Notice that this network plot is still not too helpful.
# We can identify the type and size of nodes, but cannot see
# much about the structure since the links we're examining are so dense.
# One way to approach this is to see if we can sparsify the network.

hist(links$weight)
mean(links$weight)
sd(links$weight)

# There are more sophisticated ways to extract the key edges,
# but for the purposes of this excercise we'll only keep ones
# that have weight higher than the mean for the network.

# We can delete edges using delete_edges(net, edges)
cut.off <- mean(links$weight) 
net.sp <- delete_edges(net, E(net)[weight<cut.off])
plot(net.sp) 

# Another way to think about this is to plot the two tie types 
# (hyperlik & mention) separately:

E(net)$width <- 2
plot(net, edge.color=c("dark red", "slategrey")[(E(net)$type=="hyperlink")+1],
      vertex.color="gray40", layout=layout_in_circle)

# Another way to delete edges:  
net.m <- net - E(net)[E(net)$type=="hyperlink"]
net.h <- net - E(net)[E(net)$type=="mention"]

# Plot the two links separately:
par(mfrow=c(1,2))

plot(net.h, vertex.color="orange", main="Tie: Hyperlink")
plot(net.m, vertex.color="lightsteelblue2", main="Tie: Mention")

dev.off()

# Make sure the nodes stay in place in both plots:
par(mfrow=c(1,2),mar=c(1,1,4,1))

l <- layout_with_fr(net)
plot(net.h, vertex.color="orange", layout=l, main="Tie: Hyperlink")
plot(net.m, vertex.color="lightsteelblue2", layout=l, main="Tie: Mention")

dev.off()


# ------->> Interactive plotting with tkplot -------- 

# R and igraph offer interactive plotting capabilities
# (mostly helpful for small networks)

tkid <- tkplot(net) #tkid is the id of the tkplot
l <- tkplot.getcoords(tkid) # grab the coordinates from tkplot
tk_close(tkid, window.close = T)
plot(net, layout=l)


# ------->> Heatmaps as a way to represent networks -------- 

# A quick reminder that there are other ways to represent a network:

# Heatmap of the network matrix:
netm <- get.adjacency(net, attr="weight", sparse=F)
colnames(netm) <- V(net)$media
rownames(netm) <- V(net)$media

palf <- colorRampPalette(c("gold", "dark orange")) 
heatmap(netm[,17:1], Rowv = NA, Colv = NA, col = palf(20), 
        scale="none", margins=c(10,10) )


# ------->> Plotting two-mode networks with igraph --------  

head(nodes2)
head(links2)

net2
plot(net2)

# This time we will make nodes look different based on their type.
V(net2)$color <- c("steel blue", "orange")[V(net2)$type+1]
V(net2)$shape <- c("square", "circle")[V(net2)$type+1]
V(net2)$label <- ""
V(net2)$label[V(net2)$type==F] <- nodes2$media[V(net2)$type==F] 
V(net2)$label.cex=.6
V(net2)$label.font=2

plot(net2, vertex.label.color="white", vertex.size=(2-V(net2)$type)*8) 

plot(net2, vertex.label=NA, vertex.size=7, layout=layout_as_bipartite) 

 
# Using text as nodes:
par(mar=c(0,0,0,0))
plot(net2, vertex.shape="none", vertex.label=nodes2$media,
     vertex.label.color=V(net2)$color, vertex.label.font=2, 
     vertex.label.cex=.95, edge.color="gray70",  edge.width=2)

dev.off()


# ================ 6. Network and node descriptives ================


# Density
# The proportion of present edges from all possible ties.
edge_density(net, loops=F)
ecount(net)/(vcount(net)*(vcount(net)-1)) #for a directed network

# Reciprocity
# The proportion of reciprocated ties (for a directed network).
reciprocity(net)
dyad_census(net) # Mutual, asymmetric, and null node pairs
2*dyad_census(net)$mut/ecount(net) # Calculating reciprocity

# Transitivity
# global - ratio of triangles (direction disregarded) to connected triples
# local - ratio of triangles to connected triples each vertex is part of
transitivity(net, type="global")  # net is treated as an undirected network
transitivity(as.undirected(net, mode="collapse")) # same as above
transitivity(net, type="local")
triad_census(net) # for directed networks

# Triad types (per Davis & Leinhardt):
# 
# 003  A, B, C, empty triad.
# 012  A->B, C 
# 102  A<->B, C  
# 021D A<-B->C 
# 021U A->B<-C 
# 021C A->B->C
# 111D A<->B<-C
# 111U A<->B->C
# 030T A->B<-C, A->C
# 030C A<-B<-C, A->C.
# 201  A<->B<->C.
# 120D A<-B->C, A<->C.
# 120U A->B<-C, A<->C.
# 120C A->B->C, A<->C.
# 210  A->B<->C, A<->C.
# 300  A<->B<->C, A<->C, completely connected.


# Diameter (longest geodesic distance)
# Note that edge weights are used by default, unless set to NA.
diameter(net, directed=F, weights=NA)
diameter(net, directed=F)
diam <- get_diameter(net, directed=T)
diam

# Note: vertex sequences asked to behave as a vector produce numeric index of nodes
class(diam)
as.vector(diam)

# Color nodes along the diameter:
vcol <- rep("gray40", vcount(net))
vcol[diam] <- "gold"
ecol <- rep("gray80", ecount(net))
ecol[E(net, path=diam)] <- "orange" 
# E(net, path=diam) finds edges along a path, here 'diam'
plot(net, vertex.color=vcol, edge.color=ecol, edge.arrow.mode=0)

# Node degrees
# 'degree' has a mode of 'in' for in-degree, 'out' for out-degree,
# and 'all' or 'total' for total degree. 
deg <- degree(net, mode="all")
plot(net, vertex.size=deg*3)
hist(deg, breaks=1:vcount(net)-1, main="Histogram of node degree")

# Degree distribution
deg.dist <- degree_distribution(net, cumulative=T, mode="all")
plot( x=0:max(deg), y=1-deg.dist, pch=19, cex=1.2, col="orange", 
      xlab="Degree", ylab="Cumulative Frequency")


# Centrality & centralization

# Centrality functions (vertex level) and centralization functions (graph level).
# The centralization functions return "res" - vertex centrality, "centralization", 
# and "theoretical_max" - maximum centralization score for a graph of that size.
# The centrality functions can run on a subset of nodes (set with the "vids" parameter)

# Degree (number of ties)
degree(net, mode="in")
centr_degree(net, mode="in", normalized=T)

# Closeness (centrality based on distance to others in the graph)
# Inverse of the node's average geodesic distance to others in the network
closeness(net, mode="all", weights=NA) 
centr_clo(net, mode="all", normalized=T) 

# Eigenvector (centrality proportional to the sum of connection centralities)
# Values of the first eigenvector of the graph adjacency matrix
eigen_centrality(net, directed=T, weights=NA)
centr_eigen(net, directed=T, normalized=T) 

# Betweenness (centrality based on a broker position connecting others)
# (Number of geodesics that pass through the node or the edge)
betweenness(net, directed=T, weights=NA)
edge_betweenness(net, directed=T, weights=NA)
centr_betw(net, directed=T, normalized=T)



-----------------------------------
# * TASK FOR WORKSHOP PARTICIPANTS:

# Compute the degree, closeness, eigenvector, and betweenness centrality of
# the actors in the Zachary karate club network. Plot the network, sizing the
# nodes based on the different centrality types.

-----------------------------------

  

# Hubs and authorities

# The hubs and authorities algorithm developed by Jon Kleinberg was initially used 
# to examine web pages. Hubs were expected to contain catalogues with a large number 
# of outgoing links; while authorities would get many incoming links from hubs, 
# presumably because of their high-quality relevant information. 

hs <- hub_score(net, weights=NA)$vector
as <- authority_score(net, weights=NA)$vector

par(mfrow=c(1,2))
 plot(net, vertex.size=hs*50, main="Hubs")
 plot(net, vertex.size=as*30, main="Authorities")
dev.off()


# ================ 7. Distances and paths ================


# Average path length 
# The mean of the shortest distance between each pair of nodes in the network 
# (in both directions for directed graphs). 
mean_distance(net, directed=F)
mean_distance(net, directed=T)

# We can also find the length of all shortest paths in the graph:
distances(net) # with edge weights
distances(net, weights=NA) # ignore weights

# We can extract the distances to a node or set of nodes we are interested in.
# Here we will get the distance of every media from the New York Times.
dist.from.NYT <- distances(net, v=V(net)[media=="NY Times"], to=V(net), weights=NA)

# Set colors to plot the distances:
oranges <- colorRampPalette(c("dark red", "gold"))
col <- oranges(max(dist.from.NYT)+1)
col <- col[dist.from.NYT+1]

plot(net, vertex.color=col, vertex.label=dist.from.NYT, edge.arrow.size=.6, 
     vertex.label.color="white")

# We can also find the shortest path between specific nodes.
# Say here between MSNBC and the New York Post:
news.path <- shortest_paths(net, 
                            from = V(net)[media=="MSNBC"], 
                             to  = V(net)[media=="New York Post"],
                             output = "both") # both path nodes and edges

# Generate edge color variable to plot the path:
ecol <- rep("gray80", ecount(net))
ecol[unlist(news.path$epath)] <- "orange"
# Generate edge width variable to plot the path:
ew <- rep(2, ecount(net))
ew[unlist(news.path$epath)] <- 4
# Generate node color variable to plot the path:
vcol <- rep("gray40", vcount(net))
vcol[unlist(news.path$vpath)] <- "gold"

plot(net, vertex.color=vcol, edge.color=ecol, 
     edge.width=ew, edge.arrow.mode=0)


# Identify the edges going into or out of a vertex, for instance the WSJ.
# For a single node, use 'incident()', for multiple nodes use 'incident_edges()'
inc.edges <- incident(net, V(net)[media=="Wall Street Journal"], mode="all")

# Set colors to plot the selected edges.
ecol <- rep("gray80", ecount(net))
ecol[inc.edges] <- "orange"
vcol <- rep("grey40", vcount(net))
vcol[V(net)$media=="Wall Street Journal"] <- "gold"
plot(net, vertex.color=vcol, edge.color=ecol)


# We can also easily identify the immediate neighbors of a vertex, say WSJ.
# The 'neighbors' function finds all nodes one step out from the focal actor.
# To find the neighbors for multiple nodes, use 'adjacent_vertices()'.
# To find node neighborhoods going more than one step out, use function 'ego()'
# with parameter 'order' set to the number of steps out to go from the focal node(s).

neigh.nodes <- neighbors(net, V(net)[media=="Wall Street Journal"], mode="out")

# Set colors to plot the neighbors:
vcol[neigh.nodes] <- "#ff9d00"
plot(net, vertex.color=vcol)

# Special operators for the indexing of edge sequences: %--%, %->%, %<-%
# E(network)[X %--% Y] selects edges between vertex sets X and Y, ignoring direction
# E(network)[X %->% Y] selects edges from vertex sets X to vertex set Y
# E(network)[X %->% Y] selects edges from vertex sets Y to vertex set X

# For example, select edges from newspapers to online sources:
E(net)[ V(net)[type.label=="Newspaper"] %->% V(net)[type.label=="Online"] ]

# Cocitation (for a couple of nodes, how many shared nominations they have)
cocitation(net)



# ================ 8. Subgroups and communities ================

# Converting 'net' to an undirected network.
# There are several ways to do that: we can create an undirected link between any pair
# of connected nodes (mode="collapse), or create an undirected link for each directed
# one (mode="each"), or create an undirected link for each symmetric link (mode="mutual").
# In cases when A -> B and B -> A are collapsed into a single undirected link, we
# need to specify what to do with the edge attributes. Here we have said that
# the 'weight' of links should be summed, and all other edge attributes ignored.

net.sym <- as.undirected(net, mode="collapse", edge.attr.comb=list(weight="sum", "ignore"))


#  ------->> Cliques --------

 # Find cliques (complete subgraphs of an undirected graph)
cliques(net.sym) # list of cliques       
sapply(cliques(net.sym), length) # clique sizes
largest_cliques(net.sym) # cliques with max number of nodes

vcol <- rep("grey80", vcount(net.sym))
vcol[unlist(largest_cliques(net.sym))] <- "gold"
plot(net.sym, vertex.label=V(net.sym)$name, vertex.color=vcol)



#  ------->> Communities --------

# A number of algorithms aim to detect groups that consist of densely connected nodes
# with fewer connections across groups. 

# Community detection based on edge betweenness (Newman-Girvan)
# High-betweenness edges are removed sequentially (recalculating at each step)
# and the best partitioning of the network is selected.
ceb <- cluster_edge_betweenness(net) 
dendPlot(ceb, mode="hclust")
plot(ceb, net) 

# Let's examine the community detection igraph object:
class(ceb)
length(ceb)     # number of communities
membership(ceb) # community membership for each node
crossing(ceb, net)   # boolean vector: TRUE for edges across communities
modularity(ceb) # how modular the graph partitioning is

# High modularity for a partitioning reflects dense connections within communities 
# and sparse connections across communities.


# Community detection based on propagating labels
# Assigns node labels, randomizes, and replaces each vertex's label with
# the label that appears most frequently among neighbors. Repeated until
# each vertex has the most common label of its neighbors.
clp <- cluster_label_prop(net)
plot(clp, net)

# Community detection based on greedy optimization of modularity
cfg <- cluster_fast_greedy(as.undirected(net))
plot(cfg, as.undirected(net))
 
# We can also plot the communities without relying on their built-in plot:
V(net)$community <- cfg$membership
colrs <- adjustcolor( c("gray50", "tomato", "gold", "yellowgreen"), alpha=.6)
plot(net, vertex.color=colrs[V(net)$community])


-----------------------------------
# * TASK FOR WORKSHOP PARTICIPANTS:

# Plot the results of the three different community detection algorithms 
#  applied to  the Zachary karate club network. 
  
-----------------------------------


# K-core decomposition
# The k-core is the maximal subgraph in which every node has degree of at least k
# This also means that the (k+1)-core will be a subgraph of the k-core.
# The result here gives the coreness of each vertex in the network.
kc <- coreness(net, mode="all")
plot(net, vertex.size=kc*6, vertex.label=kc, vertex.color=colrs[kc])


# ================ 9. Assortativity and Homophily ================

# Assortativity (homophily)
# The tendency of nodes to connect to others who are similar on some variable.
# assortativity_nominal() is for categorical variables (labels)
# assortativity() is for ordinal and above variables
# assortativity_degree() checks assortativity in node degrees

V(net)$type.label
V(net)$media.type

assortativity_nominal(net, V(net)$media.type, directed=F)

assortativity(net, V(net)$audience.size, directed=F)

assortativity_degree(net, directed=F)


# ================ The End ================




