============================
Syntax
============================

-----------
Terminology
-----------


.. code-block:: cpp

  a=b+c;



----------------------
Backus Naur Form (BNF)
----------------------


    <syntactic category> ::= a string of terminals and nonterminals


.. _bnfexamples:

BNF Examples
===================


.. code-block:: text

  <primitive-type> ::= boolean
  <primitive-type> ::= char


.. code-block:: text

 <primitive-type> ::= boolean | char | byte | short | int | long | float | ...
 <argument-list> ::= <expression> | <argument-list> , <expression>
 <selection-statement> ::=
   if ( <expression> ) <statement> |
   if ( <expression> ) <statement> else <statement> |
   switch ( <expression> ) <block>
 <method-declaration> ::=
   <modifiers> <type-specifier> <method declarator> <throws-clause> <method-body> |
   <modifiers> <type-specifier> <method-declarator> <method-body> |
   <type-specifier> <method-declarator> <throws-clause> <method-body> |
   <type-specifier> <method-declarator> <method-body>


Extended BNF (EBNF)
===================

  #.  **item?** or **[item]** means the item is optional.
  #.  **item\*** or **\{item\}** means zero or more occurrences of an item are allowable.
  #.  **item+** means one or more occurrences of an item are allowable.
  #.  Parentheses may be used for grouping


---------------------
Context-Free Grammars
---------------------

.. math::
   G = (N,T,P,S)

where

  *  :math:`N` is a set of symbols called nonterminals or syntactic categories.
  *  :math:`T` is a set of symbols called terminals or tokens.
  *  :math:`P` is a set of productions of the form :math:`n \rightarrow \alpha`
     where :math:`n \in N` and :math:`\alpha \in (N \cup T)^*`
  *  :math:`S \in N` is a special nonterminal called the start symbol of the grammar.

.. _infixgrammar:

The Infix Expression Grammar
=============================

A context-free grammar for infix expressions can be specified as
:math:`G=(N,T,P,E)` where

|
|            :math:`N = \{E,T,F\}`
|            :math:`T = \{identifier,number,+,-,*,/,(,)\}`
|            :math:`P` is defined by the set of productions
|
|              :math:`E \rightarrow E~+~T \mid E~-~T \mid T`
|              :math:`T \rightarrow T~*~F \mid T~/~F \mid F`
|              :math:`F \rightarrow (~E~) \mid identifier \mid number`



-----------
Derivations
-----------


.. _derivationsec:

A Derivation
=============

.. math::

   & \underline{E} \Rightarrow  \underline{E} + T \Rightarrow \underline{T} + T \Rightarrow \underline{F} + T \Rightarrow (\underline{ E }) + T \Rightarrow ( \underline{T} ) + T \Rightarrow ( \underline{T} * F ) + T  \\
   & \Rightarrow ( \underline{F} * F ) + T  \Rightarrow ( 5 * \underline{F} ) + T \Rightarrow ( 5 * x ) + \underline{T} \Rightarrow ( 5 * x ) + \underline{F} \Rightarrow ( 5 * x ) + y


.. container:: exercise

  **Practice 2.1**

  Construct a derivation for the infix expression 4+(a-b)\*x.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-1>`

Types of Derivations
====================


.. math::
   & E  \Rightarrow E + T  \Rightarrow E + F  \Rightarrow E + y  \Rightarrow T + y  \Rightarrow F + y  \Rightarrow ( E ) + y  \Rightarrow ( T ) + y
   \Rightarrow ( T * F) + y  \\
   &\Rightarrow ( T * x ) + y  \Rightarrow ( F * x ) + y  \Rightarrow ( 5 * x ) + y


.. container:: exercise

  **Practice 2.2**

  Construct a right-most derivation for the expression x\*y+z.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-2>`

Prefix Expressions
==================


The Prefix Expression Grammar
==============================

A context-free grammar for prefix expressions can be specified as
:math:`G=(N,T,P,E)` where

|
|            :math:`N = \{E\}`
|            :math:`T = \{identifier,number,+,-,*,/\}`
|            :math:`P` is defined by the set of productions
|
|              :math:`E \rightarrow +~E~E \mid -~E~E \mid *~E~E \mid /~E~E \mid identifier \mid number`



