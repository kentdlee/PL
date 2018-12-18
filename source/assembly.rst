.. _assemblychap:

=========================================
Assembly Language
=========================================

-------------------------------------
Overview of the JCoCo VM
-------------------------------------

.. container:: figboxcenter

   .. _cocofig:

   .. figure:: coco.png

  **Fig 3.1** The JCoCo Virtual Machine


-----------------------------------
Getting Started
-----------------------------------

.. _runningdis:

Running the Disassembler
===========================

  .. code-block:: python
      :linenos:

      from disassembler import *
      import sys

      def main():
          x=5
          y=6
          z=x+y
          print(z)

      if len(sys.argv) == 1:
        main()
      else:
        disassemble(main)

.. code-block:: text
    :linenos:

    MyComputer> python3.2 addtwo.py 1
    Function: main/0
    Constants: None, 5, 6
    Locals: x, y, z
    Globals: print
    BEGIN
              LOAD_CONST                     1
              STORE_FAST                     0
              LOAD_CONST                     2
              STORE_FAST                     1
              LOAD_FAST                      0
              LOAD_FAST                      1
              BINARY_ADD
              STORE_FAST                     2
              LOAD_GLOBAL                    0
              LOAD_FAST                      2
              CALL_FUNCTION                  1
              POP_TOP
              LOAD_CONST                     0
              RETURN_VALUE
    END
    MyComputer> python3.2 addtwo.py 1 > addtwo.casm

.. _runningcoco:

Running JCoCo
=========================

.. code-block:: text
    :linenos:

    MyComputer> coco -v addtwo.casm
    Function: main/0
    Constants: None, 5, 6
    Locals: x, y, z
    Globals: print
    BEGIN
              LOAD_CONST                     1
              STORE_FAST                     0
              LOAD_CONST                     2
              STORE_FAST                     1
              LOAD_FAST                      0
              LOAD_FAST                      1
              BINARY_ADD
              STORE_FAST                     2
              LOAD_GLOBAL                    0
              LOAD_FAST                      2
              CALL_FUNCTION                  1
              POP_TOP
              LOAD_CONST                     0
              RETURN_VALUE
    END

    11
    MyComputer> coco addtwo.casm
    11
    MyComputer>



.. code-block:: text

    MyComputer> python3.2 addtwo.py 1 > addtwo.casm
    MyComputer> coco addtwo.casm

----------------
Input/Output
----------------

.. _pythonio:

Python I/O
===========


.. code-block:: python
    :linenos:

    import disassembler

    def main():
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        print(name + ", a year from now you will be", age+1, "years old.")

    #main()
    disassembler.disassemble(main)


.. _cocoio:

CoCo I/O
==============



.. container:: figboxcenter

  .. code-block:: text
      :linenos:

      Function: main/0
      Constants: None,
        "Enter your name: ", "Enter your age: ",
        ", a year from now you will be",
        1, "years old."
      Locals: name, age
      Globals: input, int, print
      BEGIN
                LOAD_GLOBAL                    0
                LOAD_CONST                     1
                CALL_FUNCTION                  1
                STORE_FAST                     0
                LOAD_GLOBAL                    1
                LOAD_GLOBAL                    0
                LOAD_CONST                     2
                CALL_FUNCTION                  1
                CALL_FUNCTION                  1
                STORE_FAST                     1
                LOAD_GLOBAL                    2
                LOAD_FAST                      0
                LOAD_CONST                     3
                BINARY_ADD
                LOAD_FAST                      1
                LOAD_CONST                     4
                BINARY_ADD
                LOAD_CONST                     5
                CALL_FUNCTION                  3
                POP_TOP
                LOAD_CONST                     0
                RETURN_VALUE
      END

  **Fig 3.2** JCoCo I/O




.. container:: exercise

  **Practice 3.1**

  The code in :ref:`cocoio` is a bit wasteful which often happens when compiling a program written in a higher level language. Optimize the code in :ref:`cocoio` so it contains fewer instructions.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-1>`

.. _ifthenelsecode:

------------------------
If-Then-Else Statements
------------------------

.. code-block:: python
    :linenos:

    import disassembler

    def main():
        x = 5
        y = 6
        if x > y:
            z = x
        else:
            z = y

        print(z)

    disassembler.disassemble(main)


.. container:: figboxcenter


  .. code-block:: text
      :linenos:

      Function: main/0
      Constants: None, 5, 6
      Locals: x, y, z
      Globals: print
      BEGIN
                LOAD_CONST                     1
                STORE_FAST                     0
                LOAD_CONST                     2
                STORE_FAST                     1
                LOAD_FAST                      0
                LOAD_FAST                      1
                COMPARE_OP                     4
                POP_JUMP_IF_FALSE        label00
                LOAD_FAST                      0
                STORE_FAST                     2
                JUMP_FORWARD             label01
      label00:  LOAD_FAST                      1
                STORE_FAST                     2
      label01:  LOAD_GLOBAL                    0
                LOAD_FAST                      2
                CALL_FUNCTION                  1
                POP_TOP
                LOAD_CONST                     0
                RETURN_VALUE
      END

  **Fig 3.3** If-Then-Else assembly

.. code-block:: text
    :linenos:

      onelabel:  LOAD_FAST                     1
                 STORE_FAST                    2
      twolabel:
    threelabel: LOAD_GLOBAL                    0

.. _cocoassembled:

Assembled CoCo
================

.. container:: figboxcenter

  .. code-block:: text
      :linenos:

      Function: main/0
      Constants: None, 5, 6
      Locals: x, y, z
      Globals: print
      BEGIN
                LOAD_CONST                     1
                STORE_FAST                     0
                LOAD_CONST                     2
                STORE_FAST                     1
                LOAD_FAST                      0
                LOAD_FAST                      1
                COMPARE_OP                     4
                POP_JUMP_IF_FALSE             11
                LOAD_FAST                      0
                STORE_FAST                     2
                JUMP_FORWARD                  13
                LOAD_FAST                      1
                STORE_FAST                     2
                LOAD_GLOBAL                    0
                LOAD_FAST                      2
                CALL_FUNCTION                  1
                POP_TOP
                LOAD_CONST                     0
                RETURN_VALUE
      END

  **Fig 3.4** Assembled code


.. container:: exercise

  **Practice 3.2**

  Without touching the code that compares the two values, the assembly in :ref:`cocoassembled` can be optimized to remove at least three instructions. Rewrite the code to remove at least three instructions from this code. With a little more work, five instructions could be removed.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-2>`

