============================
Prolog
============================


.. container:: figboxcenter

  .. code-block:: sml
    :linenos:

    let val m = ref 0
        val n = ref 0
    in
      m:=Int.fromString(input("Please enter an integer: "));
      n:=Int.fromString(input("Please enter another: "));
      while !m >= !n do m:=!m-!n;
      println(!m)
    end

  **Fig. 7.1** A Small Sample


---------------------------
Getting Started with Prolog
---------------------------

.. container:: figboxcenter

  .. code-block:: prolog

    parent(fred, sophusw). parent(fred, lawrence).
    parent(fred, kenny). parent(fred, esther).
    parent(inger,sophusw). parent(johnhs, fred).
    parent(mads,johnhs). parent(lars, johan).
    parent(johan,sophus). parent(lars,mads).
    parent(sophusw,gary). parent(sophusw,john).
    parent(sophusw,bruce). parent(gary, kent).
    parent(gary, stephen). parent(gary,anne).
    parent(john,michael). parent(john,michelle).
    parent(addie,gary). parent(gerry, kent).
    male(gary). male(fred).
    male(sophus). male(lawrence).
    male(kenny). male(esther).
    male(johnhs). male(mads).
    male(lars). male(john).
    male(bruce). male(johan).
    male(sophusw). male(kent).
    male(stephen). female(inger).
    female(anne). female(michelle).
    female(gerry). female(addie).
    father(X,Y):-parent(X,Y),male(X).
    mother(X,Y):-parent(X,Y), female(X).

  **Fig. 7.2** The Family Tree



Example 7.2
===========


------------
Fundamentals
------------



.. code-block:: prolog

  father(X,Y):-parent(X,Y), male(X).



.. container:: exercise

  **Practice 7.1**

  What are the terms in example 7.2? What is the difference between an atom and a variable? Give examples of terms, atoms, and variables from example 7.2.

  :ref:`You can check your answer(s) here.<exercise7-1>`


Example 7.3
===========


.. code-block:: prolog

  % swipl
  ?- consult('family.prolog').
  ?- father(johan,sophus).
  Yes
  ?-


Example 7.4
===========


.. code-block:: prolog

  ?- father(X, sophus).
  X = johan
  Yes
  ?- parent(X,kent).
  X = gary ;
  X = gerry ;
  No
  ?-

-----------------------------------
The Prolog Program
-----------------------------------


Example 7.5
===========


.. code-block:: prolog

  ?- father(X,kent).
  X = gary ;
  No
  ?- father(gary,X).
  X = kent ;
  X = stephen ;
  X = anne ;
  No



.. container:: exercise

  **Practice 7.2**

  Write predicates that define the following relationships.

    #.  brother
    #.  sister
    #.  grandparent
    #.  grandchild

  Depending on how you wrote grandparent and grandchild  there might be something to note about these two predicates. Do you see a pattern? Why?

  :ref:`You can check your answer(s) here.<exercise7-2>`




-----
Lists
-----

Example 7.6
===========


.. code-block:: prolog

  append([],Y,Y).
  append([H|T1], L2, [H|T3]) :- append(T1,L2,T3).


Example 7.7
===========


.. code-block:: prolog

  sublist(X,Y) :- append(_,X,L), append(L,_,Y).



  .. container:: figboxcenter

     .. figure:: prologproof.png


  **Fig. 7.3** A Unification Tree

.. container:: exercise

  **Practice 7.3**

  What is the complexity of the append predicate? How many steps does it take to append two lists?

  :ref:`You can check your answer(s) here.<exercise7-3>`


.. container:: exercise

  **Practice 7.4**

  Write the reverse predicate for lists in Prolog using the append predicate. What is the complexity of this reverse predicate?

  :ref:`You can check your answer(s) here.<exercise7-4>`

-----------------------------------
The Accumulator Pattern
-----------------------------------


.. code-block:: sml

  fun reverse(L) =
      let fun helprev (nil, acc) = acc
            | helprev (h::t, acc) = helprev(t,h::acc)
      in
        helprev(L,[])
      end




.. container:: exercise

  **Practice 7.5**

  Write the reverse predicate using a helper predicate to make a linear time reverse using the accumulator pattern.

  :ref:`You can check your answer(s) here.<exercise7-5>`


-------------------
Built-in Predicates
-------------------



--------------------------
Unification and Arithmetic
--------------------------