.. container:: exercise

  **Practice 2.3**

  Construct a left-most derivation for the prefix expression +4\*-a b x.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-3>`

-----------
Parse Trees
-----------



.. container:: figboxcenter

   .. _parsetree:

   .. figure:: parsetree.png

  **Fig 2.1** A Parse Tree


.. container:: exercise

  **Practice 2.4**

  What does the parse tree look like for the right-most derivation of (5\*x)+y?

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-4>`


.. container:: exercise

  **Practice 2.5**

  Construct a parse tree for the infix expression 4+(a-b)\*x.

  HINT: What has higher precedence, "+" or "\*"? The given grammar automatically makes "\*" have higher precedence. Try it the other way and see why!

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-5>`


.. container:: exercise

  **Practice 2.6**

  Construct a parse tree for the prefix expression +4\*-a b x.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-6>`


---------------------
Abstract Syntax Trees
---------------------

.. container:: figboxcenter

   .. _abstree:

   .. figure:: abstree.png

  **Fig 2.2** An AST


.. container:: exercise

  **Practice 2.7**

  Construct an abstract syntax tree for the expression 4+(a-b)\*x.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-7>`


-----------------------
Lexical Analysis
-----------------------


The Language of Regular Expressions
=====================================

The language of regular expression is defined by a context-free grammar. The context-free grammar for regular expressions is :math:`RE=(N,T,P,E)` where

|
|            :math:`N = \{ E, T, K, F \}`
|            :math:`T = \{character, *, +, ., (, ) \}`
|            :math:`P` is defined by the set of productions
|
|              :math:`E \rightarrow E + T \mid T`
|              :math:`T \rightarrow T . K \mid K`
|              :math:`K \rightarrow F * \mid F`
|              :math:`F \rightarrow character \mid (~E~)`


  letter.letter\* + digit.digit\* + '+' + '-' + '*' + '/' + '(' + ')'


.. container:: exercise

  **Practice 2.8**

  Define a regular expression so that negative and non-negative integers can both be specified as tokens of the infix expression language.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-8>`

Finite State Machines
=======================

Formally a finite state automata is defined as follows.

  :math:`M=(\Sigma, S, F, s_0, \delta)`
    where :math:`\Sigma` (pronounced sigma) is the input alphabet (the characters understood by the machine),
    :math:`S` is a set of states,
    :math:`F` is a subset of :math:`S` usually written as :math:`F \subseteq S`,
    :math:`s_0` is a special state called the start state,
    and :math:`\delta` (pronounced delta) is a function that takes as input an alphabet symbol and a state and returns a new state. This is usually written as :math:`\delta : \Sigma \times S \rightarrow S`.


.. container:: figboxcenter

   .. _lexerfsm:

   .. figure:: lexerfsm.png

  **Fig 2.3** A Finite State Machine


Lexer Generators
=================

-------
Parsing
-------

.. container:: figboxcenter

   .. _parser:

   .. figure:: parser.png

  **Fig 2.4** Parser Data Flow


----------------
Top-Down Parsers
----------------

An LL(1) Grammar
==================

The grammar for prefix expressions is LL(1). Examine the prefix expression grammar :math:`G=(N,T,P,E)` where

|
|            :math:`N = \{E\}`
|            :math:`T = \{identifier,number,+,-,*,/\}`
|            :math:`P` is defined by the set of productions
|
|              :math:`E \rightarrow +~E~E \mid -~E~E \mid *~E~E \mid /~E~E \mid identifier \mid number`


.. _nonll1:

A Non-LL(1) Grammar
=====================

Some grammars are not LL(1). The grammar for infix expressions is not LL(1). Examine the infix expression grammar :math:`G=(N,T,P,E)` where

|
|            :math:`N = \{E,T,F\}`
|            :math:`T = \{identifier,number,+,-,*,/,(,)\}`
|            :math:`P` is defined by the set of productions
|
|              :math:`E \rightarrow E~+~T \mid E~-~T \mid T`
|              :math:`T \rightarrow T~*~F \mid T~/~F \mid F`
|              :math:`F \rightarrow (~E~) \mid identifier \mid number`


