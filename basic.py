from sys import * 

tokens = []
num_stack = []
symbols ={}
def open_file(filename):
	data = open(filename, "r").read()
	data += "<EOF>"
	return data
def lex(filecontents):
	tok = ""
	state = 0
	string = ""
	expr = ""
	n = ""
	ifexpr = 0
	var_start = 0
	var = ""
	filecontents = list(filecontents)
	for char in filecontents:
		tok +=char
		if tok == " ":
			if state == 0:
				tok = ""
			else:
				tok = " "
		elif tok == "\n" or tok == "<EOF>":
			if expr != "" and ifexpr ==1:
				tokens.append("EXPR: " + expr)
				expr = ""
			elif expr != "" and ifexpr ==0:
				tokens.append("NUM: " + expr)
				expr = ""
			elif var != "":
				tokens.append("VAR:" + var)
				var = ""
				var_start = 0
			tok = ""
		elif tok == "=" and state == 0:
			if expr != "" and ifexpr ==0:
				tokens.append("NUM: " + expr)
				expr = ""
			if var != "":
				tokens.append("VAR:" + var)
				var = ""
				var_start = 0
			if tokens[-1] == "EQUALS":
				tokens[-1]=("EQ&EQ")
			else:
				tokens.append("EQUALS")
			tok = ""
		elif tok == "$" and state == 0:
			var_start = 1
			var += tok
			tok = ""
		elif var_start == 1:
			if tok == "<" or tok == ">":
				if var != "":
					tokens.append("VAR:" + var)
					var = ""
					var_start = 0
			var += tok 
			tok = ""	
		elif tok == "SHOW" or tok == "show":
			tokens.append("SHOW")
			tok = ""
		elif tok == "IF" or tok == "if":
			tokens.append("IF")
			tok = ""
		elif tok == "ENDIF" or tok == "endif":
			tokens.append("ENDIF")
			tok = ""
		elif tok == "THEN" or tok == "then":
			if expr != "" and ifexpr ==0:
				tokens.append("NUM: " + expr)
				expr = ""
			tokens.append("THEN")
			tok = ""
		elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok =="4" or tok == "5" or tok =="6" or tok =="7" or tok =="8" or tok == "9":
			expr += tok
			tok = ""
		elif tok == "+" or tok =="-" or tok == "/" or tok == "*" or tok == "^" or tok == "(" or tok == ")":
			ifexpr = 1
			expr += tok
			tok = ""
		elif tok == "\t":
			tok = ""
		elif tok == "/"or tok == "\"":
			if state == 0:
				state = 1
			elif state == 1:
				tokens.append ("STRING:" + string + "\"" )
				string = ""
				state = 0
				tok = ""
		elif state == 1:
			string += tok
			tok = ""
	print(tokens)
	#return ''
	return tokens 
	

def eval_expr(expr):

	return eval(expr)

def do_show (to_show):
	if (to_show[0:6]== "STRING"):
		to_show = to_show[8:]
		to_show = to_show[:-1]
	elif (to_show[0:3]== "NUM"):
		to_show = to_show[4:]
	elif (to_show[0:4]== "EXPR"):
		to_show = eval_expr(to_show[5:])
	print(to_show)

def do_assign(varname, varvalue):
	symbols[varname[4:]] = varvalue

def get_var(varname):
	varname = varname[4:]
	if varname in symbols:
		return symbols[varname]
	else: 
		return "Variable Error: Undefined variable"
		exit ()

#def get_text(string, varname):
	#i = input(string[1:-1] + " ")
	#symbols[varname] = "STRING:\"" + i  + "\""


def parse (toks):
	i = 0 
	while(i < len(toks)):
		if toks[i] == "ENDIF":
			i +=1
		if toks[i] + " " + toks[i +1][0:6] == "SHOW STRING" or toks[i] + " " + toks[i +1][0:3] == "SHOW NUM" or toks[i] + " " + toks[i +1][0:4] == "SHOW EXPR" or toks[i] + " " + toks[i +1][0:3] == "SHOW VAR":
			if toks[i +1][0:6] == "STRING":
				do_show(toks[i +1])
			elif toks[i+1][0:3] == 'NUM':
				do_show(toks[i +1])
			elif toks[i+1][0:4] == 'EXPR':
				do_show(toks[i +1])
			elif toks[i+1][0:3] == 'VAR':
				do_show(get_var(toks[i+1]))
			i +=2 
		elif toks[i][0:3] + " " + toks[i +1] + " " + toks[i +2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i +1] + " " + toks[i +2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i +1] + " " + toks[i +2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i +1] + " " + toks[i +2][0:3] == "VAR EQUALS VAR" :
			if toks[i +2][0:6] == "STRING":
				do_assign(toks[i], toks[ i+2])
			elif toks[i+2][0:3] == 'NUM':
				do_assign(toks[i], toks[ i+2])
			elif toks[i+2][0:4] == 'EXPR':
				do_assign(toks[i], "NUM:" + str(eval_expr(toks[i+2][5:])))
			elif toks[i+2][0:3] == 'VAR':
				do_assign(toks[i], get_var(toks[ i+2]))
			i +=3 
		elif toks[i]+ " " + toks[i +1][0:3] + " " + toks[i+2][0:3] + " " + toks[i+4] == "IF NUM EQ&EQ NUM THEN":
			if toks[i+1][4:] == toks[i+3][4:]:
				print("True")
			else:
				print("False")
			i +=5
		
			
	#print (symbols)

def run():
	data = open_file(argv[1])
	toks = lex(data)
	parse(toks)
run()