.. code-block:: prolog

        Singleton variables: [X]




.. container:: exercise

  **Practice 7.6**

  Write a length predicate that computes the length of a list.

  :ref:`You can check your answer(s) here.<exercise7-6>`


----------------
Input and Output
----------------



Example 7.8
===========


.. code-block:: prolog

  ? - readln(L,_,_,_,lowercase).



.. code-block:: prolog

  |: + 5 S R
  L = [+, 5, s, r] ;
  No
  ?-



Example 7.9
===========


.. code-block:: prolog

  ?- print(X).
  _G180
  X = _G180 ;
  No



----------
Structures
----------


Example 7.10
============


.. code-block:: prolog

  btnode(5,
    btnode(3,
      btnode(2, nil, nil),
      btnode(4, nil, nil)),
    btnode(8,
      btnode(7, nil, nil),
      btnode(9, nil,
        btnode(10, nil, nil))))


.. container:: figboxcenter

   .. figure:: bst.png

   **Fig. 7.4** Search Tree




.. container:: exercise

  **Practice 7.7**

  Write a lookup predicate that looks up a value in a binary search tree like the kind defined in example 7.10.

  :ref:`You can check your answer(s) here.<exercise7-7>`


-----------------
Parsing in Prolog
-----------------


Example 7.11
============


Sentence ::= Subject Predicate .

Subject ::= Determiner Noun

Predicate ::= Verb | Verb Subject

Determiner ::= a | the

Noun ::= professor | home | group

Verb ::= walked | discovered | jailed


.. container:: exercise

  **Practice 7.8**

  Construct the parse tree for "the professor discovered a group." using the grammar in example 7.11.

  :ref:`You can check your answer(s) here.<exercise7-8>`



Example 7.12
============


.. container:: figbox

   .. figure:: prologsen.png

   **Fig. 7.5** A Transition Graph


.. container:: figboxcenter

   .. figure:: prologsub2.png

   **Fig. 7.6** Sentence Structure



.. container:: figbox

   .. figure:: prologsennum.png

   **Fig. 7.7** Labeled Graph



.. code-block:: prolog

  the(1,2).
  professor(2,3).
  discovered(3,4).
  a(4,5).
  group(5,6).
  period(6,7).


.. code-block:: prolog

  subject(K,L) :- determiner(K,M), noun(M,L).


.. container:: exercise

  **Practice 7.9**

  Construct the predicates for the rest of the grammar.

  :ref:`You can check your answer(s) here.<exercise7-9>`

Example 7.13
============

.. code-block:: prolog

  ?- sentence(1,7).
  yes
  ? - sentence(X,Y).
  X = 1
  Y = 7

Example 7.14
============

.. container:: figboxcenter

   .. figure:: sengraph.png

   **Fig. 7.8** An Upside Down Parse Tree



Difference Lists
================


Example 7.15
============


.. container:: figboxcenter

   .. figure:: difflists.png

   **Fig. 7.9** Difference Lists


Example 7.16
============


.. code-block:: prolog

  c([H|T],H,T).




.. code-block:: prolog

  determiner(K,L) :- c(K,a,L).
  determiner(K,L):- c(K,the,L).

  noun(K,L) :- c(K,professor,L).
  noun(K,L) :- c(K,home,L).
  noun(K,L) :- c(K,group,L).

  verb(K,L) :- c(K,walked,L).
  verb(K,L) :- c(K,discovered,L).
  verb(K,L) :- c(K,jailed,L).


.. code-block:: prolog

  ?- sentence([the,professor,discovered,a,group,'.'], [ ]).
  yes



.. code-block:: prolog

  ?- sentence(S,[ ]).





.. code-block:: prolog

  Subject ::= Determiner Noun | Determiner Noun Subject




--------------------
Prolog Grammar Rules
--------------------


Example 7.17
============



.. code-block:: prolog

  sentence --> subject, predicate,['.'].
  subject --> determiner, noun.
  predicate --> verb, subject.
  determiner --> [a].
  determiner --> [the].
  noun --> [professor]; [home]; [group].
  verb --> [walked]; [discovered]; [jailed].


-----------------------------------
Building an AST
-----------------------------------




Example 7.18
============


.. code-block:: prolog

  sentence(sen(N,P)) --> subject(N), predicate(P), ['.'].


.. code-block:: prolog

  sentence(sen(N,P),K,L) :- subject(N,K,M),
  	                        predicate(P,M,R),c(R,'.',L).