.. math::
   E  \Rightarrow T  \Rightarrow T * F \Rightarrow F * F  \Rightarrow 5 * F  \Rightarrow 5 * 4


.. _ll1infix:

An LL(1) Infix Expression Grammar
===================================

The following grammar is an LL(1) grammar for infix expressions. :math:`G=(N,T,P,E)` where

|
|            :math:`N = \{E,RestE, T, RestT, F\}`
|            :math:`T = \{identifier,number,+,-,*,/,(,)\}`
|            :math:`P` is defined by the set of productions
|
|              :math:`E \rightarrow T~RestE`
|              :math:`RestE \rightarrow +~T~RestE \mid -~T~RestE \mid \epsilon`
|              :math:`T \rightarrow F~RestT`
|              :math:`RestT \rightarrow *~F~RestT \mid /~F~RestT \mid \epsilon`
|              :math:`F \rightarrow (~E~) \mid identifier \mid number`



.. container:: exercise

  **Practice 2.9**

  Construct a left-most derivation for the infix expression 4+(a-b)\*x using the grammar in :ref:`ll1infix`, proving that this infix expression is in L(G) for the given grammar.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-9>`


-----------------
Bottom-Up Parsers
-----------------

.. container:: figboxcenter

   .. _generator:

   .. figure:: generator.png

  **Fig 2.5** Parser Generator Data Flow

.. _pda:

PDA
======

.. container:: figboxcenter

   .. figure:: pda.png

  **Fig 2.6** A Pushdown Automaton Stack


.. _infixparse:

Parsing an Infix Expression
============================

Consider the grammar for infix expressions as
:math:`G=(N,T,P,E)` where

|
|            :math:`N = \{E,T,F\}`
|            :math:`T = \{identifier,number,+,-,*,/,(,)\}`
|            :math:`P` is defined by the set of productions
|
|              :math:`(1)~E \rightarrow E~+~T`
|              :math:`(2)~E \rightarrow T`
|              :math:`(3)~T \rightarrow T~*~F`
|              :math:`(4)~T \rightarrow F`
|              :math:`(5)~F \rightarrow number`
|              :math:`(6)~F \rightarrow ( E )`


.. math::
   E  \Rightarrow E + T  \Rightarrow E + F  \Rightarrow E + 3  \Rightarrow T + 3  \Rightarrow T * F + 3 \Rightarrow T * 4 + 3 \Rightarrow F * 4 + 3 \Rightarrow 5 * 4 + 3

.. container:: exercise

  **Practice 2.10**

  For each step in :ref:`pda`, is there a shift or reduce operation being performed? If it is a reduce operation, then what production is being reduced? If it is a shift operation, what token is being shifted onto the stack?

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-10>`

.. container:: exercise

  **Practice 2.11**

  Consider the expression (6+5)\*4. What are the contents of the pushdown automaton's stack as the expression is parsed using a bottom-up parser? Show the stack after each shift and each reduce operation.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise2-11>`

----------------------
Ambiguity in Grammars
----------------------

.. code-block:: ruby

    if a<b then
      if b<c then
        writeln("a<c")
    else
      writeln("?")


.. code-block:: ruby

   <statement> ::= if <expression> then <statement> else <statement>
                 | if <expression> then <statement>
                 | writeln ( <expression> )


-----------------------
Other Forms of Grammars
-----------------------

------------------------------------
Limitations of Syntactic Definitions
------------------------------------

-----------------------------------------------
Chapter Summary
-----------------------------------------------

-----------------
Review Questions
-----------------

  #.  What does the word syntax refer to? How does it differ from semantics?
  #.  What is a token?
  #.  What is a nonterminal?
  #.  What does BNF stand for? What is its purpose?
  #.  What kind of derivation does a top-down parser construct?
  #.  What is another name for a top-down parser?
  #.  What does the abstract syntax tree for 3\*(4+5) look like for infix expressions?
  #.  What is the prefix equivalent of the infix expression 3\*(4+5)? What does the prefix expression's abstract syntax tree look like?
  #.  What is the difference between lex and yacc?
  #.  Why aren't all context-free grammars good for top-down parsing?
  #.  What kind of machine is needed to implement a bottom-up parser?
  #.  What is a context-sensitive issue in a language? Give an example in Java.
  #.  What do the terms *shift* and *reduce* apply to?

