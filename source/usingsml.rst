.. _usingsml:

=================================================
Compiling Standard ML
=================================================


.. container:: figboxcenter

   .. figure:: mlcalccomp.png

      Structure of MLComp

------------
ML-lex
------------


.. code-block:: sml

  User declarations
  %%
  ML-lex definitions
  %%
  Token Rules



.. code-block:: sml

  reg_exp => (return_value);



Example 6.1
===========

  .. container:: figbox

    .. code-block:: text
      :linenos:

      (* mlcomp.lex -- lexer spec *)
      type pos = int
      type svalue = Tokens.svalue
      type ('a, 'b) token = ('a, 'b) Tokens.token
      type lexresult = (svalue, pos) token
      val pos = ref 1
      val error = fn x => TextIO.output(TextIO.stdErr, x ^ "\n")
      val eof = fn () => Tokens.EOF(!pos, !pos)
      fun countnewlines s =
          let val lst = explode s
              fun count (c:char) nil = 0
                | count c (h::t) =
                  let val tcount = count c t
                  in
                    if c = h then 1+tcount else tcount
                  end
          in
            pos:= (!pos) + (count #"\n" lst)
          end
      %%
      %header (functor mlcompLexFun(structure Tokens : mlcomp_TOKENS));
      alpha=[A-Za-z];
      alphanumeric=[A-Za-z0-9_\.];
      digit=[0-9];
      ws=[\ \t];
      dquote=[\"];
      squote=[\'];
      anycharbutquote=[^"];
      anychar=[.];
      pound=[\#];
      tilde=[\~];
      period=[\.];
      %%
      \(\*([^*]|[\r\n]|(\*+([^*\)]|[\r\n])))*\*+\) => (countnewlines yytext; lex());
      \n  => (pos := (!pos) + 1; lex());
      {ws}+  => (lex());
      "+"  => (Tokens.Plus(!pos,!pos));
      "*"  => (Tokens.Times(!pos,!pos));
      "-"  => (Tokens.Minus(!pos,!pos));
      "@"  => (Tokens.Append(!pos,!pos));
      "=" => (Tokens.Equals(!pos,!pos));
      "("  => (Tokens.LParen(!pos,!pos));
      ")"  => (Tokens.RParen(!pos,!pos));
      "[" => (Tokens.LBracket(!pos,!pos));
      "]" => (Tokens.RBracket(!pos,!pos));
      "::" => (Tokens.ListCons(!pos,!pos));
      "," => (Tokens.Comma(!pos,!pos));
      ";" => (Tokens.Semicolon(!pos,!pos));
      "_" => (Tokens.Underscore(!pos,!pos));
      "=>" => (Tokens.Arrow(!pos,!pos));
      "|" => (Tokens.VerticalBar(!pos,!pos));
      ">" => (Tokens.Greater(!pos,!pos));
      "<" => (Tokens.Less(!pos,!pos));
      ">=" => (Tokens.GreaterEqual(!pos,!pos));
      "<=" => (Tokens.LessEqual(!pos,!pos));
      "<>" => (Tokens.NotEqual(!pos,!pos));
      "!" => (Tokens.Exclaim(!pos,!pos));
      ":=" => (Tokens.SetEqual(!pos,!pos));


      {tilde}?{digit}+  => (Tokens.Int(yytext,!pos,!pos));
      {pound}{dquote}{anychar}{dquote} => (Tokens.Char(yytext,!pos,!pos));
      {dquote}{anycharbutquote}*{dquote} => (Tokens.String(yytext,!pos,!pos));
      {alpha}{alphanumeric}*=>
         (let val tok = String.implode (List.map (Char.toLower)
                   (String.explode yytext))
          in
            if      tok="let" then Tokens.Let(!pos,!pos)
            else if tok="val" then Tokens.Val(!pos,!pos)
            else if tok="in" then Tokens.In(!pos,!pos)
            else if tok="end" then Tokens.End(!pos,!pos)
            else if tok="if" then Tokens.If(!pos,!pos)
            else if tok="then" then Tokens.Then(!pos,!pos)
            else if tok="else" then Tokens.Else(!pos,!pos)
            else if tok="div" then Tokens.Div(!pos,!pos)
            else if tok="mod" then Tokens.Mod(!pos,!pos)
            else if tok="fn" then Tokens.Fn(!pos,!pos)
            else if tok="while" then Tokens.While(!pos,!pos)
            else if tok="do" then Tokens.Do(!pos,!pos)
            else if tok="and" then Tokens.And(!pos,!pos)
            else if tok="rec" then Tokens.Rec(!pos,!pos)
            else if tok="fun" then Tokens.Fun(!pos,!pos)
            else if tok="as" then Tokens.As(!pos,!pos)
            else if tok="handle" then Tokens.Handle(!pos,!pos)
            else if tok="raise" then Tokens.Raise(!pos,!pos)
            else if tok="true" then Tokens.True(!pos,!pos)
            else if tok="false" then Tokens.False(!pos,!pos)
            else Tokens.Id(yytext,!pos,!pos)
          end);
      .  => (error ("error: bad token "^yytext); lex())

    **Fig. 6.2, 6.3, 6.4** mlcomp.lex


.. container:: exercise

  **Practice 6.1**

  Given the ML-lex specification in example~, what more would have to be added to allow expressions like this to be correctly tokenized by the scanner? What new tokens would have to be recognized? How would you modify the specification to accept these tokens?

  .. code-block:: text

    case x of
       1 => "hello"
     | 2 => "how"
     | 3 => "are"
     | 4 => "you"

  :ref:`You can check your answer(s) here.<exercise6-1>`


-----------------------------------------
The Small AST Definition
-----------------------------------------

.. container:: figboxcenter

  .. code-block:: sml
      :linenos:

      structure MLAS =
      struct

      datatype
        exp = int of string
            | ch of string
            | str of string
            | boolval of string
            | id of string
            | listcon of exp list
            | tuplecon of exp list
            | apply of exp * exp
            | infixexp of string * exp * exp
            | expsequence of exp list
            | letdec of dec * (exp list)
            | raisexp of exp
            | handlexp of exp * match list
            | ifthen of exp * exp * exp
            | whiledo of exp * exp
            | func of int * match list
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
            | funmatches of
                   (string * match list) list
      end

  **Fig. 6.5** mlast.sml


.. container:: exercise

  **Practice 6.2**

  How would you modify the abstract syntax so expressions like the one below could be represented?

  .. code-block:: text

    case x of
       1 => "hello"
     | 2 => "how"
     | 3 => "are"
     | 4 => "you"

  :ref:`You can check your answer(s) here.<exercise6-2>`

-------------
Using ML-yacc
-------------


.. code-block:: text

  User declarations
  %%
  ML-yacc definitions
  %%
  Rules


Example 6.3
===========

  .. container:: figbox

    .. code-block:: text
      :linenos:

      open MLAS;
      val idnum = ref 0
      fun nextIdNum() =
        let val x = !idnum
        in
          idnum := !idnum + 1;
          x
        end
      exception emptyDecList;
      exception argumentMismatch;
      fun uncurryIt nil = raise emptyDecList
        | uncurryIt (L as ((name,patList,exp)::t)) =
          let fun len nil = raise argumentMismatch
                | len [(n,p,e)] = length(p)
                | len ((n,p,e)::t) =
                  let val size = length(p)
                  in
                    if size = len t then size else
                      (TextIO.output(TextIO.stdOut,
                      "Syntax Error: Number of arguments does not match in function "
                      ^name^"\n");
                       raise argumentMismatch)
                  end
              val tupleList = List.map (fn x => "v"^Int.toString(nextIdNum())) patList
           in
             len(L); (* just check the parameter list sizes so all patterns have same length *)
             (name,[match(idpat(hd(tupleList)),
                       List.foldr (fn (x,y) => func(nextIdNum(),[match(idpat(x), y)]))
                          (apply (func(nextIdNum(),
                                  List.map (fn (n,p,e) => match(tuplepat(p),e)) L),
                                  tuplecon(List.map (fn x => id(x)) tupleList)))
                              (tl tupleList))])
           end
      fun makeMatchList (nil) = raise emptyDecList
        | makeMatchList (L as (name,pat,exp)::t) =
          (name, List.map (fn (n,p,e) =>
                     (if name <> n then (
                         TextIO.output(TextIO.stdOut,
                         "Syntax Error: Function definition with different names "
                         ^name^" and "^n^" not allowed.\n");
                         raise argumentMismatch)
                      else match(p,e))) L)
      %%
      %name mlcomp (* mlcomp becomes a prefix in functions *)
      %verbose
      %eop EOF
      %pos int
      %nodefault
      %pure (* no side-effects in actions *)
      %term EOF | LParen | RParen | Plus | Minus | Times | Div | Mod | Greater | Less
          | GreaterEqual | LessEqual | NotEqual | Append | ListCons | Negate | Comma
          | Semicolon | Underscore | Arrow | Equals | VerticalBar | LBracket | RBracket
          | Fun | As | Let | Val | In | End | If | Then | Else | Fn | While | Do | Handle
          | Raise | And | Rec | String of string | Char of string | Int of string | True
          | False | Id of string | SetEqual | Exclaim
      %nonterm Prog of exp | Exp of exp | Expressions of exp list | ExpSequence of exp list
             | MatchExp of match list | Pat of pat | Patterns of pat list
             | PatternSeq of pat list | Dec of dec | ValBind of dec
             | FunBind of (string * match list) list | FunMatch of (string * pat * exp) list
             | Con of exp | FuncExp of exp | DecSeq of dec list
             | CurriedFun of (string * pat list * exp) list
      %right SetEqual
      %left Plus Minus Append Equals NotEqual
      %left Times Div Mod Greater Less GreaterEqual LessEqual
      %right ListCons
      %right Exclaim
      %%
      Prog : Exp EOF                                             (Exp)
      Exp : Con                                                  (Con)
          | Id                                                   (id(Id))
          | FuncExp Exp                                          (apply(FuncExp,Exp))
          | Exclaim Exp                                          (apply(id("!"),Exp))
          | Id SetEqual FuncExp                                  (infixexp(":=",id(Id),FuncExp))
          | Exp Plus Exp                                         (infixexp("+",Exp1,Exp2))
          | Exp Minus Exp                                        (infixexp("-",Exp1,Exp2))
          | Exp Times Exp                                        (infixexp("*",Exp1,Exp2))
          | Exp Div Exp                                          (infixexp("div",Exp1,Exp2))
          | Exp Mod Exp                                          (infixexp("mod",Exp1,Exp2))
          | Exp Greater Exp                                      (infixexp(">",Exp1,Exp2))
          | Exp GreaterEqual Exp                                 (infixexp(">=",Exp1,Exp2))
          | Exp Less Exp                                         (infixexp("<",Exp1,Exp2))
          | Exp LessEqual Exp                                    (infixexp("<=",Exp1,Exp2))
          | Exp Equals Exp                                       (infixexp("=",Exp1,Exp2))
          | Exp NotEqual Exp                                     (infixexp("<>",Exp1,Exp2))
          | Exp Append Exp                                       (infixexp("@",Exp1,Exp2))
          | Exp ListCons Exp                                     (infixexp("::",Exp1,Exp2))
          | LParen Exp RParen                                    (Exp)
          | LParen Expressions RParen                            (tuplecon(Expressions))
          | LParen ExpSequence RParen                            (expsequence(ExpSequence))
          | LBracket Expressions RBracket                        (listcon(Expressions))
          | LBracket RBracket                                    (id("nil"))
          | Let DecSeq In ExpSequence End
                      (List.hd (List.foldr (fn (x,y) => [letdec(x,y)]) ExpSequence DecSeq))
          | Raise Exp                                            (raisexp(Exp))
          | Exp Handle MatchExp                                  (handlexp(Exp,MatchExp))
          | If Exp Then Exp Else Exp                             (ifthen(Exp1,Exp2,Exp3))
          | While Exp Do Exp                                     (whiledo(Exp1,Exp2))
          | Fn MatchExp                                          (func(nextIdNum(),MatchExp))
      FuncExp : Exp                                              (Exp)
      Expressions : Exp                                          ([Exp])
                  | Exp Comma Expressions                        (Exp::Expressions)
      ExpSequence : Exp                                          ([Exp])
                  | Exp Semicolon ExpSequence                    (Exp::ExpSequence)
      MatchExp : Pat Arrow Exp                                   ([match(Pat,Exp)])
               | Pat Arrow Exp VerticalBar MatchExp              (match(Pat,Exp)::MatchExp)
      Pat : Int                                                  (intpat(Int))
          | Char                                                 (chpat(Char))
          | String                                               (strpat(String))
          | True                                                 (boolpat("true"))
          | False                                                (boolpat("false"))
          | Underscore                                           (wildcardpat)
          | Id                                                   (idpat(Id))
          | Pat ListCons Pat                                     (infixpat("::",Pat1,Pat2))
          | LParen Pat RParen                                    (Pat)
          | LParen Patterns RParen                               (tuplepat(Patterns))
          | LBracket Patterns RBracket                           (listpat(Patterns))
          | LBracket RBracket                                    (idpat("nil"))
          | Id As Pat                                            (aspat(Id,Pat))
      Patterns : Pat                                             ([Pat])
               | Pat Comma Patterns                              (Pat::Patterns)
      PatternSeq : Pat                                           ([Pat])
                 | Pat PatternSeq                                (Pat::PatternSeq)
      Dec : Val ValBind                                          (ValBind)
          | Fun FunBind                                          (funmatches(FunBind))
      DecSeq : Dec                                               ([Dec])
             | Dec DecSeq                                        (Dec::DecSeq)
      ValBind : Pat Equals Exp                                   (bindval(Pat,Exp))
              | Rec Id Equals Exp                                (bindvalrec(idpat(Id),Exp))
      FunBind : FunMatch                                         ([makeMatchList FunMatch])
              | CurriedFun                                       ([uncurryIt CurriedFun])
              | FunBind And FunBind                              (FunBind1@FunBind2)
      FunMatch : Id Pat Equals Exp                               ([(Id,Pat,Exp)])
               | Id Pat Equals Exp VerticalBar FunMatch          ((Id,Pat,Exp)::FunMatch)
      CurriedFun :
                 Id PatternSeq Equals Exp                        ([(Id,PatternSeq,Exp)])
               | Id PatternSeq Equals Exp VerticalBar CurriedFun ((Id,PatternSeq,Exp)::CurriedFun)
      Con : Int                                                  (int(Int))
          | Char                                                 (ch(Char))
          | String                                               (str(String))
          | True                                                 (boolval("true"))
          | False                                                (boolval("false"))
          | LParen RParen                                        (tuplecon([]))

    **Fig. 6.6, 6.7, 6.8, 6.9** mlcomp.grm



Example 6.4
==============

.. code-block:: sml

  4 * x + 5


.. container:: exercise

  **Practice 6.3**

  What modifications would be required in the *mlcomp.grm* specification to parse expressions like the one below?

  .. code-block:: text

    case x of
       1 => "hello"
     | 2 => "how"
     | 3 => "are"
     | 4 => "you"

  :ref:`You can check your answer(s) here.<exercise6-3>`

-----------------------------------
Compiling and Running the Compiler
-----------------------------------

.. container:: figboxcenter

  .. code-block:: sml

    5 + 4

  **Fig. 6.10** SML Addition

.. container:: figboxcenter

  .. code-block:: text
    :linenos:

    Function: main/0
    Constants: None, 5, 4
    BEGIN
        LOAD_CONST 1
        LOAD_CONST 2
        BINARY_ADD
        POP_TOP
        LOAD_CONST 0
        RETURN_VALUE
    END

  **Fig. 6.11** CoCo Addition


.. container:: figboxcenter

  .. code-block:: text

    infixexp("+", int("5"),
                  int("4"))

  **Fig. 6.12** Addition AST

Example 6.5
=============

.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    fun codegen(int(i),outFile,indent,consts,...) =
        let val index = lookupIndex(i,consts)
        in
          TextIO.output(outFile,indent^"LOAD_CONST "^index^"\n")
        end
      | codegen(infixexp("+",t1,t2),outFile,indent,consts,...) =
        let val _ = codegen(t1,outFile,indent,consts,...)
            val _ = codegen(t2,outFile,indent,consts,...)
        in
          TextIO.output(outFile,indent^"BINARY_ADD\n")
        end

  **Fig. 6.13** Addition code generation

Example 6.6
=============

.. container:: figboxcenter

  .. code-block:: bash
    :linenos:

    #!/bin/bash
    set -f
    export file="$1"
    if [ -z $file ]; then
      echo -n "Enter a file name: "
      read file
    fi
    if [ -e $file ]; then
      rm a.casm >& /dev/null
      rm a.term >& /dev/null
      echo ******* Source File ********
      cat $file
      sml @SMLload=mlcompimage $file
      echo * Target Program Execution *
      coco a.casm
    else
      echo FILE DOES NOT EXIST
    fi

  **Fig. 6.14** The mlcomp script

.. container:: figbox

  .. code-block:: text
    :linenos:

    fun compile filename  =
        let val (ast, _) = parse filename
            val outFile = TextIO.openOut("a.casm")
            val termFile = TextIO.openOut("a.term")
            val _ = writeTerm(termFile,ast)
            val _ = TextIO.closeOut(termFile)
            val consts = removeDups ("None"::"'Match Not Found'"::"0"::(constants ast))
            val globalBindings = [("println","print"),...]
            val (newbindings,freeVars,cells) = localBindings(ast,[],globalBindings,0)
            val bindingVars = removeDups (List.map (fn x => #2(x)) newbindings)
            val cellVars = List.map (fn x => boundTo(x,newbindings@globalBindings)) cells
            val locals = listdiff bindingVars cellVars
            val globals = removeDups (List.map (fn (x,y) => y) globalBindings)
        in
          if length(freeVars) <> 0 then
             (TextIO.output(TextIO.stdOut,
                "Error: Unbound variable(s) found in main expression => " ^
                (commaSepList freeVars) ^ ".\n");
              raise notFound)
          else ();
          TextIO.output(outFile,"Function: main/0\n");
          nestedfuns(ast,outFile,"    ",globals,[],globalBindings,0);
          TextIO.output(outFile,"Constants: "^(commaSepList consts) ^ "\n");
          if not (List.null(locals)) then
            TextIO.output(outFile,"Locals: "^(commaSepList locals) ^ "\n")
          else ();
          if not (List.null(cellVars)) then
            TextIO.output(outFile,"CellVars: "^(commaSepList cellVars) ^ "\n")
          else ();
          TextIO.output(outFile,"Globals: "^(commaSepList globals) ^ "\n");
          TextIO.output(outFile,"BEGIN\n");
          makeFunctions(ast,outFile,"    ",consts,...);
          codegen(ast,outFile,"    ",consts,...);
          TextIO.output(outFile,"    POP_TOP\n");
          TextIO.output(outFile,"    LOAD_CONST 0\n");
          TextIO.output(outFile,"    RETURN_VALUE\n");
          TextIO.output(outFile,"END\n");
          TextIO.closeOut(outFile)
        end
        handle _ => (TextIO.output(TextIO.stdOut,
                       "An error occurred while compiling!\n\n"));
     fun run(a,b::c) = (compile b; OS.Process.success)
       | run(a,b) = (TextIO.print("usage: sml @SMLload=mlcomp\n");
                     OS.Process.success)

  **Fig. 6.15** MLComp Run Function


.. container:: figboxcenter

  .. code-block:: bash
    :linenos:

    #!/bin/bash
    sml << EOF
    CM.make "sources.cm";
    SMLofNJ.exportFn("mlcompimage",mlcomp.run);
    EOF

  **Fig. 6.16** Makefile.gen

.. container:: figboxcenter

  .. code-block:: text
    :linenos:

    Group is
      $/ml-yacc-lib.cm
      $/basis.cm
      $smlnj-tdp/back-trace.cm
      mlcomp.lex
      mlcomp.grm
      mlcomp.sml
      mlast.sml

  **Fig. 6.17** sources.cm


.. code-block:: text

  make
  mlcomp test0.sml


----------------------
Function Calls
----------------------

.. container:: figboxcenter

  .. code-block:: text
    :linenos:

    Function: main/0
    Constants: None, 'Match Not Found', 0, 5, 4
    Globals: print, fprint, input, int, len,
             type, Exception, funlist, concat
    BEGIN
        LOAD_GLOBAL 0
        LOAD_CONST 3
        LOAD_CONST 4
        BINARY_ADD
        CALL_FUNCTION 1
        POP_TOP
        LOAD_CONST 0
        RETURN_VALUE
    END

  **Fig. 6.18** test1.sml CoCo Code

.. code-block:: text

  apply(id("println"),infixexp("+",int("5"),int("4")))


.. container:: figbox

  .. code-block:: text
    :linenos:

    | codegen(id(name),outFile,indent,consts,...,globals,env,globalBindings,...) =
        load(name,outFile,indent,locals,freeVars,cellVars,globals,globalBindings,env)
    | codegen(apply(t1,t2),outFile,indent,consts,...,globals,env,globalBindings,...) =
        let val _ = codegen(t1,outFile,indent,consts,l...,globals,env,globalBindings,...)
            val _ = codegen(t2,outFile,indent,consts,...,globals,env,globalBindings,...)
        in
           TextIO.output(outFile,indent^"CALL_FUNCTION 1\n")
        end

**Fig. 6.19** Code Generation for Function Calls


---------------------------
Let Expressions
---------------------------

.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let val x = 5
    in
      println x
    end


  **Fig. 6.20** test2.sml

.. container:: figboxcenter

  .. code-block:: text
    :linenos:

    Function: main/0
    Constants: None, 'Match Not Found',
               0, 5
    Locals: x@0
    Globals: print, ...
    BEGIN
        LOAD_CONST 3
        STORE_FAST 0
        LOAD_GLOBAL 0
        LOAD_FAST 0
        CALL_FUNCTION 1
        POP_TOP
        LOAD_CONST 0
        RETURN_VALUE
    END


  **Fig. 6.21** test2.sml CoCo Code


.. code-block:: text

  letdec(bindval(idpat("x"),int("5")),
         [apply(id("println"),id("x"))])



.. container:: figbox

  .. code-block:: sml
    :linenos:

    | codegen(letdec(d,L2),...,consts,locals,...,globals,env,globalBindings,scope) =
      let val newbindings = decgen(d,...,consts,locals,...,globals,env,globalBindings,scope)
      in
        codegenseq(L2,...,consts,locals,...,globals,newbindings@env,globalBindings,scope+1)
      end

  **Fig. 6.22** Let Expression Code Generation



.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let val x = 5
        val y = 6
    in
      println (x + y)
    end

  **Fig. 6.23** test10.sml

  .. container:: figboxcenter

    .. code-block:: sml
      :linenos:

      | Let DecSeq In ExpSequence End
          (List.hd (List.foldr (fn (x,y) => [letdec(x,y)]) ExpSequence DecSeq))

    **Fig. 6.24** The folded set


.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let val x = 5
    in
      let val y = 6
      in
        println (x + y)
      end
    end

  **Fig. 6.25** Unsweetened

----------------------
Unary Negation
----------------------

.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let val x = 5
    in
      println ~x
    end


  **Fig. 6.26** test3.sml


.. code-block:: text

  {tilde} => (Tokens.Negate(!pos,!pos));
  {digit}+({period}{digit}+)?  => (Tokens.Int(yytext,!pos,!pos));


.. code-block:: text

  %term EOF
      | Negate
      | ...


.. code-block:: text

  %right ListCons Negate


.. code-block:: text

  | Negate Exp         (negate(Exp))


.. code-block:: text

  | negate of exp

.. code-block:: text

  | nameOf(infixexp(operator,e1,e2)) = operator
  | nameOf(negate(e)) = "~"


.. code-block:: text

  | con(infixexp(operator,t1,t2)) = (con t1) @ (con t2)
  | con(negate(e)) = "0" :: (con e)


.. code-block:: text

  | bindingsOf(infixexp(operator,exp1,exp2),bindings,scope) =
          (bindingsOf(exp1,bindings,scope); bindingsOf(exp2,bindings,scope))
  | bindingsOf(negate(exp),bindings,scope) = bindingsOf(exp,bindings,scope)


.. code-block:: text

  | codegen(negate(t),outFile,indent,consts,...) =
    let val _ = codegen(int("0"),outFile,indent,consts,...)
        val _ = codegen(t,outFile,indent,consts,...)
    in
      TextIO.output(outFile,indent^"BINARY_SUBTRACT\n")
    end


.. code-block:: text

  | functions(infixexp(operator,exp1,exp2)) = (functions exp1;functions exp2)
  | functions(negate(exp)) = functions exp

.. container:: figboxcenter

  .. code-block:: text
    :linenos:

    Function: main/0
    Constants: None, 'Match Not Found', 5, 0
    Locals: x@0
    Globals: print, ...
        LOAD_CONST 2
        STORE_FAST 0
        LOAD_GLOBAL 0
        LOAD_CONST 3
        LOAD_FAST 0
        BINARY_SUBTRACT
        CALL_FUNCTION 1
        POP_TOP
        LOAD_CONST 0
        RETURN_VALUE
    END

  **Fig. 6.27** test3.sml JCoCo Code


.. code-block:: text
  :linenos:

  | writeExp(indent,negate(exp)) =
            (print("negate(");
             writeExp(indent,exp);
             print(")"))



-------------------------
If-Then-Else Expressions
-------------------------
.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let val x = Int.fromString(
                input("Please enter an integer: "))
        val y = Int.fromString(
                input("Please enter an integer: "))
    in
      print "The maximum is ";
      println (if x > y then x else y)
    end

  **Fig. 6.28** test4.sml

.. container:: figboxcenter

  .. code-block:: text
    :linenos:

    Function: main/0
    Constants: None, 'Match Not Found',
      0, "Please enter an integer: ",
      "The maximum is "
    Locals: y@1, x@0
    Globals: print, fprint, input, int, len,
      type, Exception, funlist, concat
    BEGIN
        LOAD_GLOBAL 3
        LOAD_GLOBAL 2
        LOAD_CONST 3
        CALL_FUNCTION 1
        CALL_FUNCTION 1
        STORE_FAST 1
        LOAD_GLOBAL 3
        LOAD_GLOBAL 2
        LOAD_CONST 3
        CALL_FUNCTION 1
        CALL_FUNCTION 1
        STORE_FAST 0
        LOAD_GLOBAL 1
        LOAD_CONST 4
        CALL_FUNCTION 1
        POP_TOP
        LOAD_GLOBAL 0
        LOAD_FAST 1
        LOAD_FAST 0
        COMPARE_OP 4
        POP_JUMP_IF_FALSE L0
        LOAD_FAST 1
        JUMP_FORWARD L1
    L0:
        LOAD_FAST 0
    L1:
        CALL_FUNCTION 1
        POP_TOP
        LOAD_CONST 0
        RETURN_VALUE
    END

  **Fig. 6.29** test4.sml JCoCo Code



.. code-block:: text

  ifthen(infixexp(">",id("x"),id("y")),id("x"),id("y"))


----------------------
Short-Circuit Logic
----------------------

.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let val x = true
        val y = false
    in
      println (x orelse y div 0);
      println (y andalso x * 5)
    end

  **Fig. 6.30** test5.sml


.. container:: figboxcenter

  .. code-block:: text
    :linenos:

    Function: main/0
    Constants: None,
       'Match Not Found',
       True, False, 0, 5
    Locals: y@1, x@0
    Globals: print, fprint, input,
       int, len, type, Exception,
       funlist, concat
    BEGIN
        LOAD_CONST 2
        STORE_FAST 1
        LOAD_CONST 3
        STORE_FAST 0
        LOAD_GLOBAL 0
        LOAD_FAST 1
        DUP_TOP
        POP_JUMP_IF_TRUE L0
        POP_TOP
        LOAD_FAST 0
        LOAD_CONST 4
        BINARY_FLOOR_DIVIDE
    L0:
        CALL_FUNCTION 1
        POP_TOP
        LOAD_GLOBAL 0
        LOAD_FAST 0
        DUP_TOP
        POP_JUMP_IF_FALSE L1
        POP_TOP
        LOAD_FAST 1
        LOAD_CONST 5
        BINARY_MULTIPLY
    L1:
        CALL_FUNCTION 1
        POP_TOP
        LOAD_CONST 0
        RETURN_VALUE
    END


  **Fig. 6.31** test5.sml JCoCo Code


.. code-block:: text

  infixexp("orelse",id("x"),infixexp("div",id("y"),int("0")))
  infixexp("andalso",id("y"),infixexp("*",id("x"),int("5")))


----------------------
Defining Functions
----------------------


.. code-block:: sml

  TextIO.output(outFile,"Function: main/0\n");
  nestedfuns(ast,outFile,"    ",globals,[],globalBindings,0);



.. code-block:: text

  | Fn MatchExp (func(nextIdNum(),MatchExp))

.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let fun factorial 0 = 1
          | factorial n = n * (factorial (n-1))
    in
      println (factorial 5)
    end

  **Fig. 6.32** test6.sml


.. container:: figboxcenter

  .. code-block:: text
    :linenos:

    Function: main/0
        Function: factorial/1
        Constants: None,
            'Match Not Found', 0, 1
        Locals: factorial@Param, n@1
        FreeVars: factorial
        Globals: print, fprint, input,
            int, len, type, Exception,
            funlist, concat
        BEGIN
            LOAD_FAST 0
            LOAD_CONST 2
            COMPARE_OP 2
            POP_JUMP_IF_FALSE L0
            LOAD_CONST 3
            RETURN_VALUE
    L0:
            LOAD_FAST 0
            STORE_FAST 1
            LOAD_FAST 1
            LOAD_DEREF 0
            LOAD_FAST 1
            LOAD_CONST 3
            BINARY_SUBTRACT
            CALL_FUNCTION 1
            BINARY_MULTIPLY
            RETURN_VALUE
    L1:
            LOAD_GLOBAL 6
            LOAD_CONST 1
            CALL_FUNCTION 1
            RAISE_VARARGS 1
        END
    ...

  **Fig. 6.33** test6.sml JCoCo Code


Curried Functions
====================

.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let
      fun append nil L = L
        | append (h::t) L = h :: (append t L)

      fun appendOne x =
        (fn nil => (fn L => L)
         | h::t => (fn L => h :: (appendOne t L))) x
    in
      println(append [1,2,3] [4]);
      println(appendOne [1,2,3] [4])
    end

  **Fig. 6.34** test7.sml

.. container:: figbox

  .. code-block:: sml
    :linenos:

    exception emptyDecList;
    exception argumentMismatch;
    fun uncurryIt nil = raise emptyDecList
      | uncurryIt (L as ((name,patList,exp)::t)) =
        let fun len nil = raise argumentMismatch
              | len [(n,p,e)] = length(p)
              | len ((n,p,e)::t) =
                let val size = length(p)
                in
                  if size = len t then size else
                    (TextIO.output(TextIO.stdOut,
                      "Syntax Error: Number of arguments does not match in function "^name^"\n");
                     raise argumentMismatch)
                end
            val tupleList = List.map (fn x => "v"^Int.toString(nextIdNum())) patList
         in
           len(L); (* just check the paramter list sizes so all patterns have same length *)
           (name,[match(idpat(hd(tupleList)),
                     List.foldr (fn (x,y) => func(nextIdNum(),[match(idpat(x), y)]))
                        (apply (func(nextIdNum(),List.map (fn (n,p,e) => match(tuplepat(p),e)) L),
                                tuplecon(List.map (fn x => id(x)) tupleList))) (tl tupleList))])
         end

  **Fig. 6.35** The uncurryIt Function



Mutually Recursive Functions
==============================

.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let fun f(0,y) = y
          | f(x,y) = g(x,x*y)
        and g(x,y) = f(x-1,y)
    in
      println (f(10,5))
    end

  **Fig. 6.36** test11.sml

.. code-block:: text

  letdec(funmatches([funmatch("f",f's body),funmatch("g",g's body)]))

.. container:: figboxcenter

  .. code-block:: sml

    | dec(funmatches(L)) =
      let val nameList = List.map (fn (name,matchlist) => name) L
      in
        List.map (fn (name,matchList) =>
        let val adjustedBindings = List.map (fn x => (x,x)) (listdiff nameList [name])
        in
          nestedfun(name,matchList,outFile,indent,globals,adjustedBindings@env,globalBindings,scope)
        end) L;
        ()
      end

    **Fig 6.37** Mutually recursive function declarations

-----------------------
Reference Variables
-----------------------

.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let val x = ref 0
    in
      x := !x + 1;
      println (!x)
    end

  **Fig. 6.38** test8.sml

.. container:: figboxcenter

  .. code-block:: text

    | Exclaim Exp     (apply(id("!"),Exp))
    | Id SetEqual FuncExp (infixexp(":=",id(Id),FuncExp))

  **Fig. 6.39** Set equal and deref operators


.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    and decbindingsOf(bindval(idpat(name),apply(id("ref"),exp)),bindings,scope) =
        let val newbindings = patBindings(idpat(name),scope)
            val newcellvar = name^"@"^Int.toString(scope)
        in
          bindingsOf(exp,newbindings@bindings,scope+1);
          addIt(newcellvar,cellVars);
          [addIt((name,newcellvar),theBindings)]
        end

  **Fig. 6.40** Reference variable bindings

.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    | codegen(apply(id("ref"),t2),...) =
          codegen(t2,outFile,...)
    | codegen(apply(id("!"),t2),...) =
          codegen(t2,outFile,...)
    | codegen(infixexp(":=",id(name),t2),...) =
      let val _ = codegen(t2,...)
          val noneIndex =
                lookupIndex("None",consts)
      in
        store(name,outFile,indent,locals,,...);
        TextIO.output(outFile,
            indent^"LOAD_CONST "^noneIndex^"\n")
      end

  **Fig. 6.41** Variable Code Generation



.. code-block:: text
  :linenos:

  | bindingsOf(id("!"),bindings,scope) = ()


.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let val x = 0
        fun f y = (x:=!x+1)
    in
      f 0;
      println x
    end


  **Fig. 6.42** test9.sml




------------------
Chapter Summary
------------------


-----------------
Review Questions
-----------------

  #.  The language of regular expressions can be used to define the tokens of a language. Give an example for a regular expression from the chapter and indicate what kind of tokens it represents.
  #.  What does ML-lex do? What input does it require? What does it produce?

  #.  What does ML-yacc do? What input does it require? What does it produce?

  #.  How is an abstract syntax tree declared in ML?

       .. code-block:: sml

           fun abs(x) = if x > 0 then x else ~1*x

---------
Exercises
---------

  #. Modify the compiler to support unary negation as described in this chapter. Upon completion *test3.sml* should compile and run correctly.
  #. Add >=, <=, and <> (not equal) operators to the Small language. Provide all the pieces in all the files so programs using these operators can be compiled. Write a Small program that demonstrates that this functionality works.
  #. Add support for *if-then-else* expressions to the Small compiler as described in this chapter. Follow the instructions of the chapter and be sure to test your implementation using *test4.sml*.
  #. Implement short-circuit logic as described in this chapter for the *andalso* and the *orelse* operators.
  #. Follow the step in this chapter to add support for compiling expressions with variables. Then, implement a *while do* loop for the *mlcomp* compiler. A while loop is written *while Exp1 do Exp2*. The *Exp1* expression is evaluated first to see if it yields true. If it does, then *Exp2* is evaluated. This repeats until *Exp2* returns false. Remember your job is to generate code for a while loop, not execute it. Use examples like adding *if-then-else* to help you determine where the changes need to be made to add support for *while do* loops. Successfully writing this code will result in successfully compiling and running test12.sml.
  #. Add support for *case* expressions in the *mlcomp* Small compiler. The concrete syntax of a case statement is

       .. code-block:: sml

           Expression : ...
             | Case Exp Of MatchExp  (caseof(Exp,MatchExp))

     while the abstract syntax of a case expression is given here.

       .. code-block:: sml

           caseof of exp * match list

     Follow an example like adding support for unary negation to see what all is required to support the *case* expression in CoCo. Write a program to test the use of the *case* expression in your code. There is currently no support for case expressions in the mlcomp compiler. This project will require you to add support to all facets of the compiler including the scanner, parser, and code generator. When you have successfully implemented the code to parse and compile case expressions, you will be able to compile this program which is test15.sml in the mlcomp distribution.

       .. code-block:: sml
          :linenos:

          let val x = 4
          in
            println
              case x of
                1 => "hello"
              | 2 => "how"
              | 3 => "are"
              | 4 => "you"
          end

     The generated code for this program is given below. The program, when run, will print *you* to the screen.

       .. code-block:: text
          :linenos:

          Function: main/0
          Constants: None, 'Match Not Found', 0, 1, "hello", 2, "how", 3, "are", 4, "you"
          Locals: x@0
          Globals: print, fprint, input, int, len, type, Exception, funlist, concat
          BEGIN
              LOAD_CONST 9     # Here the 6 is stored in x.
              STORE_FAST 0
              LOAD_GLOBAL 0    # This is the println pushed onto stack.
              LOAD_FAST 0      # x is loaded onto stack.
              DUP_TOP          # Case expression code where x's value is duplicated.
              LOAD_CONST 3     # This is a pattern match for the first pattern.
              COMPARE_OP 2
              POP_JUMP_IF_FALSE L1
              POP_TOP          # Case expression code to pop x from stack
              LOAD_CONST 4     # This is the expression for the first match.
              JUMP_FORWARD L0  # Case expression code to jump to end of case.
          L1:                  # Case expression code for label for end of first pattern.
              DUP_TOP          # Case expression code where x's value is duplicated.
              LOAD_CONST 5     # This is a pattern match for the second pattern.
              COMPARE_OP 2
              POP_JUMP_IF_FALSE L2
              POP_TOP          # Case expression code to pop x from stack
              LOAD_CONST 6     # This is the expression for the second match.
              JUMP_FORWARD L0  # Case expression code to jump to end of case.
          L2:                  # Case expression code for label for end of second pattern.
              DUP_TOP          # Case expression code where x's value is duplicated.
              LOAD_CONST 7     # This is a pattern match for the third pattern.
              COMPARE_OP 2
              POP_JUMP_IF_FALSE L3
              POP_TOP          # Case expression code to pop x from stack
              LOAD_CONST 8     # This is the expression for the third match.
              JUMP_FORWARD L0  # Case expression code to jump to end of case.
          L3:                  # Case expression code for label for end of third pattern.
              DUP_TOP          # Case expression code where x's value is duplicated.
              LOAD_CONST 9     # This is a pattern match for the fourth pattern.
              COMPARE_OP 2
              POP_JUMP_IF_FALSE L4
              POP_TOP          # Case expression code to pop x from stack
              LOAD_CONST 10    # This is the expression for the fourth match.
              JUMP_FORWARD L0  # Case expression code to jump to end of case.
          L4:                  # Case expression code for label for end of fourth pattern.
          L0:                  # This is the end of case expression label.
              CALL_FUNCTION 1  # print the result which was left on the stack
              POP_TOP          # Pop the None left by println
              LOAD_CONST 0     # Push a None to return
              RETURN_VALUE     # Return the None
          END




  #. The following program does not compile correctly using the mlcomp compiler and type inference system. However, it is a valid Standard ML program. Modify the mlcomp compiler to correctly compile this program.

     .. code-block:: sml

        let val [(x,y,z)] = [("hello",1,true)] in println x end

------------------------------
Solutions to Practice Problems
------------------------------

These are solutions to the practice problem s. You should only consult these answers after you have tried each of them for yourself first. Practice problems  are meant to help reinforce the material you have just read so make use of them.

.. _exercise6-1:

Solution to Practice Problem 6.1
================================

The keywords *case* and *of* must be added to the scanner specification in *mlcomp.lex*. All the other tokens are already available in the scanner.

.. _exercise6-2:

Solution to Practice Problem 6.2
================================

You need to add a new AST node type.

.. code-block:: sml

           | caseof of exp * match list


.. _exercise6-3:

Solution to Practice Problem 6.3
================================

The grammar changes required for case expressions are as follows.

.. code-block:: sml

  Expression : ...
    | Case Exp Of MatchExp  (caseof(Exp,MatchExp))
