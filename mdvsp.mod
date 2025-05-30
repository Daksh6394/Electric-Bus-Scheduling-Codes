tuple Node {
  int id;
  int time;
  string loc;
};

tuple Arc {
  Node src;
  Node dst;
  int cost;
  int cap;
};

int nNodes = ...;
int nVehicles = ...;
int MinUtilTime = ...;

range N = 1..nNodes;
range K = 1..nVehicles;
range H = 0..23;

{string} L = ...;

int freq1[H] = ...;
int freq2[H] = ...;

{Node} V = ...;
{Arc} E = ...;

int id0 = ...;
int idend = ...;

dvar int+ x[N][N][K];
dvar int+ T[K];
dvar int+ z[K];

minimize sum(k in K, edge in E) edge.cost*x[edge.src.id][edge.dst.id][k];

subject to {
  forall(k in K) {
    T[k] == sum(edge in E : edge.cap == 1) x[edge.src.id][edge.dst.id][k]*edge.cost;
    z[k] == max(edge in E : edge.cap == 1) x[edge.src.id][edge.dst.id][k];
    
    T[k] >= z[k]*MinUtilTime; 
  }
  
  sum(edge in E : edge.src.id == id0, k in K)
    x[edge.src.id][edge.dst.id][k] == nVehicles;
  
  sum(edge in E : edge.dst.id == idend, k in K)
    x[edge.src.id][edge.dst.id][k] == nVehicles;
  
  forall(i in V : i.id != id0 && i.id != idend) {
    sum(edge in E : edge.src == i, k in K) x[edge.src.id][edge.dst.id][k]
    	== sum(edge in E : edge.dst == i, k in K) x[edge.src.id][edge.dst.id][k];
  }
  
  forall(h in H) {
    sum(edge in E : edge.cap == 1 && edge.src.loc == "ATB" && edge.src.time div 60 == h, k in K)
      x[edge.src.id][edge.dst.id][k] >= freq1[h];
    
    sum(edge in E : edge.cap == 1 && edge.src.loc == "HSK" && edge.src.time div 60 == h, k in K)
      x[edge.src.id][edge.dst.id][k] >= freq2[h];
  }
  
  forall(edge in E : edge.cap == 1)
    sum(k in K)
    	x[edge.src.id][edge.dst.id][k] <= 1;
    
//  sum(edge in E : edge.src.id != id0 && edge.dst.id != idend, k in K)
//    x[edge.src.id][edge.dst.id][k] <= 1;
  
  forall(edge in E, k in K)
    x[edge.src.id][edge.dst.id][k] <= edge.cap;
}

execute {
  
  function getNode(ID) {
    for (var node in V) {
      if (node.id == ID) {
        return node;
      }
    }
    return null;
  }
  
  var vehicles = 0;
  
  for (var i in N) {
    for (var j in N) {
      for (var k in K) {
        if (x[i][j][k] > 0) {
          var src = getNode(i);
          if (x[i][j][k] == 1 && src.loc == "X") {
            vehicles++;
          }
          var dst = getNode(j);
          var src_hour = Math.floor(src.time / 60);
          var src_min = src.time % 60;
          var dst_hour = Math.floor(dst.time / 60);
          var dst_min = dst.time % 60;
          writeln("(", src.loc, " at ", src_hour, ":", src_min, ") --> (", dst.loc, " at ", dst_hour, ":", dst_min,"), flow = ", x[i][j][k]);
        }
      }
    }
  }
  writeln("Optimal Objective Value: ", cplex.getObjValue());
  writeln("No. of vehicles = ", vehicles); explain this in detail