---------
Exercises
---------

  #.  Rewrite the BNF in :ref:`bnfexamples` using EBNF.
  #.  Given the grammar in :ref:`infixgrammar`, derive the sentence 3\*(4+5) using a right-most derivation.
  #.  Draw a parse tree for the sentence 3\*(4+5).
  #.  Describe how you might evaluate the abstract syntax tree of an expression to get a result? Write out your algorithm in English that describes how this might be done.
  #.  Write a regular expression to describe identifier tokens which must start with a letter and then can be followed by any number of letters, digits, or underscores.
  #.  Draw a finite state machine that would accept identifier tokens as specified in the previous exercise.
  #.  For the expression 3\*(4+5) show the sequence of shift and reduce operations using the grammar in :ref:`infixparse`. Be sure to say what is shifted and which rule is being used to reduce at each step. See the solution to practice problem 2.11 for the proper way to write the solution to this problem.
  #.  Construct a left-most derivation of 3\*(4+5) using the grammar in :ref:`ll1infix`.

------------------------------
Solutions to Practice Problems
------------------------------

These are solutions to the practice problems. You should only consult these answers after you have tried each of them for yourself first. Practice problems are meant to help reinforce the material you have just read so make use of them.


.. _exercise2-1:

Solution to Practice Problem 2.1
================================

This is a left-most derivation of the expression. There are other derivations that would be correct as well.



.. math::
   & E \Rightarrow E + T \Rightarrow T + T \Rightarrow F + T \Rightarrow 4 + T \Rightarrow 4 + T * F \Rightarrow 4 + F * F \Rightarrow 4 + ( E ) * F \\
   & \Rightarrow 4 + ( E - T ) * F \Rightarrow 4 + ( T - T ) * F \Rightarrow 4 + ( F - T ) * F \Rightarrow 4 + ( a - T ) * F \Rightarrow \\
   & 4 + ( a - F ) * F \Rightarrow 4 + ( a - b ) * F \Rightarrow 4 + ( a - b ) * x \\


.. _exercise2-2:

Solution to Practice Problem 2.2
================================

This is a right-most derivation of the expression x\*y+z. There is only one correct right-most derivation.

.. math::
   E \Rightarrow E + T \Rightarrow E + F \Rightarrow E + z \Rightarrow T + z \Rightarrow T * F + z \Rightarrow T * y + z \Rightarrow F * y + z \Rightarrow x * y + z



.. _exercise2-3:

Solution to Practice Problem 2.3
================================

This is a left-most derivation of the expression +4\*-a b x.

.. math::
   & E \Rightarrow + E E \Rightarrow + 4 E \Rightarrow + 4 * E E \Rightarrow + 4 * - E E E  \Rightarrow + 4 * - a E E \Rightarrow + 4 * - a b E \Rightarrow + 4 * - a b x



.. _exercise2-4:

Solution to Practice Problem 2.4
================================

Exactly like the parse tree for any other derivation of (5\*x)+y. There is only one parse tree for the expression given this grammar.

.. _exercise2-5:

Solution to Practice Problem 2.5
================================


.. container:: figboxcenter

   .. _parsetree2ex:

   .. figure:: parsetree2ex.png

  **Fig 2.7** The parse tree for practice problem 2.5

.. _exercise2-6:

Solution to Practice Problem 2.6
================================


.. container:: figboxcenter

   .. _parsetreeprefix:

   .. figure:: parsetreeprefix.png

  **Fig 2.8** The parse tree for practice problem 2.6

.. _exercise2-7:

Solution to Practice Problem 2.7
=================================


.. container:: figboxcenter

   .. _abstreeex:

   .. figure:: abstreeex.png

  **Fig 2.9** The abstract syntax tree for practice problem 2.7



