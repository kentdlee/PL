
.. container:: figboxright


   .. figure:: bookcover.jpg


---------------
Welcome!
---------------

Welcome to Foundations of Programming Languages Second Edition by Kent D. Lee. If you are looking for the First Edition website, please go to the address `https://kentdlee.github.io/PL1 <https://kentdlee.github.io/PL1>`_. This text, available from `Springer <http://www.amazon.com/Foundations-Programming-Languages-Undergraduate-Computer/dp/3319133136/ref=sr_1_2?ie=UTF8&qid=1423340935&sr=8-2&keywords=kent+d+lee>`_, covers material on the design and implementation of programming languages, focusing on the three paradigms of prorgramming: imperative, functional, and logic programming.

Concepts covered in the text include syntax specification, lexical analysis, parsing, abstract syntax, compilation, disassembly, interpretation, functional programming, logic programming, type inference, and type inference rules. The text covers several programming languages including assembly language programming, C++, Standard ML, and Prolog.

This text uses and extends the JCoCo Virtual Machine. JCoCo is based on the Python Virtual Machine version 3.2. JCoCo, and its Python disassember, were written to illustrate assembly language programming on a virtual machine. The text both uses JCoCo so students can learn about assembly language programming, and extends JCoCo so students can learn about virtual machine implementations. The `JCoCo website <https://kentdlee.github.io/JCoCoPages>`_ describes the JCoCo virtual machine and the Github website http://github.com/kentdlee/JCoCo provides the source code for JCoCo.

An older C++ version of the CoCo code is available at `https://kentdlee.github.io/CoCoPages <https://kentdlee.github.io/CoCoPages/>`_. 

In addition, this text uses CoCo as a target language for implementing a compiler of Standard ML. The code for this project is available on Github at http://github.com/kentdlee/MLComp. The text extends the MLComp compiler to compile a robust subset of Standard ML.

The final chapter of this text covers type inference in Standard ML and provides the description and partial implementation of the Standard ML type inference system written in Prolog. This code is included in the MLComp Github project. The text extends the type checker to cover a more complete subset of the language.

Solutions to JCoCo and MLComp can be provided to instructors of qualified universities or colleges. These solutions cover chapters 4, 6, and 8 of the text.
In addition, solutions to exercises from chapters 1, 2, 3, 5 and 7 can be provided to teachers upon request.
Teachers must provide proof that they are teaching at a university or college.

This website provides access to figures and example code from the text as well as practice problems, review questions, and exercises.

Errata
========

Unfortunately there are several errata in the second edition. Most are minor and were introduced when removing some formatting
from the first edition. Here they are in order of the textbook

  * Page 230, Solution to Practice Problem 5.8 is correct on these web pages.

  * Page 231, Solution to Practice Problem 5.10 is correct on these web pages.

  * Page 242, fig. 6.5 is correct on these web pages.

  * Page 268, fig. 6.34 caption should read "test7.sml".

  * Page 271, figure 6.40 should be as given on these web pages.

  * Page 271, figure 6.41 should be as given on these web pages.

  * Page 275, exercise 7, the example code is correct on these web pages and in test20.sml.

  * Page 329, review question 8, the example code is correct on these web pages.

  * Page 330, exercise 1, the sample program is correct on these web pages and in test20.sml.

  * Page 331, exercise 3, the sample program is correct on these web pages and in test12.sml.




Contents
========

.. toctree::
   :maxdepth: 4
   :numbered:

   introduction.rst

   syntax.rst

   assembly.rst

   oop.rst

   functional.rst

   usingsml.rst

   prolog.rst

   typeinference.rst

..   bib.rst

..   appendices.rst