If-Then Statements
====================


.. code-block:: python

    import disassembler

    def main():
        x = 5
        y = 6
        if x > y:
            print(x)

        print(y)

    disassembler.disassemble(main)

.. _cocoifthenasm:

CoCo If-Then Assembly
======================

.. container:: figboxcenter

    .. code-block:: text
        :linenos:

        Function: main/0
        Constants: None, 5, 6
        Locals: x, y
        Globals: print
        BEGIN
                  LOAD_CONST                     1
                  STORE_FAST                     0
                  LOAD_CONST                     2
                  STORE_FAST                     1
                  LOAD_FAST                      0
                  LOAD_FAST                      1
                  COMPARE_OP                     4
                  POP_JUMP_IF_FALSE        label00
                  LOAD_GLOBAL                    0
                  LOAD_FAST                      0
                  CALL_FUNCTION                  1
                  POP_TOP
                  JUMP_FORWARD             label00
        label00:  LOAD_GLOBAL                    0
                  LOAD_FAST                      1
                  CALL_FUNCTION                  1
                  POP_TOP
                  LOAD_CONST                     0
                  RETURN_VALUE
        END

    **Fig 3.5** If-Then assembly



.. container:: exercise

  **Practice 3.3**

  Rewrite the code in :ref:`cocoifthenasm` so it executes with the same result using *POP_JUMP_IF_TRUE* instead of the jump if false instruction. Be sure to optimize your code when you write it so there are no unnecessary instructions.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-3>`


.. _whileloops:

--------------
While Loops
--------------

.. code-block:: python
    :linenos:

    import disassembler

    def main():
        f = 8
        i = 1
        j = 1
        n = 1
        while n < f:
            n = n + 1
            tmp = j
            j = j + i
            i = tmp

        print("Fibonacci("+str(n)+") is",i)

    disassembler.disassemble(main)


.. container:: figboxcenter

    .. code-block:: text
        :linenos:

        Function: main/0
        Constants: None, 8, 1, "Fibonacci(", ") is"
        Locals: f, i, j, n, tmp
        Globals: print, str
        BEGIN
                  LOAD_CONST                     1
                  STORE_FAST                     0
                  LOAD_CONST                     2
                  STORE_FAST                     1
                  LOAD_CONST                     2
                  STORE_FAST                     2
                  LOAD_CONST                     2
                  STORE_FAST                     3
                  SETUP_LOOP               label02
        label00:  LOAD_FAST                      3
                  LOAD_FAST                      0
                  COMPARE_OP                     0
                  POP_JUMP_IF_FALSE        label01
                  LOAD_FAST                      3
                  LOAD_CONST                     2
                  BINARY_ADD
                  STORE_FAST                     3
                  LOAD_FAST                      2
                  STORE_FAST                     4
                  LOAD_FAST                      2
                  LOAD_FAST                      1
                  BINARY_ADD
                  STORE_FAST                     2
                  LOAD_FAST                      4
                  STORE_FAST                     1
                  JUMP_ABSOLUTE            label00
        label01:  POP_BLOCK
        label02:  LOAD_GLOBAL                    0
                  LOAD_CONST                     3
                  LOAD_GLOBAL                    1
                  LOAD_FAST                      3
                  CALL_FUNCTION                  1
                  BINARY_ADD
                  LOAD_CONST                     4
                  BINARY_ADD
                  LOAD_FAST                      1
                  CALL_FUNCTION                  2
                  POP_TOP
                  LOAD_CONST                     0
                  RETURN_VALUE
        END

    **Fig 3.6** While loop assembly


.. container:: exercise

  **Practice 3.4**

  Write a short program that tests the use of the *BREAK_LOOP* instruction. You don't have to write a while loop to test this. Simply write some code that uses a *BREAK_LOOP* and prints something to the screen to verify that it worked.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-4>`

-------------------
Exception Handling
-------------------

.. code-block:: python
    :linenos:

    import disassembler

    def main():
        try:
            x = float(input("Enter a number: "))
            y = float(input("Enter a number: "))
            z = x / y
            print(x,"/",y,"=",z)
        except Exception as ex:
            print(ex)

    disassembler.disassemble(main)


.. container:: figboxcenter

    .. code-block:: text
        :linenos:

        Function: main/0
        Constants: None,
            "Enter a number: ", "/", "="
        Locals: x, y, z, ex
        Globals: float, input, print, Exception
        BEGIN
                  SETUP_EXCEPT             label00
                  LOAD_GLOBAL                    0
                  LOAD_GLOBAL                    1
                  LOAD_CONST                     1
                  CALL_FUNCTION                  1
                  CALL_FUNCTION                  1
                  STORE_FAST                     0
                  LOAD_GLOBAL                    0
                  LOAD_GLOBAL                    1
                  LOAD_CONST                     1
                  CALL_FUNCTION                  1
                  CALL_FUNCTION                  1
                  STORE_FAST                     1
                  LOAD_FAST                      0
                  LOAD_FAST                      1
                  BINARY_TRUE_DIVIDE
                  STORE_FAST                     2
                  LOAD_GLOBAL                    2
                  LOAD_FAST                      0
                  LOAD_CONST                     2
                  LOAD_FAST                      1
                  LOAD_CONST                     3
                  LOAD_FAST                      2
                  CALL_FUNCTION                  5
                  POP_TOP
                  POP_BLOCK
                  JUMP_FORWARD             label03
        label00:  DUP_TOP
                  LOAD_GLOBAL                    3
                  COMPARE_OP                    10
                  POP_JUMP_IF_FALSE        label02
                  POP_TOP
                  STORE_FAST                     3
                  POP_TOP
                  SETUP_FINALLY            label01
                  LOAD_GLOBAL                    2
                  LOAD_FAST                      3
                  CALL_FUNCTION                  1
                  POP_TOP
                  POP_BLOCK
                  POP_EXCEPT
                  LOAD_CONST                     0
        label01:  LOAD_CONST                     0
                  STORE_FAST                     3
                  DELETE_FAST                    3
                  END_FINALLY
                  JUMP_FORWARD             label03
        label02:  END_FINALLY
        label03:  LOAD_CONST                     0
                  RETURN_VALUE
        END

    **Fig 3.7** Exception handling assembly