.. _exercise2-8:

Solution to Practice Problem 2.8
=================================
In order to define both negative and positive numbers, we can use the choice operator.


  letter.letter\* + digit.digit\* + '-'.digit.digit* '+' + '-' + '*' + '/' + '(' + ')'

.. _exercise2-9:

Solution to Practice Problem 2.9
=================================

.. math::
   & E \Rightarrow T~RestE \Rightarrow F~RestT~RestE \Rightarrow 4~RestT~RestE \Rightarrow 4~RestE \Rightarrow \\
   & 4 + T~RestE \Rightarrow 4 + F~RestT~RestE \Rightarrow 4 + ( E )~RestT~RestE \Rightarrow 4 + ( T~RestE ) RestT~RestE \\
   & \Rightarrow 4 + ( F~RestT~RestE )~RestT~RestE \Rightarrow 4 + ( a~RestT~RestE ) RestT~RestE~\Rightarrow \\
   & 4 + ( a~RestE )~RestT~RestE  \Rightarrow 4 + ( a - T~RestE )~RestT~RestE \Rightarrow \\
   & 4 + ( a - F~RestE )~RestT~RestE \Rightarrow 4 + ( a - b~RestE ) \Rightarrow 4 + ( a - b )~RestT~RestE \\
   & \Rightarrow 4 + ( a - b ) * F~RestT~RestE \Rightarrow 4 + ( a - b ) * x~RestT~RestE \Rightarrow 4 + ( a - b ) * x~RestE \\
   & \Rightarrow 4 + ( a - b ) * x

.. _exercise2-10:

Solution to Practice Problem 2.10
=================================
In the parsing of 5\*4+3 the following shift and reduce operations: step A initial condition, step B shift, step C reduce by rule 5, step D reduce by rule 4, step E shift, step F shift, step G reduce by rule 5, step H reduce by rule 3, step I reduce by rule 2, step J shift, step K shift, step L reduce by rule 5, step M reduce by rule 4, step N reduce by rule 1, step O finished parsing with dot on right side and E on top of stack so pop and complete with success.


.. _exercise2-11:

Solution to Practice Problem 2.11
=================================

To complete this problem it is best to do a right-most derivation of (6+5)\*4 first. Once that derivation is complete, you go through the derivation backwards. The difference in each step of the derivation tells you whether you shift or reduce. Here is the result.

.. math::
  & E \Rightarrow T \Rightarrow T * F \Rightarrow T * 4 \Rightarrow F * 4 \Rightarrow ( E ) * 4 \Rightarrow ( E + T ) * 4 \Rightarrow ( E + F ) * 4 \Rightarrow ( E + 5 ) * 4 \\
  &\Rightarrow ( T + 5 ) * 4 \Rightarrow ( F + 5 ) * 4 \Rightarrow ( 6 + 5 ) * 4

We get the following operations from this. Stack contents have the top on the right up to the dot. Everything after the dot has not been read yet. We shift when we must move through the tokens to get to the next place we are reducing. Each step in the reverse derivation provides the reduce operations. Since there are seven tokens there should be seven shift operations.

  #. Initially: . ( 6 + 5 ) * 4
  #. Shift: ( . 6 + 5 ) * 4
  #. Shift: ( 6 . + 5 ) * 4
  #. Reduce by rule 5: ( F . + 5 ) * 4
  #. Reduce by rule 4: ( T . + 5 ) * 4
  #. Reduce by rule 2: ( E . + 5 ) * 4
  #. Shift: ( E + . 5 ) * 4
  #. Shift: ( E + 5 . ) * 4
  #. Reduce by rule 5: ( E + F . ) * 4
  #. Reduce by rule 4: ( E + T . ) * 4
  #. Shift: ( E + T ) . * 4
  #. Reduce by rule 1: ( E ) . * 4
  #. Reduce by rule 6: F . * 4
  #. Reduce by rule 4: T . * 4
  #. Shift: T * . 4
  #. Shift: T * 4 .
  #. Reduce by rule 5: T * F .
  #. Reduce by rule 3: T .
  #. Reduce by rule 2: E .