.. code-block:: prolog

  ?- sentence(Tree, [the,professor,discovered,a,group,'.'],[]).
  Tree = sen(sub(det(the),noun(professor)),
  	           pred(verb(discovered),sub(det(a),noun(group))))



.. container:: exercise

  **Practice 7.10**

  Write a grammar for the subset of English sentences presented in this text to parse sentences like the one above. Include parameters to build abstract syntax trees like the one above.

  :ref:`You can check your answer(s) here.<exercise7-10>`


--------------------
Attribute Grammars
--------------------


.. container:: figboxcenter

   .. figure:: attrtree.png

   **Fig. 7.10** Annotated AST for + S 4 R

.. container:: figboxcenter

  .. code-block:: text

      AST = prog of AST
          | add of AST * AST
          | sub of AST * AST
          | prod of AST * AST
          | div of AST * AST
          | negate of AST
          | num of number
          | store of AST
          | recall

  **Fig. 7.11** AST Definition



Example 7.19
==============

| :math:`G=(\mathcal{N,T,P,}E)` where
|
|    :math:`\mathcal{N} = {E}`
|    :math:`\mathcal{T} = {S,R,number,~,+,-,*,/}`
|    :math:`\mathcal{P}` is defined by the set of productions
|
|    :math:`E \rightarrow +~E~E \mid -~E~E \mid *~E~E \mid /~E~E \mid \sim E \mid S~E \mid R \mid number`


.. container:: figboxcenter

  |     AST --> Prog AST
  |     (1)  AST1.min = 0
  |     (2)  AST0.val = AST1.val
  |
  |     AST --> op AST AST
  |     (3)  AST1.min = AST0.min
  |     (4)  AST2.min = AST1.mout
  |     (5)  AST0.mout = AST2.mout
  |     (6)  AST0.val = AST1.val op AST2.val
  |          where op is one of +,-,\*,/
  |
  |     AST --> Store AST
  |     (7)  AST1.min = AST0.min
  |     (8)  AST0.mout = AST1.val
  |     (9)  AST0.val = AST1.val
  |
  |     AST --> Negate AST
  |     (10) AST1.min = AST0.min
  |     (11) AST0.mout = AST1.mout
  |     (12) AST0.val = -1 * AST1.val
  |
  |     AST --> Recall
  |     (13) AST0.val = AST0.min
  |     (14) AST0.mout = AST0.min
  |
  |     AST --> number
  |     (15) AST0.mout = AST0.min
  |     (16) AST0.val = number


  **Fig. 7.12** Attribute Grammar




.. container:: exercise

  **Practice 7.11**

  Justify the annotation of the tree given in figure 7.10 by stating which rule was used in assigning each of the attributes annotating the tree.

  :ref:`You can check your answer(s) here.<exercise7-11>`

Synthesized vs Inherited
===========================


.. container:: exercise

  **Practice 7.12**

  Is the *min* attribute synthesized or inherited?
  Is the *mout* attribute synthesized or inherited?

  :ref:`You can check your answer(s) here.<exercise7-12>`


------------------
Chapter Summary
------------------




-----------------
Review Questions
-----------------

  #. What is a term made up of in Prolog? Give examples of both simple and complex terms.
  #. What is a predicate in Prolog?
  #. In Standard ML you can pattern match a list using (h::t). How do you pattern match a list in Prolog?
  #. According to the definition of append, which are the input and the output parameters to the predicate?
  #. How do you get more possible answers for a question posed to Prolog?
  #. In the expression *X = 6 \* 5 + 4* why doesn't *X* equal 34 when evaluated in Prolog? What does *X* equal? What would you write to get *X* equal to 34?
  #. Provide the calls to lookup to look up 7 in the binary tree in example 7.10 and figure 7.4. Be sure to write down the whole term that is passed to lookup each time. You can consult the answer to practice problem 7.7 to see the definition of the lookup predicate.
  #. What symbol is used in place of the *:-* when writing a grammar in Prolog?
  #. What is a synthesized atrribute?
  #. What is an inherited attribute?

---------
Exercises
---------