.. container:: exercise

  **Practice 3.5**

  Write a short program that tests creating an exception, raising it, and printing the handled exception. Write this as a JCoCo program without using the disassembler.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-5>`

-------------------
List Constants
-------------------

.. code-block:: python
    :linenos:

    import disassembler

    def main():
        lst = ["hello","world"]
        print(lst)

    disassembler.disassemble(main)

.. container:: figboxcenter

    .. code-block:: text
        :linenos:

        Function: main/0
        Constants: None, "hello", "world"
        Locals: lst
        Globals: print
        BEGIN
                  LOAD_CONST                     1
                  LOAD_CONST                     2
                  BUILD_LIST                     2
                  STORE_FAST                     0
                  LOAD_GLOBAL                    0
                  LOAD_FAST                      0
                  CALL_FUNCTION                  1
                  POP_TOP
                  LOAD_CONST                     0
                  RETURN_VALUE
        END

    **Fig 3.8** Assembly for building a list


.. _methodcall:

---------------------
Calling a Method
---------------------

.. code-block:: python
    :linenos:

    import disassembler

    def main():
        s = input("Enter a list of integers:")
        lst = s.split()

        print(lst)

    disassembler.disassemble(main)


.. container:: figboxcenter

    .. code-block:: text
        :linenos:

        Function: main/0
        Constants: None, "Enter a list of integers:"
        Locals: s, lst
        Globals: input, split, print
        BEGIN
                  LOAD_GLOBAL                    0
                  LOAD_CONST                     1
                  CALL_FUNCTION                  1
                  STORE_FAST                     0
                  LOAD_FAST                      0
                  LOAD_ATTR                      1
                  CALL_FUNCTION                  0
                  STORE_FAST                     1
                  LOAD_GLOBAL                    2
                  LOAD_FAST                      1
                  CALL_FUNCTION                  1
                  POP_TOP
                  LOAD_CONST                     0
                  RETURN_VALUE
        END

    **Fig 3.9** Assembly for calling a method


.. container:: exercise

  **Practice 3.6**

  Normally, if you want to add to numbers together in Python, like 5 and 6, you write 5+6. This corresponds to using the *BINARY_ADD* instruction in JCoCo which in turn calls the magic method *__add__* with the method call 5.__add__(6). Write a short JCoCo program where you add two integers together without using the *BINARY_ADD* instruction. Print the result to the screen.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-6>`


-----------------------
Iterating Over a List
-----------------------

.. code-block:: python
    :linenos:

    from disassembler import *

    def main():
        x = input("Enter a list: ")
        lst = x.split()

        for b in lst:
            print(b)

    disassemble(main)

.. container:: figboxcenter

    .. code-block:: text
        :linenos:

        Function: main/0
        Constants: None, "Enter a list: "
        Locals: x, lst, b
        Globals: input, split, print
        BEGIN
                  LOAD_GLOBAL                    0
                  LOAD_CONST                     1
                  CALL_FUNCTION                  1
                  STORE_FAST                     0
                  LOAD_FAST                      0
                  LOAD_ATTR                      1
                  CALL_FUNCTION                  0
                  STORE_FAST                     1
                  SETUP_LOOP               label02
                  LOAD_FAST                      1
                  GET_ITER
        label00:  FOR_ITER                 label01
                  STORE_FAST                     2
                  LOAD_GLOBAL                    2
                  LOAD_FAST                      2
                  CALL_FUNCTION                  1
                  POP_TOP
                  JUMP_ABSOLUTE            label00
        label01:  POP_BLOCK
        label02:  LOAD_CONST                     0
                  RETURN_VALUE
        END

    **Fig 3.10** List iteration assembly


