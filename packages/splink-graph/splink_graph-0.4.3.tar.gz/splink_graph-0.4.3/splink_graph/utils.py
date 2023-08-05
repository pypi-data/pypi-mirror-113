import networkx as nx
from scipy import sparse
import numpy as np
import pyspark
from pyspark.context import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.types import *
import pyspark.sql.functions as f
from pyspark.sql.functions import when
from pyspark.sql.types import LongType, StringType, FloatType, DoubleType



def _graphharmoniser(sparkdf, colsrc, coldst):
    sparkdf = sparkdf.withColumn(
        "newsrc",
        when(f.col(colsrc) < f.col(coldst), f.col(colsrc)).otherwise(f.col(coldst)),
    )
    sparkdf = sparkdf.withColumn(
        "newdst",
        when(f.col(coldst) > f.col(colsrc), f.col(coldst)).otherwise(f.col(colsrc)),
    )
    sparkdf = (
        sparkdf.drop(colsrc)
        .withColumn(colsrc, f.col("newsrc"))
        .drop(coldst)
        .withColumn(coldst, f.col("newdst"))
        .drop("newsrc", "newdst")
    )
    return sparkdf


def _nodearray_from_edge_df(sparkdf, src="src", dst="dst", cluster_id_colname="cluster_id"):

    out = sparkdf.groupby(cluster_id_colname).agg(
        f.collect_set(src).alias("_1"), f.collect_list(dst).alias("_2")
    )
    out = out.withColumn("nodes", f.array_union(f.col("_1"), f.col("_2"))).drop(
        "_1", "_2"
    )
    return out


def _nx_compute_all_pairs_shortest_path(nxgraph, weight=None, normalize=False):

    """
    Takes as input :
        a networkx graph nxGraph
            
    Returns: a dictionary of the computed shortest path lengths between all nodes in a graph. Accepts weighted or unweighted graphs
    
    """

    lengths = nx.all_pairs_dijkstra_path_length(nxgraph, weight=weight)
    lengths = dict(lengths)  # for compatibility with network 1.11 code
    return lengths


def _nx_longest_shortest_path(lengths):
    """
    Takes as input :
        the output of _nx_compute_all_pairs_shortest_path function which is a dictionary of shortest paths from the graph that function took as input
            
    Returns: the longest shortest path 
    This is also known as the *diameter* of a graph

    
    """

    max_length = max([max(lengths[i].values()) for i in lengths])
    return max_length


def _laplacian_matrix(nxgraph):
    """

    Takes as input :
            undirected NetworkX graph
            
    A: Adjacency Matrix
    D: Diagonal Matrix
    L: Laplacian Matrix
            
     Returns:
            Scipy sparse format Laplacian matrix
    """
    A = nx.to_scipy_sparse_matrix(
        nxgraph, format="csr", dtype=np.float, nodelist=nxgraph.nodes
    )
    D = sparse.spdiags(
        data=A.sum(axis=1).flatten(),
        diags=[0],
        m=len(nxgraph),
        n=len(nxgraph),
        format="csr",
    )
    L = D - A

    return L


def _laplacian_spectrum(nxgraph):

    la_spectrum = nx.laplacian_spectrum(nxgraph)
    la_spectrum = np.sort(la_spectrum)  # sort ascending

    return la_spectrum

def _from_unweighted_graphframe_to_nxGraph(g):
    """Takes as input:
       
           an unweighted Graphframe graph g 
           
       Returns: 
       
           an unweighted networkx graph"""

    nxGraph = nx.Graph()
    nxGraph.add_nodes_from(g.vertices.rdd.map(lambda x: x.id).collect())
    nxGraph.add_edges_from(g.edges.rdd.map(lambda x: (x.src, x.dst)).collect())
    return nxGraph


def _from_weighted_graphframe_to_nxGraph(g):
    """Takes as input:
       
           a weighted Graphframe graph g 
           (note: edge weight column needs to be called as weight on the Graphframe)
           
       Returns: 
       
           a weighted networkx graph"""

    nxGraph = nx.Graph()
    nxGraph.add_nodes_from(g.vertices.rdd.map(lambda x: x.id).collect())
    nxGraph.add_weighted_edges_from(
        g.edges.rdd.map(lambda x: (x.src, x.dst, x.weight)).collect()
    )
    return nxGraph
