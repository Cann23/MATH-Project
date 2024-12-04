// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the variables.

int                    D = ...; // The faculty has D departments
int              n[1..D] = ...; // department p has exactly a number n[p] of participants in the commission  
int                    N = ...; // The faculty has N members
int              d[1..N] = ...; // the department of i will be denoted by d[i]
float      m[1..N][1..N] = ...; // m[i][j] is the compatibility between members i and j 


// Define here your decision variables and
// any other auxiliary program variables you need.
// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>
dvar boolean x[1..N]; // decision variable x[i] is true if member i is selected
int numberOfTotalParticipants = sum(p in 1..D) n[p]; // total number of participants
float numberOfPair = numberOfTotalParticipants * (numberOfTotalParticipants - 1) / 2;  // total number of pairs    
//<<<<<<<<<<<<<<<<



// Write here the objective function.

//>>>>>>>>>>>>>>>>
maximize sum(i in 1..N, j in i+1..N) m[i][j] * x[i] * x[j] / numberOfPair; // maximize the compatibility of the selected members
//<<<<<<<<<<<<<<<<



subject to {

    // Write here the constraints.

    //>>>>>>>>>>>>>>>>    

// constraint 1 - each department must have exactly required number of participants
forall(p in 1..D)
    sum(i in 1..N: p == d[i]) x[i] == n[p];

// constraint 2 - zero compatibility should be forbidden. 
// If their compatibility is zero, then they cannot be selected together.
forall(i in 1..N, j in i+1..N : m[i][j] == 0)
    x[i] + x[j] <= 1;

// constraint 3 - if 0 < m[i][j] < 0.15, then there must be a third participant
// in the commission k such that m[i][k] > 0.85 and m[k][j] > 0.85
forall(i in 1..N, j in i+1..N : 0 < m[i][j] && m[i][j] < 0.15)
    x[i] + x[j] <= 1 + sum(k in 1..N: m[i][k] > 0.85 && m[k][j] > 0.85) x[k];
    //<<<<<<<<<<<<<<<<
}

// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>

//<<<<<<<<<<<<<<<<