.. container:: exercise

  **Practice 3.7**

  Write a JCoCo program that gets a string from the user and iterates over the characters of the string, printing them to the screen.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-7>`

.. _lazyeval:

----------------------------------
Range Objects and Lazy Evaluation
----------------------------------

.. code-block:: python
    :linenos:

    from disassembler import *

    def main():
        x = input("Enter a list: ")
        lst = x.split()

        for i in range(len(lst)-1,-1,-1):
            print(lst[i])

    disassemble(main)

.. container:: figboxcenter

    .. code-block:: text
        :linenos:

        Function: main/0
        Constants: None, "Enter a list: ", 1, -1, -1
        Locals: x, lst, i
        Globals: input, split, range, len, print
        BEGIN
                  LOAD_GLOBAL                    0
                  LOAD_CONST                     1
                  CALL_FUNCTION                  1
                  STORE_FAST                     0
                  LOAD_FAST                      0
                  LOAD_ATTR                      1
                  CALL_FUNCTION                  0
                  STORE_FAST                     1
                  SETUP_LOOP               label02
                  LOAD_GLOBAL                    2
                  LOAD_GLOBAL                    3
                  LOAD_FAST                      1
                  CALL_FUNCTION                  1
                  LOAD_CONST                     2
                  BINARY_SUBTRACT
                  LOAD_CONST                     3
                  LOAD_CONST                     4
                  CALL_FUNCTION                  3
                  GET_ITER
        label00:  FOR_ITER                 label01
                  STORE_FAST                     2
                  LOAD_GLOBAL                    4
                  LOAD_FAST                      1
                  LOAD_FAST                      2
                  BINARY_SUBSCR
                  CALL_FUNCTION                  1
                  POP_TOP
                  JUMP_ABSOLUTE            label00
        label01:  POP_BLOCK
        label02:  LOAD_CONST                     0
                  RETURN_VALUE
        END

    **Fig 3.11** Range assembly


.. _closures:

----------------------------------
Functions and Closures
----------------------------------

.. code-block:: python
  :linenos:

  def main():
    x = 10
    def f(x):
      def g():
        return x
      return g
    print(f(3)())
  #main()
  disassembler.disassemble(main)

.. _nested-fun:

Nested Functions Assembly
===========================
.. container:: figboxcenter

    .. code-block:: text
        :linenos:

        Function: main/0
            Function: f/1
                Function: g/0
                Constants: None
                FreeVars: x
                BEGIN
                          LOAD_DEREF    0
                          RETURN_VALUE
                END
            Constants: None, code(g)
            Locals: x, g
            CellVars: x
            BEGIN
                      LOAD_CLOSURE      0
                      BUILD_TUPLE       1
                      LOAD_CONST        1
                      MAKE_CLOSURE      0
                      STORE_FAST        1
                      LOAD_FAST         1
                      RETURN_VALUE
            END
        Constants: None, 10, code(f), 3
        Locals: x, f
        Globals: print
        BEGIN
                  LOAD_CONST            1
                  STORE_FAST            0
                  LOAD_CONST            2
                  MAKE_FUNCTION         0
                  STORE_FAST            1
                  LOAD_GLOBAL           0
                  LOAD_FAST             1
                  LOAD_CONST            3
                  CALL_FUNCTION         1
                  CALL_FUNCTION         0
                  CALL_FUNCTION         1
                  POP_TOP
                  LOAD_CONST            0
                  RETURN_VALUE
        END

    **Fig 3.12** Nested functions assembly


.. _nestedfig:

Nested Function
=================

.. container:: figboxcenter

   .. figure:: nested.png

  **Fig 3.13** Execution of nested.casm



.. container:: exercise

  **Practice 3.8**

  The program in :ref:`nested-fun` would work just fine without the cell. The variable *x* could refer directly to the 3 in both the *f* and *g* functions without any ramifications. Yet, a cell variable is needed in some circumstances. Can you come up with an example where a cell variable is absolutely needed?

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-8>`

.. _recursion:

-----------
Recursion
-----------

.. code-block:: python
    :linenos:

    import disassembler

    def factorial(n):
        if n==0:
            return 1

        return n*factorial(n-1)

    def main():
        print(factorial(5))

    disassembler.disassemble(factorial)
    disassembler.disassemble(main)


.. _cocorecursion:

CoCo Recursion Assembly
=========================

.. container:: figboxcenter

    .. code-block:: text
        :linenos:

        Function: factorial/1
        Constants: None, 0, 1
        Locals: n
        Globals: factorial
        BEGIN
                  LOAD_FAST                      0
                  LOAD_CONST                     1
                  COMPARE_OP                     2
                  POP_JUMP_IF_FALSE        label00
                  LOAD_CONST                     2
                  RETURN_VALUE
        label00:  LOAD_FAST                      0
                  LOAD_GLOBAL                    0
                  LOAD_FAST                      0
                  LOAD_CONST                     2
                  BINARY_SUBTRACT
                  CALL_FUNCTION                  1
                  BINARY_MULTIPLY
                  RETURN_VALUE
        END
        Function: main/0
        Constants: None, 5
        Globals: print, factorial
        BEGIN
                  LOAD_GLOBAL                    0
                  LOAD_GLOBAL                    1
                  LOAD_CONST                     1
                  CALL_FUNCTION                  1
                  CALL_FUNCTION                  1
                  POP_TOP
                  LOAD_CONST                     0
                  RETURN_VALUE
        END

    **Fig 3.14** Recursion assembly


.. container:: exercise

  **Practice 3.9**

  Draw a picture of the run-time stack just before the instruction on line 11 of :ref:`cocorecursion` is executed. Use :ref:`nestedfig` as a guide to how you draw this picture. Be sure to include the code, the values of *n*, and the *PC* values.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-9>`


.. _classesasm:

---------------------------------
Support for Classes and Objects
---------------------------------

.. code-block:: python
    :linenos:

    import disassembler
    class Dog:
      def __init__(self):
        self.food = 0
      def eat(self):
        self.food = self.food + 1
      def speak(self):
        if self.food > 2:
          print("I am happy!")
        else:
          print("I am hungry!!!")
        self.food=self.food - 1
    def main():
      mesa  = Dog()
      mesa.eat()
      mesa.speak()
      mesa.eat()
      mesa.eat()
      mesa.speak()
    disassembler.disassemble(Dog)
    disassembler.disassemble(main)



.. container:: figboxcenter

    .. code-block:: text
        :linenos:

        Class: Dog
        BEGIN
           Function: eat/1
           Constants: None, 1
           Locals: self
           Globals: food
           BEGIN
                     LOAD_FAST     0
                     LOAD_ATTR     0
                     LOAD_CONST    1
                     BINARY_ADD
                     LOAD_FAST     0
                     STORE_ATTR    0
                     LOAD_CONST    0
                     RETURN_VALUE
           END
           Function: __init__/1
           Constants: None, 0
           Locals: self
           Globals: food
           BEGIN
                     LOAD_CONST  1
                     LOAD_FAST   0
                     STORE_ATTR  0
                     LOAD_CONST  0
                     RETURN_VALUE
           END
           # speak function omitted
        END
        Function: main/0
        Constants: None
        Locals: mesa
        Globals: Dog, eat, speak
        BEGIN
                  LOAD_GLOBAL   0
                  CALL_FUNCTION 0
                  STORE_FAST    0
                  LOAD_FAST     0
                  LOAD_ATTR     1
                  CALL_FUNCTION 0
                  POP_TOP
                  ...
                  RETURN_VALUE
        END

    **Fig 3.15** The dog class


.. container:: exercise

  **Practice 3.10**

  In this section it was stated that every object consists of a dictionary which holds the attributes of the object. What is stored in the dictioinary of the object that mesa refers to in this section?

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-10>`


