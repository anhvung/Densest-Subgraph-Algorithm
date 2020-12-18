# Densest Subgraph Algorithm
 2-approxiamtion algorithm in linear time

<strong>The Algorithm : </strong><br>
H = G;<br>
while (G contains at least one edge)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;let v be the node with minimum degree δG (v) in G;<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;remove v and all its edges from G;<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if ρ(G) > ρ(H) then H ← G;<br>
return H;<br>

![performance_fig](performance_fig.png?raw=true "Title")
![performance_fig](performance_fig2.png?raw=true "Title")
