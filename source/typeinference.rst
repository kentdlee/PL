======================================
Type Inference
======================================


Why Static Type Inference?
---------------------------


.. container:: figboxcenter

	.. code-block:: sml
		:linenos:

		let val x = ref 0
		in
		  x := !x + 1;
		  println (!x)
		end

	**Fig 8.1** test8.sml


.. container:: figboxcenter

	.. code-block:: sml
		:linenos:

		let val x = ref 0
		in
		  x := x + 1;
		  println (x)
		end

	**Fig 8.2** test13.sml

.. container:: figboxcenter

	.. code-block:: sml
		:linenos:

		exception E of int;
		fun g(y) = raise E(y);
		fun f(x) =
		    let
		      exception E of real;
		      fun z(y)= raise E(y);
		    in
		      x(3.0);
		      z(3)
		    end;
		f(g);

	**Fig. 8.3** Exception Program


.. code-block:: text

	stdIn:216.8-216.12 Error: operator and operand don't agree [literal]
	  operator domain: real
	  operand:         int
	  in expression:
	    z 3


.. container:: figboxcenter

	.. code-block:: sml
		:linenos:

		let val x = 6
		in
		  println x
		  println "Done"
		end

	**Fig 8.4** A bad function call


Type Inference Rules
-----------------------

**RuleName**

	.. math::

		\frac{Premise_1,~~Premise_2,~~...,~~Premise_n}{Conclusion}





Using Prolog
--------------

.. container:: figboxcenter

	.. code-block:: prolog

	    letdec(
		  bindval(idpat('x'),apply(id('ref'),int('0'))),
	      [apply(id(':='),tuple([id('x'),
	       apply(id('+'),tuple([apply(id('!'),id('x')),
	             int('1')]))])),
	       apply(id('println'),apply(id('!'),id('x')))
	      ]).

    **Fig. 8.5** test8.sml prolog AST


.. container:: figboxcenter

	.. code-block:: prolog
		:linenos:

		finalStatus(typeerror) :- print('The program failed to pass the typechecker.'), nl, !.
		finalStatus(_) :- print('The program passed the typechecker.'), nl, !.

		warning([],_) :- !.
		warning(_,fn(_,_)) :- !.
		warning([_|_],_) :-
		  print('Warning: type vars not instantiated in result type initialized to dummy types!'),
		  nl, nl, !.

		errorOut(error(E)) :-
		     nl, nl, print('Error: Typechecking failed. Message was : '), nl,
		     print(E), nl, nl, halt(0).
		errorOut(typeerror(E)) :-
		     nl, nl, print('Error: Typechecking failed due to type error. Message was : '), nl,
		     print(E), nl, nl, halt(0).
		errorOut(E) :-
		     nl, nl, print('Error: Typechecking failed for unknown reason : '), nl,
		     print(E), nl, nl, halt(0).
		run :- print('Typechecking is commencing...'), nl,
		       readAST(AST), print('Here is the AST'), nl, print(AST), nl, nl, nl,
		       catch(typecheckProgram(AST,Type),E,errorOut(E)),
		       nl, nl, print('val it : '), printType(Type,TypeVars), nl, nl,
		       warning(TypeVars,Type), finalStatus(Type).
		runNonInteractive :- run, halt(0).


	**Fig. 8.6** The Type Checker run Predicate


.. container:: figboxcenter

	.. code-block:: sml
		:linenos:

		datatype
		  exp = int of string
		      | ch of string
		      | str of string
		      | bool of string
		      | id of string
		      | listcon of exp list
		      | tuplecon of exp list
		      | apply of exp * exp
		      | expsequence of exp list
		      | letdec of dec * (exp list)
		      | handlexp of exp * match list
		      | ifthen of exp * exp * exp
		      | whiledo of exp * exp
		      | func of string * match list
		and
		  match = match of pat * exp
		and
		  pat = intpat of string
		      | chpat of string
		      | strpat of string
		      | boolpat of string
		      | idpat of string
		      | wildcardpat
		      | infixpat of string * pat * pat
		      | tuplepat of pat list
		      | listpat of pat list
		      | aspat of string * pat
		and
		  dec = bindval of pat * exp
		      | bindvalrec of pat * exp
		      | funmatch of string * match list
		      | funmatches of (string * match list) list


	**Fig. 8.7** AST Description


.. container:: figboxcenter

	.. code-block:: text

		type = bool
		     | int
		     | str
		     | exn
		     | tuple of type list
		     | listOf of type
		     | fn of type * type
		     | ref of type
		     | typevar of string
		     | typeerror

	**Fig. 8.8** Small Types


The Type Environment
----------------------