Inheritance
======================

.. code-block:: python
    :linenos:

    import disassembler
    class Dog:
      def __init__(self):
        self.food = 0
      def eat(self):
        self.food = self.food + 1
      def speak(self):
        if self.food > 2:
          print("I am happy!")
        else:
          print("I am hungry!!!")
        self.food=self.food - 1
    def main():
      mesa  = Dog()
      mesa.eat()
      mesa.speak()
      mesa.eat()
      mesa.eat()
      mesa.speak()
    disassembler.disassemble(Dog)
    disassembler.disassemble(main)

.. container:: figboxcenter

  .. code-block:: text
      :linenos:

      Class: Animal
      BEGIN
          Function: __init__/2
          Constants: None, 0
          Locals: self, name
          Globals: name, food
          BEGIN
                    LOAD_FAST   1
                    LOAD_FAST   0
                    STORE_ATTR  0
                    LOAD_CONST  1
                    LOAD_FAST   0
                    STORE_ATTR  1
                    LOAD_CONST  0
                    RETURN_VALUE
          END
          Function: eat/1
          Constants: None, 1
          Locals: self
          Globals: food
          BEGIN
                    LOAD_FAST  0
                    ...
                    RETURN_VALUE
          END
          Function: speak/1
          Constants: None, "is an animal"
          Locals: self
          Globals: print, name
          BEGIN
                    LOAD_GLOBAL  0
                    ...
                    RETURN_VALUE
          END
      END

  **Fig 3.16** Inheritance in JCoCo - part 1

.. container:: figboxcenter

  .. code-block:: text
      :linenos:

      Class: Dog(Animal)
      BEGIN
          Function: __init__/2
          Constants: None
          Locals: self, name
          FreeVars: __class__
          Globals: super, __init__
          BEGIN
                    LOAD_GLOBAL                    0
                    CALL_FUNCTION                  0
                    LOAD_ATTR                      1
                    LOAD_FAST                      1
                    CALL_FUNCTION                  1
                    POP_TOP
                    LOAD_CONST                     0
                    RETURN_VALUE
          END
          Function: speak/1
          Constants: None, "says woof!"
          Locals: self
          Globals: print, name
          BEGIN
                    LOAD_GLOBAL                    0
                    ...
                    RETURN_VALUE
          END
      END
      Function: main/0
      Constants: None, "Mesa"
      Locals: mesa
      Globals: Dog, eat, speak
      BEGIN
                LOAD_GLOBAL                    0
                LOAD_CONST                     1
                CALL_FUNCTION                  1
                STORE_FAST                     0
                ...
                RETURN_VALUE
      END


  **Fig 3.17** Inheritance in JCoCo - part 2


