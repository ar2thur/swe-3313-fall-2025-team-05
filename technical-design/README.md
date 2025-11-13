# Technical Design

## Table of Contents
- [A. Implementation Language(s)](#a)
- [B. Implementation Framework(s)](#b)
- [C. Data Storage Plan](#c)
- [D. Entity Relationship Diagram](#d)
- [E. Entity/Field Descriptions](#e)
- [F. Data Examples](#f)
- [G. Database Seed Data](#g)
- [H. Authentication and Authorization Plan](#h)
- [I. Coding Style Guide](#i)
- [Technical Design Presentation](#j)

<a id="a"></a>
## A. Implementation Language(s)
For our languages we have chosen to develop our project in:
- Python 3.12
    1. All team members have more experience with Python than Java or C#.
    2. Simple syntax significantly increases development and prototyping speed.
    3. Significant amount of quality of life packages for building web applications.
- HTML5
    1. All browsers natively understand and know how to render HTML.
    2. Simple syntax, easy to pick up for members of our group that haven't used it before.
- CSS
    1. We will be using CSS vicariously through DaisyUI.
- JavaScript
    1. Allows website to have interactive buttons and dynamic content.
    2. Supported in all major web browsers.

<a id="b"></a>
## B. Implementation Framework(s)
For our implementation frameworks and libraries we have chosen:
- Framework - Flask
    1. Really popular and easy to follow web application framework for Python.
    2. Comes with out of the box SQLite support, which is our database of choice.
    3. Amazing documentation.
- TailwindCSS Component Library - DaisyUI
    1. Pure CSS prebuilt components, works on any browser.
    2. Has a rich component library and detailed documentation.
    3. Supports all TailwindCSS modifiers as well.
- ORM - SQLAlchemy
    1. Converts SQL tables and queries into pythonic class objects in our codebase.
    2. Makes working with SQLite intuitive and easy to use for team members without SQL experience.

<a id="c"></a>
## C. Data Storage Plan
We plan to use SQLite for data storage. Since Flask offers native support for connecting and 
persisting SQLite databases, this was the natural choice. TODO: Got stuck here

<a id="d"></a>
## D. Entity Relationship Diagram
![erdiagram](./assets/entity-relationship-diagram.png)

<a id="e"></a>
## E. Entity/Field Descriptions


<a id="f"></a>
## F. Data Examples


<a id="g"></a>
## G. Database Seed Data


<a id="h"></a>
## H. Authentication and Authorization Plan


<a id="i"></a>
## I. Coding Style Guide
- All code in the project will follow the [PEP 8](https://peps.python.org/pep-0008/) style guide because:
    1. It is the style that all of our team defaults to when writing Python code.
    2. It is the official style guide for Python.

- All code written should have high cohesion and low coupling.

- All code written should be readable and use proper commenting so it can be understood by other developers. "Proper commenting" in this case means concisely explaining complex or non-obvious logic, possibly including reasoning behind it. 

- All commits to the project repository during development will follow the [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) branch management strategy because:
    1. The implementation of pull requests encourage code reviews. This practice will help us maintain a clean and cohesive codebase, along with ensuring that it meets the standards of the style guide.
    2. The use of branching helps protect the stability of the *main* branch by isolating the work of each developer.


<a id="j"></a>
## Technical Design Presentation
See [here]() for a link to the technical design video presentation.