In these early exercises you should work with the relative database presented at the beginning of this chapter.

  #.  Write a rule (i.e. predicate) that describes the relationship of a sibling. Then write a query to find out if Anne and Stephen are siblings. Then ask if Stephen and Michael are siblings. What is Prolog's response?
  #.  Write a rule that describes the relationship of a brother. Then write a query to find the brothers of sophusw. What is Prolog's response?
  #.  Write a rule that describes the relationship of a niece. Then write a query to find all nieces in the database. What is Prolog's response?
  #.  Write a predicate that describes the relationship of cousins.
  #.  Write a predicate that describes the ancestor relationship.
  #.  Write a predicate called odd that returns true if a list has an odd number of elements.
  #.  Write a predicate that checks to see if a list is a palindrome.
  #.  Show the substitution required to prove that sublist([a,b],[c,a,b]) is true. Use the definition in figure 7.3 and use the same method of proving it's true.
  #.  Write a predicate that computes the factorial of a number.
  #.  Write a predicate that computes the nth fibonacci number in exponential time complexity.
  #.  Write a predicate that computes the nth fibonacci number in linear time complexity.
  #.  Write a predicate that returns true if a third list is the result of zipping two others together. For instance,

      .. code-block:: prolog

        zipped([1,2,3],[a,b,c],[pair(1,a),pair(2,b),pair(3,c)])

      should return true since zipping [1,2,3] and [a,b,c] would yield the list of pairs given above.
  #.  Write a predicate that counts the number of times a specific atom appears in a list.
  #.  Write a predicate that returns true if a list is three copies of the same sublist. For instance, the predicate should return true if called as

      .. code-block:: prolog

        threecopies([a, b, c, a, b, c, a, b, c]).

      It should also return true if it were called like

      .. code-block:: prolog

        threecopies([a,b,c,d,a,b,c,d,a,b,c,d]).

  #.  Implement insert, lookup, and delete on a binary search tree. The structure of a binary search tree was discussed in this chapter. Your main *run* predicate should be this:

      .. code-block:: prolog

        buildtree(T) :- readln(L,_,_,_,lowercase), processlist(L,nil,T).

        run :- print('Please enter integers to build a tree: '), buildtree(T),
               print('Here is the tree:'), print(T), print('\n'),
               print('Now enter integers to delete: '), readln(L,_,_,_,lowercase),
               delListFromTree(L,T,DT), print(DT).

      The *run* predicate calls the *buildTree* predicate to build the binary search tree from the list read by the readline. If *5 8 2 10* is entered at the keyboard, *L* would be the list containing those numbers. To complete this project there should be at least three predicates: *insert*, *lookup*, and *delFromTree*.

      The *lookup* predicate was a practice problem and the solution is provided if you need it. The *insert* predicate is somewhat like the *lookup* predicate except that a new node is constructed when you reach a leaf. Deleting a node is simliar to looking it up except that if it is found, the tree is altered to delete the node. Deleting a node from a binary search tree has three cases.

        #. The node to delete is a leaf node. If this is the case, then deleting it is simple because you just return an empty tree. In figure 7.4 this occurs when 2,4,7, or 10 is deleted.
        #. The node to delete has one child. If this is the case, then the result of deleting the node is the subtree under the deleted node. In figure 7.4, if the 9 is deleted, then the 10 is just moved up to replace the 9 in the tree.
        #. The node to delete has two children. If this is the case, then you have to do two things. First, find the left-most value from the right subtree. Then, delete the left-most value from the right subtree and return a new tree with the left-most value of the right subtree at its root. Consider delete 5 from figure 7.4. The left-most value of the right subtree is 7. To delete 5 we put the 7 at the root of the tree and then delete 7 from the right subtree.

      To make this project easy, write it incrementally. Print the results as you go so you can see what works and what doesn't. The print predicate will print its argument while the nl predicate will print a newline. Don't start by writing the entire *run* predicate right away. Write one piece at a time, test it, and then move on to the next piece.

  #.  Implement a calculator prefix expression interpreter in Prolog as described in the section on attribute grammars in this chapter. The interpreter will read an expression from the keyboard and print its result. The interpreter should start with a *calc* predicate. Here is the *calc* predicate to get you started.

      .. code-block:: prolog

        calc :- readln(L,_,_,_,lowercase), preprocess(L,PreL), print(PreL), nl,
                expr(Tree,PreL,[]), print(Tree), nl, interpret(Tree,0,_,Val),
                print(Val), nl.

      The program reads a list of tokens from the keyboard. The *preprocess* predicate should take the list of values and add *num* tags to any number it finds in the list. This makes writing the grammar a lot easier. Any number like *6* in *L* should be replaced by *num((6)* in the list *PreL*. The *expr* predicate represents the start symbol of your grammar. Finally, the *interpret* predicate is the *attribute grammar* evaluation of the AST represented by *Tree*.

      To make this project easy, write it incrementally. Print the results as you go so you can see what works and what doesn't. The print predicate will print its argument while the nl predicate will print a newline.  Don't write the entire *calc* predicate right away. Write one piece, test it, and then move on to the next piece.

------------------------------
Solutions to Practice Problems
------------------------------

These are solutions to the practice problem s. You should only consult these answers after you have tried each of them for yourself first. Practice problems  are meant to help reinforce the material you have just read so make use of them.

.. _exercise7-1:

Solution to Practice Problem 7.1
================================

Terms include atoms and variables. Atoms include sophus, fred, sophusw, kent, johan, mads, etc.
Atoms start with a lowercase letter. Variables start with a capital letter and include X and Y from the example.

.. _exercise7-2:

Solution to Practice Problem 7.2
================================

  #.  *brother(X,Y) :- father(Z,X), father(Z,Y), male(X).*
  #.  *sister(X,Y) :- father(Z,X), father(Z,Y), female(X).*
  #.  *grandparent(X,Y) :- parent(X,Z), parent(Z,Y).*
  #.  *grandchild(X,Y) :- grandparent(Y,X).*

Grandparent and grandchild relationships are just the inverse of each other.

.. _exercise7-3:

Solution to Practice Problem 7.3
================================

The complexity of append is O(n) in the length of the first list.

.. _exercise7-4:

Solution to Practice Problem 7.4
================================


.. code-block:: prolog

  reverse([],[]).
  reverse([H|T],L) :- reverse(T,RT), append(RT,[H],L).

This predicate has O(:math:`n^2`) complexity since append is called n times and append is O(:math:`n`) complexity.

.. _exercise7-5:

Solution to Practice Problem 7.5
================================


.. code-block:: prolog

  reverseHelp([],Acc,Acc).
  reverseHelp([H|T], Acc, L) :- reverseHelp(T,[H|Acc],L).
  reverse(L,R):-reverseHelp(L,[],R).


.. _exercise7-6:

Solution to Practice Problem 7.6
================================


.. code-block:: prolog

  len([],0).
  len([_|T],N) :- len(T,M), N is M + 1.


.. _exercise7-7:

Solution to Practice Problem 7.7
================================


.. code-block:: prolog

  lookup(X,btnode(X,_,_)).
  lookup(X,btnode(Val,Left,_)) :- X < Val, lookup(X,Left).
  lookup(X,btnode(Val,_,Right)) :- X > Val, lookup(X,Right).


.. _exercise7-8:

Solution to Practice Problem 7.8
================================


.. container:: figboxcenter

   .. figure:: profparsetree.png

.. _exercise7-9:

Solution to Practice Problem 7.9
================================


.. code-block:: prolog

  sentence(K,L) :- subject(K,M), predicate(M,N), period(N,L).
  subject(K,L) :- determiner(K,M), noun(M,L).
  predicate(K,L) :- verb(K,M), subject(M,L).
  determiner(K,L) :- a(K,L); the(K,L).
  verb(K,L) :- discovered(K,L); jailed(K,L); walked(K,L).
  noun(K,L) :- professor(K,L); group(K,L); home(K,L).


.. _exercise7-10:

Solution to Practice Problem 7.10
=================================


.. code-block:: prolog

  sentence(sen(N,P)) --> subject(N), predicate(P), ['.'].
  subject(sub(D,N)) --> determiner(D), noun(N).
  predicate(pred(V,S)) --> verb(V), subject(S).
  determiner(det(the)) --> [the].
  determiner(det(a)) --> [a].
  noun(noun(professor)) --> [professor].
  noun(noun(home)) --> [home].
  noun(noun(group)) --> [group].
  verb(verb(walked)) --> [walked].
  verb(verb(discovered)) --> [discovered].
  verb(verb(jailed)) --> [jailed].


.. _exercise7-11:

Solution to Practice Problem 7.11
=================================

.. container:: figboxcenter

   .. figure:: attrtreejustify.png

.. _exercise7-12:

Solution to Practice Problem 7.12
=================================

The *val* attribute is synthesized. The *min* value is inherited. The *mout* value is synthesized.