.. container:: figboxcenter

	.. code-block:: prolog

		typecheckProgram(Expression,Type) :-
		    typecheckExp([('Exception',fn(typevar(a),exn)),
		                  ('raise',fn(exn,typevar(a))),
		                  ('andalso',fn(tuple([bool,bool]),bool)),
		                  ('orelse',fn(tuple([bool,bool]),bool)),
		                  (':=',fn(tuple([ref(typevar(a)),typevar(a)]),tuple([]))),
		                  ('!',fn(ref(typevar(a)),typevar(a))),
		                  ('ref',fn(typevar(a),ref(typevar(a)))),
		                  ('::',fn(tuple([typevar(a),listOf(typevar(a))]),listOf(typevar(a)))),
		                  ('>', fn(tuple([typevar(a),typevar(a)]),bool)),
		                  ('<', fn(tuple([typevar(a),typevar(a)]),bool)),
		                  (@,fn(tuple([listOf(typevar(a)),listOf(typevar(a))]),listOf(typevar(a)))),
		                  ('Int.fromString',fn(str,int)),
		                  ('input',fn(str,str)),
		                  ('explode',fn(str,listOf(str))),
		                  ('implode',fn(listOf(str),str)),
		                  ('println',fn(typevar(a),tuple([]))),
		                  ('print',fn(typevar(a),tuple([]))),
		                  ('cprint',fn(typevar(a),cprint)),
		                  ('type',fn(typevar(a), str)),
		                  (+,fn(tuple([int,int]),int)),
		                  (-,fn(tuple([int,int]),int)),
		                  (*,fn(tuple([int,int]),int)),
		                  ('div',fn(tuple([int,int]),int))],
		           Expression,Type).

	**Fig. 8.9** The Prolog Type Environment

Integers, Strings, and Boolean Constants
-----------------------------------------
.. container:: figboxcenter

	.. code-block:: prolog

		typecheckExp(_,int(_),int).
		typecheckExp(_,bool(_),bool).
		typecheckExp(_,str(_),str).


	**Fig. 8.10** Constant Types



**BoolCon**

	.. math::
		\frac{}{\varepsilon\vdash bool(v) : bool}

**IntCon**

	.. math::
		\frac{}{\varepsilon\vdash int(v) : int}

**StringCon**

	.. math::
		\frac{}{\varepsilon\vdash str(v) : str}




Example 8.1
=============

.. code-block:: text

	Typechecking is commencing...
	Here is the AST
	int(5)
	val it : int
	The program passed the typechecker.



List and Tuple Constants
--------------------------

	.. math::

		[ 6, 5, 4 ] & : int~~list \\
		( "hi", true, 6) & : str * bool * int


.. code-block:: prolog

	typecheckExp(Env,listcon(L),listOf(T)) :- typecheckList(Env,L,T).
	typecheckExp(Env,tuple(L),tuple(T)) :- typecheckTuple(Env,L,T).



.. code-block:: prolog

	listOf(int)
	tuple([str,bool,int])


**ListCon**

	.. math::
	  & \forall i~~1\leq i \leq n, n \geq 0\\
	  & \frac{\varepsilon\vdash e_i:\alpha}{\varepsilon\vdash [e_1,e_2,...,e_n] : \alpha~~list}



**TupleCon**

	.. math::
	  & \forall ~~1\leq i \leq n, n \geq 0\\
	  & \frac{\varepsilon\vdash e_i:\alpha_i}{\varepsilon\vdash (e_1,e_2,...,e_n) : \times_{i=1}^n \alpha_i}


Example 8.2
==============

.. code-block:: text

	Typechecking is commencing...
	Here is the AST
	listcon([int(1),int(2),int(3),int(4)])
	val it : int list
	The program passed the typechecker.

Identifiers
--------------
.. container:: figboxcenter

	.. code-block:: prolog
		:linenos:

		exists(Env,Name) :-
		    member((Name,_),Env), !.
		find(Env,Name,Type) :-
		    member((Name,Type),Env), !.
		find(Env,Name,Type) :-
		    writeMsg(['Failed to find ',
		    Name,' with type ',Type,
		    ' in environment : ']), print(Env), nl,
		    throw(typeerror('unbound identifier')).
		typecheckExp(Env,id(Name),Type) :-
		    find(Env,Name,Type).

	**Fig. 8.11** Environment Lookup Predicates


**Identifier**

	.. math::

		\frac{}{\varepsilon[id \mapsto \alpha]\vdash id : \alpha}


Example 8.3
==============

.. code-block:: text

	Typechecking is commencing...
	Here is the AST
	id(println)
	val it : 'a -> unit
	The program passed the typechecker.


Function Application
-----------------------

.. code-block:: sml

	println 6