.. container:: exercise

  **Practice 3.11**

  Code was omitted in figures 3.16 and 3.17 for brevity in the chapter. Pick a method and complete the assembly code according to the original Python code from which it is derived.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-11>`


Dynamically Created Classes
===============================

.. code-block:: python
    :linenos:

    import disassembler

    def main():

      class Dog:
        dogNumber = 0

        def __init__(self,name):
          self.name = name
          self.id = Dog.dogNumber
          Dog.dogNumber += 1

        def speak(self):
          print("Dog number: ", self.id)

      x = Dog("Mesa")
      y = Dog("Sequoia")

      x.speak()
      y.speak()

    disassembler.disassemble(main)

.. container:: figboxcenter


  .. code-block:: text
      :linenos:

      Function: main/0
          Function: Dog/1
              Function: __init__/2
              Constants: None, 1
              Locals: self, name
              FreeVars: Dog
              Globals: name, dogNumber, id
              BEGIN
                        LOAD_FAST                      1
                        LOAD_FAST                      0
                        STORE_ATTR                     0
                        LOAD_DEREF                     0
                        LOAD_ATTR                      1
                        LOAD_FAST                      0
                        STORE_ATTR                     2
                        ...
                        RETURN_VALUE
              END
              Function: speak/1
              Constants: None, "Dog number: "
              Locals: self
              Globals: print, id
              BEGIN
                        LOAD_GLOBAL                    0
                        ...
                        RETURN_VALUE
              END
          Constants: 0, code(__init__), code(speak), None
          Locals: __locals__
          FreeVars: Dog
          Globals: __name__, __module__, dogNumber, __init__, speak
          BEGIN
                    LOAD_FAST                      0
                    STORE_LOCALS
                    LOAD_NAME                      0
                    STORE_NAME                     1
                    LOAD_CONST                     0
                    STORE_NAME                     2
                    LOAD_CLOSURE                   0
                    BUILD_TUPLE                    1
                    LOAD_CONST                     1
                    MAKE_CLOSURE                   0
                    STORE_NAME                     3
                    LOAD_CONST                     2
                    MAKE_FUNCTION                  0
                    STORE_NAME                     4
                    LOAD_CONST                     3
                    RETURN_VALUE
          END

        Constants: None, code(Dog), "Dog", "Mesa", "Sequoia"
        Locals: x, y
        CellVars: Dog
        Globals: speak
        BEGIN
                  LOAD_BUILD_CLASS
                  LOAD_CLOSURE                   0
                  BUILD_TUPLE                    1
                  LOAD_CONST                     1
                  MAKE_CLOSURE                   0
                  LOAD_CONST                     2
                  CALL_FUNCTION                  2
                  STORE_DEREF                    0
                  LOAD_DEREF                     0
                  LOAD_CONST                     3
                  CALL_FUNCTION                  1
                  STORE_FAST                     0
                  ...
                  RETURN_VALUE
        END

  **Fig 3.18 and Fig 3.19** Dynamically created class


.. container:: exercise

  **Practice 3.12**

  In some detail, describe the contents of the operand stack before and after the built-in class builder function is called to create a class instance.

  :ref:`You can check your answer(s) at the end of the chapter.<exercise3-12>`

---------------------
Chapter Summary
---------------------


----------------
Review Questions
----------------

    #. How do the Python virtual machine and JCoCo differ? Name three differences between the two implementations.
    #. What is a disassembler?
    #. What is an assembler?
    #. What is a stack frame? Where are they stored? What goes inside a stack frame?
    #. What is the purpose of the block stack and where is it stored?
    #. What is the purpose of the Program Counter?
    #. Name an instruction that is responsible for creating a list object and describe how it works.
    #. Describe the execution of the *STORE_FAST* and *LOAD_FAST* instructions.
    #. How can JCoCo read a line of input from the keyboard?
    #. What is the difference between a disassembled Python program and an assembled JCoCo program? Provide a short example and point out the differences.
    #. When a Python while loop is implemented in JCoCo, what is the last instruction of the loop and what is its purpose?
    #. What do exception handling and loops have in common in the JCoCo implementation?
    #. What is lazy evaluation and why is it important to Python and JCoCo?
    #. What is a closure and why are closures needed?
    #. How do you create an instance of a class in JCoCo? What instructions must be executed to create objects?
    #. Write a class, using JCoCo, and create some instances of the class.

-----------
Exercises
-----------

    #. Consulting the JCoCo assembly language program in :ref:`the solution to exercise 3.2<exercise3-2>`, provide the contents of the operand stack after each instruction is executed.
    #. Write a JCoCo program which reads an integer from the user and then creates a list of all the even numbers from 0 up to and including that integer. The program should conclude printing the list to the screen. Test your program with JCoCo to be sure it works.
    #. With as few instructions as possible add some exception handling to the previous exercise to print "You didn't enter an integer!" if the user fails to enter an integer in their program.
    #. In as few instructions as possible write a JCoCo program that computes the sum of the  rst n integers where the non-negative n is read from the user.
    #. Write a recursive JCoCo program that adds up the  rst n integers where n is read from the user. Re- member, there must be a base case that comes  rst in this function and the recursive case must be called on something smaller which is used in computing the solution to the whole problem.
    #. Write a Rational class that can be used to add and multiply fractions together. A Rational number has an integer numerator and denominator. The __add__ method is needed to add together Rationals. The __mul__ method is for multiplication. To get fractions in reduced format you may want to find the greatest common divisor of the numerator and the denominator when creating a Rational number. Write this code in Python first, then disassemble it to get started with this assignment.

       You may wish to write the greatest common divisor function, gcd, as part of the class although no self parameter is needed for this function. The greatest common divisor of two integers, 𝑥 and 𝑦, can be defined recursively. If 𝑦 is zero then 𝑥 is the greatest common divisor. Otherwise, the greatest common divisor of 𝑥 and 𝑦 is equal to the greatest common divisor of 𝑦 and the remainder 𝑥 divided by 𝑦. Write a recursive function called gcd to determine the greatest common divisor of 𝑥 and 𝑦.

       Disassemble the program and then look for ways of shortening up the JCoCo assembly language program. Use the following main program in your code.

        .. code-block:: text
            :linenos:

            import disassembler
            def main ():
            x = Rational(1,2)
            y = Rational(2,3)
            print(x+y)
            print(x*y)
            disassembler.disassemble(Rational)
            disassembler.disassemble(main)

       From this code you should get the following output which matches the output you should get had this been a Python program. Remember to use Python 3.2 when disassembling your program. And, remember to turn in as short a program as possible while getting this output below from the main program given above.

        .. code-block:: text
            :linenos:

            7/6 1/3

------------------------------
Solutions to Practice Problems
------------------------------


These are solutions to the practice problems. You should only consult these answers after you have tried each of them for yourself first. Practice problems are meant to help reinforce the material you have just read so make use of them.


.. _exercise3-1:

Solution to Practice Problem 3.1
================================
The assembly code in :ref:`cocoio` blindly pops the *None* at the end and then pushes *None* again before returning from main. This can be eliminated resulting in two fewer instructions. This would also mean that *None* is not needed in the constants, but this was not eliminated below.

.. code-block:: text

        Function: main/0
        Constants: None,
            "Enter your name: ", "Enter your age: ",
            ", a year from now you will be",
            1, "years old."
        Locals: name, age
        Globals: input, int, print
        BEGIN
                  LOAD_GLOBAL                    0
                  LOAD_CONST                     1
                  CALL_FUNCTION                  1
                  STORE_FAST                     0
                  LOAD_GLOBAL                    1
                  LOAD_GLOBAL                    0
                  LOAD_CONST                     2
                  CALL_FUNCTION                  1
                  CALL_FUNCTION                  1
                  STORE_FAST                     1
                  LOAD_GLOBAL                    2
                  LOAD_FAST                      0
                  LOAD_CONST                     3
                  BINARY_ADD
                  LOAD_FAST                      1
                  LOAD_CONST                     4
                  BINARY_ADD
                  LOAD_CONST                     5
                  CALL_FUNCTION                  3
                  RETURN_VALUE
        END

.. _exercise3-2:

Solution to Practice Problem 3.2
================================
As in practice 3.1 the *POP_TOP* and *LOAD_CONST* from the end can be eliminated. In the if-then-else code both the *then* part and the *else* part execute exactly the same *STORE_FAST* instruction. That can be moved after the if-then-else code and written just once, resulting in one less instruction and three less overall. Furthermore, if we move the *LOAD_GLOBAL* for the call to *print* before the if-then-else statement, we can avoid storing the maximum value in *z* at all and just leave the result on the top of the operand stack: either *x* or *y*. By leaving the bigger of *x* or *y* on the top of the stack, the call to *print* will print the correct value. This eliminates five instructions from the original code.

.. code-block:: text

    Function: main/0
    Constants: None, 5, 6
    Locals: x, y
    Globals: print
    BEGIN
              LOAD_CONST                     1
              STORE_FAST                     0
              LOAD_CONST                     2
              STORE_FAST                     1
              LOAD_GLOBAL                    0
              LOAD_FAST                      0
              LOAD_FAST                      1
              COMPARE_OP                     4
              POP_JUMP_IF_FALSE        label00
              LOAD_FAST                      0
              JUMP_FORWARD             label01
    label00:  LOAD_FAST                      1
    label01:  CALL_FUNCTION                  1
              RETURN_VALUE
    END

It is worth noting that the code above is exactly the disassembled code from this Python program.

.. code-block:: python

    import disassembler

    def main():
        x = 5
        y = 6
        print(x if x > y else y)

    disassembler.disassemble(main)

When main is called, this code prints the result of a *conditional expression*. The if-then-else expression inside the print statement is different than an if-then-else statement. An if-then-else statement updates a variable or has some other side-effect. An if-then-else expression, or *conditional expression* as it is called in Python documentation, yields a value: either the *then* value or the *else* value. In the assembly language code we see that the yielded value is passed to the print function as its argument.

.. _exercise3-3:

Solution to Practice Problem 3.3
==================================

.. code-block:: text

        Function: main/0
        Constants: None, 5, 6
        Locals: x, y
        Globals: print
        BEGIN
                  LOAD_CONST                     1
                  STORE_FAST                     0
                  LOAD_CONST                     2
                  STORE_FAST                     1
                  LOAD_FAST                      0
                  LOAD_FAST                      1
                  COMPARE_OP                     1
                  POP_JUMP_IF_TRUE         label00
                  LOAD_GLOBAL                    0
                  LOAD_FAST                      0
                  CALL_FUNCTION                  1
                  POP_TOP
        label00:  LOAD_GLOBAL                    0
                  LOAD_FAST                      1
                  CALL_FUNCTION                  1
                  RETURN_VALUE
        END

.. _exercise3-4:

Solution to Practice Problem 3.4
==================================
The following code behaves differently if the *BREAK_LOOP* instruction is removed from the program.

.. code-block:: text

        Function: main/0
        Constants: None, 7, 6
        Locals: x, y
        Globals: print
        BEGIN
                  SETUP_LOOP               label01
                  LOAD_CONST                     1
                  STORE_FAST                     0
                  LOAD_CONST                     2
                  STORE_FAST                     1
                  LOAD_FAST                      0
                  LOAD_FAST                      1
                  COMPARE_OP                     1
                  POP_JUMP_IF_TRUE         label00
                  BREAK_LOOP
                  LOAD_GLOBAL                    0
                  LOAD_FAST                      0
                  CALL_FUNCTION                  1
                  POP_TOP
        label00:  POP_BLOCK
        label01:  LOAD_GLOBAL                    0
                  LOAD_FAST                      1
                  CALL_FUNCTION                  1
                  RETURN_VALUE
        END

.. _exercise3-5:

Solution to Practice Problem 3.5
==================================
This is the hello world program with exception handling used to raise and catch an exception. This solution does not include code for *finally* handling in case an exception happened while handling the exception. It also assumes the exception will match when thrown since JCoCo only supports one type of exception.

.. code-block:: text

    Function: main/0
    Constants: None, "Hello World!"
    Locals: ex
    Globals: Exception, print
    BEGIN
              SETUP_EXCEPT             label00
              LOAD_GLOBAL                    0
              LOAD_CONST                     1
              CALL_FUNCTION                  1
              RAISE_VARARGS                  1
              POP_BLOCK
              JUMP_FORWARD             label01
    label00:  LOAD_GLOBAL                    1
              ROT_TWO
              CALL_FUNCTION                  1
              POP_TOP
              POP_EXCEPT
    label01:  LOAD_CONST                     0
              RETURN_VALUE
    END


.. _exercise3-6:

Solution to Practice Problem 3.6
==================================
This program adds 5 and 6 together using the *__add__* magic method associated with integer objects. First 5 is loaded onto the operand stack. Then *LOAD_ATTR* is used to load the *__add__* of the 5 object onto the stack. This is the function. The argument to *__add__* is loaded next which is the 6. The 6 is loaded by the *LOAD_CONST* instruction. Then *__add__* is called with one argument. The 11 is left on the operand stack after the function call. It is stored in *x*, the *print* is loaded, *x* is loaded onto the operand stack, and *print* is called to print the value. Since *print* leaves *None* on the stack, that value is returned from the main function.

.. code-block:: text

    Function: main/0
    Constants: None, 5, 6
    Locals: x
    Globals: __add__, print
    BEGIN

              LOAD_CONST                     1
              LOAD_ATTR                      0
              LOAD_CONST                     2
              CALL_FUNCTION                  1
              STORE_FAST                     0
              LOAD_GLOBAL                    1
              LOAD_FAST                      0
              CALL_FUNCTION                  1
              RETURN_VALUE
    END

.. _exercise3-7:

Solution to Practice Problem 3.7
==================================

.. code-block:: text

    Function: main/0
    Constants: None, "Enter a string: "
    Locals: x, a
    Globals: input, print
    BEGIN
              LOAD_GLOBAL                    0
              LOAD_CONST                     1
              CALL_FUNCTION                  1
              STORE_FAST                     0
              SETUP_LOOP               label02
              LOAD_FAST                      0
              GET_ITER
    label00:  FOR_ITER                 label01
              STORE_FAST                     1
              LOAD_GLOBAL                    1
              LOAD_FAST                      1
              CALL_FUNCTION                  1
              POP_TOP
              JUMP_ABSOLUTE            label00
    label01:  POP_BLOCK
    label02:  LOAD_CONST                     0
              RETURN_VALUE
    END


.. _exercise3-8:

Solution to Practice Problem 3.8
==================================

A cell variable is needed if an inner function makes a modification to a variable that is located in the outer function. Consider the JCoCo program below. Without the cell the program below would print 10 to the screen and with the cell it prints 11. Why is that? Draw the run-time stack both ways to see what happens with and without the cell variable.

.. code-block:: text

    Function: f/1
        Function: g/1
        Constants: None, 1
        Locals: y
        FreeVars: x
        BEGIN
                  LOAD_DEREF                 0
                  LOAD_CONST                 1
                  BINARY_ADD
                  STORE_DEREF                0
                  LOAD_DEREF                 0
                  LOAD_FAST                  0
                  BINARY_ADD
                  RETURN_VALUE
        END
    Constants: None, code(g)
    Locals: x, g
    CellVars: x
    BEGIN
              LOAD_CLOSURE                   0
              BUILD_TUPLE                    1
              LOAD_CONST                     1
              MAKE_CLOSURE                   0
              STORE_FAST                     1
              LOAD_FAST                      1
              LOAD_DEREF                     0
              CALL_FUNCTION                  1
              LOAD_DEREF                     0
              BINARY_ADD
              RETURN_VALUE
    END
    Function: main/0
    Constants: None, 3
    Globals: print, f
    BEGIN
              LOAD_GLOBAL                    0
              LOAD_GLOBAL                    1
              LOAD_CONST                     1
              CALL_FUNCTION                  1
              CALL_FUNCTION                  1
              POP_TOP
              LOAD_CONST                     0
              RETURN_VALUE
    END

Interestingly, this program cannot be written in Python. The closest Python equivalent of this program is given below. However, it is not the equivalent of the program written above. In fact, the program below won't even execute. There is an error on the line *x = x + 1*. The problem is that as soon as Python sees *x =* in the function *g*, it decides there is another *x* that is a local variable in *g*. But, then *x = x + 1* results in an error because *x* in *g* has not yet been assigned a value.

.. code-block:: python

    def f(x):
        def g(y):
            x = x + 1
            return x + y

        return g(x) + x

    def main():
        print(f(3))

    main()


.. _exercise3-9:

Solution to Practice Problem 3.9
==================================
A couple things to notice in figure 3.20. The run-time stack contains one stack frame for every function call to factorial. Each of the stack frames, except the one for the *main* function, point at the *factorial* code. While there is only one copy of each function's code, there may be multiple stack frames executing the code. This happens when a function is recursive. There also multiple *n* values, one for each stack frame. Again this is expected in a recursive function.

.. container:: figbox


   .. figure:: factorial.png

  **Fig 3.20** Execution of fact.casm

.. _exercise3-10:

Solution to Practice Problem 3.10
==================================

Python is a very transparent language. It turns out there is function called dir that can be used to print the attributes of an object which are the keys of its dictionary.  The dictionary maps names (i.e. strings) to the attributes of the object. The following strings map to their indicated values.

  #. \_\_init\_\_ is mapped to the constructor code.
  #. eat is mapped to the eat method.
  #. speak is mapped to the speak method.
  #. food is mapped to an integer.
  #. This is all that is mapped by JCoCo. However, if you try this in Python you will discover that a number of other methods are mapped to default implementations of magic methods in Python including a hash method, comparison methods like equality (i.e. \_\_eq\_\_), a repr method, a str method, and a number of others.



.. _exercise3-11:

Solution to Practice Problem 3.11
==================================

.. code-block:: text
    :linenos:

    Class: Animal
    BEGIN
        Function: eat/1
        Constants: None, 1
        Locals: self
        Globals: food
        BEGIN
                  LOAD_FAST                      0
                  LOAD_ATTR                      0
                  LOAD_CONST                     1
                  BINARY_ADD
                  LOAD_FAST                      0
                  STORE_ATTR                     0
                  LOAD_CONST                     0
                  RETURN_VALUE
        END
        Function: __init__/2
        Constants: None, 0
        Locals: self, name
        Globals: name, food
        BEGIN
                  LOAD_FAST                      1
                  LOAD_FAST                      0
                  STORE_ATTR                     0
                  LOAD_CONST                     1
                  LOAD_FAST                      0
                  STORE_ATTR                     1
                  LOAD_CONST                     0
                  RETURN_VALUE
        END
        Function: speak/1
        Constants: None, "is an animal"
        Locals: self
        Globals: print, name
        BEGIN
                  LOAD_GLOBAL                    0
                  LOAD_FAST                      0
                  LOAD_ATTR                      1
                  LOAD_CONST                     1
                  CALL_FUNCTION                  2
                  POP_TOP
                  LOAD_CONST                     0
                  RETURN_VALUE
        END
    END
    Class: Dog(Animal)
    BEGIN
        Function: __init__/2
        Constants: None
        Locals: self, name
        FreeVars: __class__
        Globals: super, __init__
        BEGIN
                  LOAD_GLOBAL                    0
                  CALL_FUNCTION                  0
                  LOAD_ATTR                      1
                  LOAD_FAST                      1
                  CALL_FUNCTION                  1
                  POP_TOP
                  LOAD_CONST                     0
                  RETURN_VALUE
        END
        Function: speak/1
        Constants: None, "says woof!"
        Locals: self
        Globals: print, name
        BEGIN
                  LOAD_GLOBAL                    0
                  LOAD_FAST                      0
                  LOAD_ATTR                      1
                  LOAD_CONST                     1
                  CALL_FUNCTION                  2
                  POP_TOP
                  LOAD_CONST                     0
                  RETURN_VALUE
        END
    END
    Function: main/0
    Constants: None, "Mesa"
    Locals: mesa
    Globals: Dog, eat, speak
    BEGIN
              LOAD_GLOBAL                    0
              LOAD_CONST                     1
              CALL_FUNCTION                  1
              STORE_FAST                     0
              LOAD_FAST                      0
              LOAD_ATTR                      1
              CALL_FUNCTION                  0
              POP_TOP
              LOAD_FAST                      0
              LOAD_ATTR                      2
              CALL_FUNCTION                  0
              POP_TOP
              LOAD_CONST                     0
              RETURN_VALUE
    END

.. _exercise3-12:

Solution to Practice Problem 3.12
==================================

To get ready to execute the built-in class builder function the stack must contain the following in order from the top of the stack down: The name of the class is on the top of the operand stack. Below the name is the closure of the class initializing function and its environment. Below that is the built-in class builder function itself. The CALL\_FUNCTION instruction is executed with two arguments indicated to call the class builder.

Upon its return, the two arguments and the class builder function have been popped from the stack and the instance of the class is left on the operand stack. This class instance may then be stored as a reference from some known location, likely by a STORE\_FAST instruction.
