
#source("http://bioconductor.org/biocLite.R")
#biocLite(c("graph", "Rgraphviz"))

library (bnlearn)
data (learning.test)
str (learning.test)

bn.gs <- gs(learning.test)
bn.hc <- hc(learning.test, score = "aic")

plot (bn.gs)
graphviz.plot (bn.hc)