**FunApp**

   .. math::
      \frac{\varepsilon\vdash e_1 : \alpha\rightarrow\beta, ~~ \alpha'\rightarrow\beta':inst(\alpha\rightarrow\beta),~~ \varepsilon\vdash e_2 : \alpha_{e2}, ~~ \alpha' : inst(\alpha_{e2})}
           {\varepsilon\vdash e_1 e_2 : \beta'}



.. container:: figboxcenter

	.. code-block:: prolog
		:linenos:

		instanceOfList(Env,[],[],Env).
		instanceOfList(Env,[H|T],[G|S],NewEnv) :-
		    instanceOf(Env,H,G,Env1), instanceOfList(Env1,T,S,NewEnv).
		instanceOf(Env,A,A,Env) :- var(A), !.
		instanceOf(Env,A,A,Env) :- simple(A), !.
		instanceOf(Env,fn(A,B), fn(AInst,BInst),Env2) :-
		    instanceOf(Env,A,AInst,Env1), instanceOf(Env1,B,BInst,Env2), !.
		instanceOf(Env,listOf(A),listOf(B),NewEnv) :- instanceOf(Env,A,B,NewEnv), !.
		instanceOf(Env,ref(A),ref(B),NewEnv) :- instanceOf(Env,A,B,NewEnv), !.
		instanceOf(Env,tuple(L),tuple(M),NewEnv) :- instanceOfList(Env,L,M,NewEnv), !.
		instanceOf(Env,typevar(A),B,Env) :- exists(Env,A), find(Env,A,B), !.
		instanceOf(Env,typevar(A),B,[(A,B)|Env]) :- !.
		instanceOf(_,A,B,_) :-
		    print('Type Error: Type '), printType(B,_),
		    print(' is not an instance of '), printType(A,_), nl,
		    throw(typeerror('type mismatch')), !.
		inst(X,Y) :- instanceOf([],X,Y,_).

	**Fig. 8.12** The Instantiation Operator


.. container:: figboxcenter

	.. code-block:: prolog

		typecheckExp(Env,apply(Exp1,Exp2),ITT) :-
			typecheckExp(Env,Exp1,fn(FT,TT)), typecheckExp(Env,Exp2,Exp2Type),
			inst(Exp2Type,Exp2TypeInst), catch(inst(fn(FT,TT), fn(Exp2TypeInst,ITT)),_,
			printApplicationErrorMessage(Exp1,fn(FT,TT),Exp2,Exp2Type,ITT)), !.

	**Fig. 8.13** Function Application Type Inference



Instantiation
===============


Example 8.4
==============


.. math::
	\frac{\varepsilon\vdash println : \alpha\rightarrow unit,~~~
	                int\rightarrow unit:inst(\alpha\rightarrow unit),~~~\varepsilon\vdash 6 : int}
	     { \varepsilon\vdash println~6 : unit}

Let Expressions
-----------------

Example 8.5
=============

	.. math::
		\varepsilon_1 & = [x\mapsto\alpha\rightarrow\beta,~y\mapsto int,~z\mapsto\alpha\times\beta]\\
		\varepsilon_2 & = [u\mapsto\alpha\times\beta\rightarrow\beta,~y\mapsto\ bool]\\
		\varepsilon_2\oplus\varepsilon_1 &= [u\mapsto\alpha\times\beta\rightarrow\beta,~y\mapsto\ bool]\oplus[x\mapsto\alpha\rightarrow\beta,~y\mapsto int,~z\mapsto\alpha\times\beta]\\
		& = [u\mapsto\alpha\times\beta\rightarrow\beta,~y\mapsto\ bool,x\mapsto\alpha\rightarrow\beta,~y\mapsto int, ~z\mapsto\alpha\times\beta]



	.. math::

		\varepsilon\vdash dec \Rightarrow \varepsilon_{dec}


**Let**

	.. math::

	  \frac{\varepsilon\vdash dec\Rightarrow\varepsilon_{dec},~~\varepsilon_{dec}\oplus\varepsilon\vdash e_{sequence}:\beta}{\varepsilon\vdash let~dec~in~e_{sequence}~end:\beta}


**ValDec**

    .. math::

      \frac{pat:\alpha\Rightarrow\varepsilon_{pat},~~\varepsilon\vdash e:close(\alpha)}{\varepsilon\vdash val~pat=e\Rightarrow\varepsilon_{pat}}


**ValRecDec**

    .. math::

      \frac{[id:\alpha]\oplus\varepsilon\vdash e:\alpha}{\varepsilon\vdash val~rec~id=e\Rightarrow[ id:close(\alpha)]}


**FunDecs**

	.. math::

	   &  \forall i~1 \leq i \leq n, \forall j~1 < j \leq n,~~n \geq 1,\\
	   & \frac{[id_1\mapsto\alpha_1\rightarrow\beta_1~\{,~id_j\mapsto\alpha_j\rightarrow\beta_j\}]\oplus\varepsilon\vdash id_i~matches_i:\alpha_i\rightarrow\beta_i}{\varepsilon\vdash f\!un~id_1~matches_1~\{and~id_j~matches_j\}\Rightarrow[id_1\mapsto close(\alpha_1\rightarrow\beta_1)~\{,~id_j\mapsto close(\alpha_j\rightarrow\beta_j)\}]}



Patterns
-----------

**IntPat**

	.. math::

	  	\frac{}{integer\_constant:int \Rightarrow [~]}

**BoolPat**

	.. math::

	  	& \frac{}{true:bool \Rightarrow [~]} \\
	  	& \frac{}{false:bool \Rightarrow [~]}

**StrPat**

	.. math::

	  	\frac{}{string\_constant:str \Rightarrow [~]}

**NilPat**

	.. math::

		\frac{}{nil:\alpha~list\Rightarrow[~]}

**ConsPat**

	.. math::

		\frac{pat_1:\alpha\Rightarrow  \varepsilon_{pat_1},~~pat_2:\alpha~list\Rightarrow \varepsilon_{pat_2}}
		     {pat_1::pat_2 : \alpha~list\Rightarrow \varepsilon_{pat_1}+\varepsilon_{pat_2}}

**TuplePat**

	.. math::
		&  \forall i~1 \leq i \leq n, n \geq 0\\
		& \frac{pat_i : \alpha_i \Rightarrow \varepsilon_{pat_i}}
		       {(pat_1,pat_2,...,pat_n): \times_{i=1}^{n}\alpha_i\Rightarrow \sum^{n}_{i=1}\varepsilon_{pat_i}}

**ListPat**

	.. math::
		&  \forall i~1 \leq i \leq n, n \geq 0\\
		& \frac{pat_i : \alpha \Rightarrow \varepsilon_{pat_i}}
		       {[pat_1,pat_2,...,pat_n]: \alpha~list\Rightarrow \sum^{n}_{i=1}\varepsilon_{pat_i}}


.. container:: figboxcenter

	.. code-block:: sml

		let
		  val (x,y)::L = [(1,2),(3,4)]
		in
		  println x
		end

	**Fig. 8.14** Pattern Matching

**IdPat**

	.. math::

	  	\frac{}{id:\alpha\Rightarrow[id\mapsto\alpha]}


Example 8.6
============


.. code-block:: text

	letdec(
	  bindval(infixpat(::,tuplepat([idpat(x),idpat(y)]),idpat(L)),
	    listcon([tuple([int(1),int(2)]),tuple([int(3),int(4)])])),
	  [apply(id(println),id(x))])
	val (x,y)::L : (int * int) list
	val it : unit
	The program passed the typechecker.


.. math::

	\dfrac{
	  (2) \varepsilon\vdash val~(x,y)::L = [(1,2),(3,4)]\Rightarrow\varepsilon_{dec}
	  ~~~
      (3) \varepsilon_{dec}\oplus\varepsilon\vdash println~x : unit
	}{
	  (1)\varepsilon\vdash let~val~(x,y)::L = [(1,2),(3,4)]~in~println~x~end : unit
	}(Let)

	\varepsilon_{dec} =[x\mapsto int, y\mapsto int, L\mapsto int * int~list]

To prove (2):

.. math::
	\dfrac{
	   (4) (x,y)::L : int\times int~list\Rightarrow\varepsilon_{dec}
	   ~~~
	   (5) \varepsilon\vdash [(1,2),(3,4)] : int\times int~list
	}{
	   (2) \varepsilon\vdash val~(x,y)::L = [(1,2),(3,4)]\Rightarrow\varepsilon_{dec}
	}(ValDec)

To prove (4):

.. math::
	\dfrac{
	   (6) (x,y) : int \times int \Rightarrow [x\mapsto int, y\mapsto int]
	   ~~~
	   (7) L : int\times int~list \Rightarrow[L\mapsto int\times int~list]
	}{
	   (4) (x,y)::L : int\times int~list\Rightarrow\varepsilon_{dec}
	}(ConsPat)

To prove (6):

.. math::
	\dfrac{
	   (8) x : int \Rightarrow[x\mapsto int]
	   ~~~
	   (9) y : int \Rightarrow[y\mapsto int]
	}{
	   (6) (x,y) : int \times int \Rightarrow [x\mapsto int, y\mapsto int]
	}(TuplePat)

Premises (7), (8), and (9) are true by virtue of the *IdPat* inference rule. Considering (5):

.. math::
	\dfrac {
	  (10)\varepsilon\vdash (1,2):int\times int
	  ~~~
	  (11)\varepsilon\vdash (3,4):int\times int
	}{
	 (5) \varepsilon\vdash [(1,2),(3,4)] : int\times int~list
	}(ListCon)

Considering (10) and a similar argument for (11):

.. math::
	\dfrac{
      (12)\varepsilon\vdash 1:int
      ~~~
      (13)\varepsilon\vdash 2:int
	}{
	  (10)\varepsilon\vdash (1,2):int\times int
	}(TupleCon)

Both (12) and (13) are true by the *IntCon* rule. A similar argument holds for (11). The proof nears completion by proving (3):

.. math::
	\dfrac{
      (14) \varepsilon_{dec}\oplus\varepsilon\vdash println : \alpha\rightarrow unit
      ~~~
      int\rightarrow unit : inst(\alpha\rightarrow unit)
      ~~~
      (15) \varepsilon_{dec}\oplus\varepsilon\vdash x : int
	} {
      (3) \varepsilon_{dec}\oplus\varepsilon\vdash println~x : unit
	}(FunApp)

Both (14) and (15) are true by the *Identifier* rule concluding the proof of the type correctness of this program.

.. container:: figboxcenter

	.. code-block:: sml

		let val x = 5
		    val y = 6
		in
		  println (x + y)
		end

	**Fig. 8.15** test10.sml

.. container:: exercise

  **Practice 8.1**

  Prove that the program given in figure 8.13 is correctly typed. The abstract syntax for this program is provided here.

	.. code-block:: prolog

		  letdec(bindval(idpat('x'),int('5')),
		   [letdec(bindval(idpat('y'),int('6')),
		       [apply(id('println'),apply(id('+'),tuple([id('x'),id('y')])))])
		   ]).

  :ref:`You can check your answer(s) here.<exercise8-1>`

.. container:: exercise

  **Practice 8.2**


  Minimally, what must the type environment contain to correctly type check the program in figure 8.15.

  :ref:`You can check your answer(s) here.<exercise8-2>`

Matches
------------

.. container:: figboxcenter

	.. code-block:: sml

		let fun f(0,y) = y
		      | f(x,y) = g(x,x*y)
		    and g(x,y) = f(x-1,y)
		in
		  println (f(10,5))
		end


	**Fig. 8.16** test11.sml

**Matches**

	.. math::
		&  \forall i~1 \leq i \leq n, \forall j~1 < j \leq n,~n \geq 1\\
		& \frac{\varepsilon\vdash id:\alpha\rightarrow\beta,~~pat_i:\alpha\Rightarrow
		   \varepsilon_{pat_i},~~\varepsilon_{pat_i}\oplus\varepsilon\vdash e_i:\beta}
		       {\varepsilon\vdash id~pat_1=e_1\{|~id~pat_j=e_j\}:\alpha\rightarrow\beta}

or

	.. math::
		&  \forall i~1 \leq i \leq n, \forall j~1 < j \leq n,~n \geq 1\\
		& \frac{\varepsilon\vdash id:\alpha\rightarrow\beta,~~pat_i:\alpha\Rightarrow
		   \varepsilon_{pat_i},~~\varepsilon_{pat_i}\oplus\varepsilon\vdash e_i:\beta}
		       {\varepsilon\vdash id~pat_1=>e_1\{|~pat_j=>e_j\}:\alpha\rightarrow\beta}



Example 8.7
=============

.. code-block:: prolog

	letdec(
	  funmatches(
	    [funmatch(f,
	       [match(tuplepat([intpat(0),idpat(y)]),id(y)),
	        match(tuplepat([idpat(x),idpat(y)]),apply(id(g),
	           tuple([id(x),apply(id(*),tuple([id(x),id(y)]))])))]),
	     funmatch(g,
	       [match(tuplepat([idpat(x),idpat(y)]),
	          apply(id(f),tuple([apply(id(-),tuple([id(x),int(1)])),id(y)])))])]),
	  [apply(id(println),apply(id(f),tuple([int(10),int(5)])))])


Anonymous Functions
---------------------
.. container:: figboxcenter

	.. code-block:: sml

		(fn x => x+1)


	**Fig. 8.17** Anonymous Function

**AnonFun**
	.. math::

	   \frac{[id\mapsto\alpha\rightarrow\beta]\oplus\varepsilon\vdash id~matches:\alpha\rightarrow\beta}
	        {\varepsilon\vdash fn~id~matches:\alpha\rightarrow\beta}


Example 8.8
=============

	.. code-block:: prolog

		func(anon@0,[match(idpat(x),apply(id(+),tuple([id(x),int(1)])))])


	.. math::

	   \frac{[anon@0\mapsto int\rightarrow int]\oplus\varepsilon\vdash anon@0~x => x+1:int\rightarrow int}
	        {\varepsilon\vdash fn~anon@0~x => x+1 :int\rightarrow int}


.. container:: exercise

  **Practice 8.3**


  Provide a complete proof that the program in figure 8.17 is correctly typed.

  :ref:`You can check your answer(s) here.<exercise8-3>`



Sequential Execution
----------------------

**Sequence**

	.. math::
		&  \forall i~1 \leq i \leq n, \forall j~1 < j \leq n,~n \geq 1\\
		&  \frac{\varepsilon\vdash e_i : \alpha_i}
		        {\varepsilon\vdash e_1 \{ ; e_j\} : \alpha_n}



If-Then and While-Do
------------------------

**IfThen**

	.. math::
	  \frac{\varepsilon\vdash e_1:bool,~~\varepsilon\vdash e_2:\alpha,~~~\varepsilon\vdash e_3:\alpha}{\varepsilon\vdash i\!f~e_1~then~e_2~else~e_3 : \alpha}

**WhileDo**

	.. math::
	  \frac{\varepsilon\vdash e_1:bool,~~\varepsilon\vdash e_2:\alpha}{\varepsilon\vdash while~e_1~do~e_2 : \alpha}


.. container:: figboxcenter

	.. code-block:: prolog

		typecheckExp(Env,ifthen(Exp1,Exp2,Exp3), RT) :-
		    typecheckExp(Env,Exp1,bool), typecheckExp(Env,Exp2,RT), typecheckExp(Env,Exp3,RT), !.
		typecheckExp(Env,ifthen(Exp1,Exp2,Exp3), _) :-
		    typecheckExp(Env,Exp1,bool), typecheckExp(Env,Exp2,ThenType), typecheckExp(Env,Exp3,ElseType),
		    print('Error: Result types of then and else expressions must match.'), nl,
		    print('Then Expression type is: '), printType(ThenType,_), nl,
		    print('Else Expression type is: '), printType(ElseType,_), nl,
		    throw(typeerror('result type mismatch in if-then-else expression')).
		typecheckExp(Env,ifthen(Exp1,_,_), _) :-
		    typecheckExp(Env,Exp1,Exp1Type), Exp1Type \= bool,
		    print('Error: Condition of if then expression must have bool type.'), nl,
		    print('Condition Expression type was: '), printType(Exp1Type,_), nl,
		    throw(typeerror('type not bool in if-then-else expression condition')).


	**Fig. 8.18** If-Then Prolog Code




Exception Handling
-----------------------

**Handler**

	.. math::
		\frac{\varepsilon\vdash e:\alpha, ~~ [handle@\mapsto~exn\rightarrow\alpha]\oplus\varepsilon\vdash handle@~matches : exn\rightarrow\alpha}
		     {\varepsilon\vdash e~handle~matches : \alpha}



Chapter Summary
-------------------



Review Questions
-------------------

#. What appears above and below the line in a type inference rule?
#. Why don't infix operators appear in the abstract syntax of programs handled by the type checker?
#. What does *typevar* represent in figure 8.6?
#. What does *typeerror* represent in figure 8.6?
#. What does the *type* of the list [("hello",1,true)] look like as a Prolog term?
#. What is the type environment?
#. Give an example of the use of the overlay operator.
#. What pattern(s) are used in this let expression?

   .. code-block:: sml

   		let val (x,y,z) = ("hello",1,true) in println x end

   What is the pattern as a Prolog term?
#. Give an example where the *Sequence* rule might be used to infer a type.
#. Give a short example of where the *Handler* rule might be used to infer a type.

Exercises
-----------

#. The following program does not compile correctly or typecheck
   correctly using the mlcomp compiler and type inference system.
   However, it is a valid Standard ML program. Modify both the mlcomp
   compiler and type checker to correctly compile and infer its type.
   This program is included in the compiler project as test20.sml.

   ::

       let val [(x,y,z)] = [(l+s+s2{h}ellop{,}1,true)] in println x end

   Output from the type checker should appear as follows.

   ::

       Typechecking is commencing...
       Here is the AST
       letdec(bindval(listpat([tuplepat([idpat(x),idpat(y),idpat(z)])]),
              listcon([tuple([str("hello"),int(1),bool(true)])])),
              [apply(id(println),id(x))])
       val [(x,y,z)] : (str * int * bool) list
       val it : unit
       The program passed the typechecker.

#. Implement the Prolog type predicates to get the following program to
   type check successully. This program is test14.sml in the mlcomp
   compiler project. This will involve writing type checking predicates
   for matching, boolean patterns, integer patterns, and sequential
   execution.

   .. code:: sml

       let fun f(true,x) = (println(x); g(x-1))
             | f(false,x) = g(x-1)
           and g 0 = ()
             | g x = f(true,x)
       in
              g(10)
       end

   Output from the type checker should appear as follows.

   ::

       Typechecking is commencing...
       Here is the AST
       letdec(funmatches([funmatch(f,[match(tuplepat([boolpat(true),idpat(x)]),
              expsequence([apply(id(println),id(x)),apply(id(g),apply(id(-),
              tuple([id(x),int(1)])))])),match(tuplepat([boolpat(false),idpat(x)]),
              apply(id(g),apply(id(-),tuple([id(x),int(1)]))))]),funmatch(g,[match(intpat(0),
              tuple([])),match(idpat(x),apply(id(f),tuple([bool(true),id(x)])))])]),
              [apply(id(g),int(10))])
       val f = fn : bool * int -> unit
       val g = fn : int -> unit
       val it : unit
       The program passed the typechecker.

#. Implement enough of the type checker to get test12.sml to type check
   correctly. This will mean writing the *WhileDo* inference rule as a
   Prolog predicate, implementing the *Match* rule’s predicate called
   *typecheckMatch*, and the type inference predicate for sequential
   execution named *typecheckSequence* as defined in the *Sequence*
   rule. The code for test12.sml is given here for reference.

   .. code:: sml

       let val zero = 0
           fun fib n =
           let val i = ref zero
               val current = ref 0
               val next = ref 1
               val tmp = ref 0
           in
             while !i < n do (
               tmp := !next + !current;
               current := !next;
               next := !tmp;
               i := !i + 1
             );
             !current
           end
           val x = Int.fromString(input(l+s+s2{"lease enter an integer: "))
           val r = fib(x)
       in
         print l+s+s2{F}ib(p{;}
         print x;
         print l+s+s2{)} is p{;}
         println r
       end

   Output from the type checker should appear as follows.

   ::

       Typechecking is commencing...
       Here is the AST
       letdec(bindval(idpat(zero),int(0)),[letdec(funmatches([funmatch(fib,
          [match(idpat(n),letdec(bindval(idpat(i),apply(id(ref),id(zero))),
          [letdec(bindval(idpat(current),apply(id(ref),int(0))),
          [letdec(bindval(idpat(next),apply(id(ref),int(1))),
          [letdec(bindval(idpat(tmp),apply(id(ref),int(0))),
          [whiledo(apply(id(<),tuple([apply(id(!),id(i)),id(n)])),
          expsequence([apply(id(:=),tuple([id(tmp),apply(id(+),tuple([apply(id(!),id(next)),
          apply(id(!),id(current))]))])),apply(id(:=),tuple([id(current),apply(id(!),
          id(next))])),apply(id(:=),tuple([id(next),apply(id(!),id(tmp))])),apply(id(:=),
          tuple([id(i),apply(id(+),tuple([apply(id(!),id(i)),int(1)]))]))])),apply(id(!),
          id(current))])])])]))])]),[letdec(bindval(idpat(x),apply(id(Int.fromString),
          apply(id(input),str("Please enter an integer: ")))),
          [letdec(bindval(idpat(r),apply(id(fib),id(x))),[apply(id(print),str("Fib(")),
          apply(id(print),id(x)),apply(id(print),str(") is ")),apply(id(println),id(r))])])])])
       val zero : int
       val i : int ref
       val current : int ref
       val next : int ref
       val tmp : int ref
       val fib = fn : int -> int
       val x : int
       val r : int
       val it : unit
       The program passed the typechecker.

#. Add support to the type checker to correctly infer the types of
   *case* expressions in Small. The following program should type check
   correctly once this project is completed. This test is in test15.sml
   in the mlcomp compiler project. This will involve writing code to
   correctly type check matches according to the *Match* rule. If case
   statments are not yet implemented in the compiler, support must be
   added to the compiler to parse *case* expressions, build an AST for
   them, and write their AST to the *a.term* file.

   .. code:: sml

       let val x = 4
       in
         println
           (case x of
             1 => "hello"
           | 2 => "how"
           | 3 => "are"
           | 4 => "you")
       end

   Output from the type checker should appear as follows.

   ::

       Typechecking is commencing...
       Here is the AST
       letdec(bindval(idpat(x),int(6)),[apply(id(println),caseof(id(x),
              [match(intpat(1),str("hello")),match(intpat(2),str("how")),
              match(intpat(3),str("are")),match(intpat(4),str("you"))]))])
       val x : int
       val it : unit
       The program passed the typechecker.

#. Add support to the type checker to correctly infer the types for
   test7.sml. The code is provided below for reference. Support will
   need to be added to infer the types of anonymous functions defined in
   the rule *AnonFun*, matching defined in the rule *Matches*, and the
   *ConsPat* rule.

   .. code:: sml

       let fun append nil L = L
             | append (h::t) L = h :: (append t L)
           fun appendOne x = (fn nil => (fn L => L)
                               | h::t => (fn L => h :: (appendOne t L))) x
       in
         println(append [1,2,3] [4]);
         println(appendOne [1,2,3] [4])
       end

   Output from the type checker should appear as follows.

   ::

       Typechecking is commencing...
       Here is the AST
       letdec(funmatches([funmatch(append,[match(idpat(v0),func(anon@3,
       [match(idpat(v1),apply(func(anon@2,[match(tuplepat([idpat(nil),idpat(L)]),id(L)),
       match(tuplepat([infixpat(::,idpat(h),idpat(t)),idpat(L)]),apply(id(::),
       tuple([id(h),apply(apply(id(append),id(t)),id(L))])))]),
       tuple([id(v0),id(v1)])))]))])]),[letdec(funmatches([funmatch(appendOne,
       [match(idpat(x),apply(func(anon@6,[match(idpat(nil),func(anon@4,
       [match(idpat(L),id(L))])),match(infixpat(::,idpat(h),idpat(t)),
       func(anon@5,[match(idpat(L),apply(id(::),tuple([id(h),apply(apply(id(appendOne),id(t)),
       id(L))])))]))]),id(x)))])]),[apply(id(println),apply(apply(id(append),
       listcon([int(1),int(2),int(3)])),listcon([int(4)]))),apply(id(println),
       apply(apply(id(appendOne),listcon([int(1),int(2),int(3)])),listcon([int(4)])))])])
       val append = fn : 'a list -> 'a list -> 'a list
       val appendOne = fn : 'a list -> 'a list -> 'a list
       val it : unit
       The program passed the typechecker.

#. Add support for type inference for recursive bindings. The following
   program, saved as test19.sml in the Small compiler project, is a
   valid program with a recursive binding. It will type check correctly
   if the *ValRecDec* type inference rule is implemented. Write the code
   to get this program to pass the type checker as a valid program.

   .. code:: sml

       let val rec f = (fn 0 => 1
                         | x => x * (f (x-1)))
       in
          println(f 5)
       end

   Output from the type checker should appear as follows.

   ::

       Typechecking is commencing...
           Here is the AST
           letdec(bindvalrec(idpat(f),func(anon@0,[match(intpat(0),int(1)),match(idpat(x),
              apply(id(*),tuple([id(x),apply(id(f),apply(id(-),tuple([id(x),int(1)])))])))])),
              [apply(id(println),apply(id(f),int(5)))])
           val f = fn : int -> int
           val it : unit
           The program passed the typechecker.

#. Currently the type checker allows duplicate identifiers in compound
   patterns like listPat and tuplePat. Standard ML does not allow
   duplicate identifiers in patterns. The type checker uses the *append*
   predicate to combine pattern binding environments. This is not good
   enough. Find the locations in the type checker where pattern
   environments are incorrectly appended and rewrite this code to
   enforce that all identifiers within a pattern must be unique. If not,
   you should print an error message like *“Error: duplicate variable in
   pattern(s): x”* to indicate the problem and typechecking should end
   with an error.

#. Currently, the abstract syntax and parser of *Small* includes support
   for the wildcard pattern in pattern matching, but the type checker
   does not support it. Add support for wildcard patterns, write a test
   program, and test the compiler and type checker. Be sure to write a
   type inference rule for wildcard patterns first.

#. Currently, the abstract syntax and parser of *Small* includes support
   for the *as* pattern in pattern matching, but the type checker does
   not support it. Add support for *as* patterns, write a test program,
   and test the compiler and type checker. The *as* pattern comes up
   when you write a pattern like *L as h::t* which assigns *L* as a
   pattern that represents the same value as the compound pattern of
   *h::t*. Be sure to write a type inference rule for *as* patterns
   first.


Solutions to Practice Problems
----------------------------------

.. _exercise8-1:

Solution to Practice Problem 8.1
================================

The complexity of append is O(n) in the length of the first list.

.. _exercise8-2:

Solution to Practice Problem 8.2
================================

Minimally the environment must contain *println* bound to a function
type of :math:`\alpha\rightarrow unit` and the *+* function bound to a
function type of :math:`int\times int \rightarrow int`.

.. _exercise8-3:

Solution to Practice Problem 8.3
================================

The *AnonFun* rule is applied first which requires the *Matches* rule be
applied. The *Matches* rule requires the use of the *IdPat* rule and the
*FunApp* rule. Finally, the *IntCon* rule is needed to complete the
proof.
