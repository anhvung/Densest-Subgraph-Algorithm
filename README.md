# Densest Subgraph Algorithm
 2-approxiamtion algorithm in linear time

*The Algorithm : *
H = G;
while (G contains at least one edge)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;let v be the node with minimum degree δG (v) in G;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;remove v and all its edges from G;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if ρ(G) > ρ(H) then H ← G;
return H;

![performance_fig](performance_fig.png?raw=true "Title")
![performance_fig](performance_fig2.png?raw=true "Title")
