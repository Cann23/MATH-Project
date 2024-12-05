main {
	var src = new IloOplModelSource("project.mod");
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	var model = new IloOplModel(def,cplex);
	var data = new IloOplDataSource("project.1.dat");
	var start = new Date;
	var startTime = start.getTime();
	model.addDataSource(data);
	model.generate();
	
	cplex.epgap=0.01;
	
	if (cplex.solve()) {
		writeln("OBJECTIVE: " + cplex.getObjValue());
		
		writeln("Commission: " + model.x);
	}	
	else {
		writeln("Not solution found");
	}
	
	model.end();
	data.end();
	def.end();
	cplex.end();
	src.end();
	
	// print execution time
	var end = new Date();
	var endTime = end.getTime();
	var elapsedTime = endTime - startTime
	writeln("Execution Time : " + elapsedTime + "ms");
	
};