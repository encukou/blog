Title: Types as namespaces
Tags: language design


Musings inspired by Eevee's [post about Sylph](http://eev.ee/blog/2015/02/28/sylph-the-programming-language-i-want/).
Read that first.

In Python's duck-typing system, it's enough if things quack.
They don't actually need to quack *like a duck*.

<!-- PELICAN_END_SUMMARY -->

 * * *

Whenever you program, you need to keep track of the types of things you're dealing with.
Some languages – the statically typed ones – require you to specify the type in front, and then they check it rigorously.
In Python, you need to keep track of this in your head.
It's possible that you're writing code where a variable could be either a string or a number:

    def add(a, b):
        return a + b

... or you might want a variable to changes type in the middle of a function,
like in the example from [Hitchhiker's guide to Python](http://docs.python-guide.org/en/latest/writing/structure/#dynamic-typing):

    items = 'a b c d'  # This is a string...
    items = items.split(' ')  # ...becoming a list
    items = set(items)  # ...and then a set

Those are smells: they should be *possible* but not *easy*.

Variables (the *names*, not just values) always have types, even if,
as in the “dynamic” languages, they're only implied – they only exist in the
programmer's head, as assumptions on the value's behavior.
If I use a `startswith` I really want “a method with the *semantics* of `String:startswith`”,
rather than “the method *named* startswith”.

# Types of variables

I have some syntax in mind. If I rewrite one of the first examples in
Eevee's post in it, I can get something like this:

    def foo(a: String, b: StringPattern, c: List):
        if a.startswith(b):
            c.append(a)

By which I want to say `b` can be string, or a tuple of strings,
or even a regex for all I care – as long as it can be matched against a string.
Those are the semantics I wrote the function for.
If you call it with different types then you're on your own – it might work,
and the language should allow it, but I offer no guarantees about the behavior of my function.

Here the “startswith” is, quite explicitly, `String:startswith`.
The call is not a command to “quack”, but to “quack *like a duck*”.

The difference from statically-typed languages is that I'm not requiring `a` to be
a string, or a string subtype.
I don't even care if `a` implements the string interface.
I'm just saying that I want to call `String:startswith`.
The `String` declaration does not restrict the value, it provides a namespace for my operations on it.
And with the namespaced operations come some well-defined semantics: if you misimplement them,
it's not my fault that my `foo` function won't work.

Similarly, I don't care if `c` is actually a list. I'm just saying I want the
`MutableSequence:append` method (for which `List:append` is an alias).
After the `append` call, `c[-1]` should be whatever I just put there.
But that's your (the caller's) problem. If `c` is not `List` enough,
your code might break with the next version of my library.

Of course, usually `a` will be an “actual string”, and the compiler can
optimize for that case.

I'll put a random snippet with syntax ideas here:

    from somewhere import Snake

    def print_length(x: List):
        print(x.length)

        if x has Snake:length:
            print("Scary! I got a {}m long snake as argument!"(x.Snake:length))

# Type declarations

For variables, the type can be specified declaration.
Python has no variable declarations, which I don't think is healthy, because the
resulting scoping rules are not intuitive. They happen to work OK for 99%
of the cases, but when you get hit by the 1%, you don't even know where to look
(unless you remember the warning from your tutorial).
Javascript's explicit `var` keyword is a good thing, for much the same reasons as Python's
explicit `self`.

In my syntax, variable declarations can specify the type:

    str: String = "abcd"

    list: List = ["1", "2", "3"]

    for i:int in list:
        print(i * i)

But, since most (or ideally all) expressions have a well-defined types, a shorthand comes to mind:

    str := "abcd"
    list := ["1", "2", "3"]

# Operator namespaces

This would work:

    def concat(a: List, b: List):
        return a + b

    def elementwise-add(a: Array, b: Array):
        return a + b

    a := [1, 2, 3]
    b := [4, 5, 6]

    assert concat(a, b) == [1, 2, 3, 4, 5, 6]
    assert elementwise-add(a, b) == [5, 7, 9]

because while `Sequence:\+` and `Array:\+` are two different things,
lists can support *both*.

(Extending this to custom operators with custom priority is left as an exercise...)

# Definitions and Implementations

Let's make a Tree interface.
I'll use [PEP 484](https://www.python.org/dev/peps/pep-0484/)-ish syntax for generics:

    T := TypePlaceholder()

    interface Tree:
        walk(self: T) -> Iterator[T]

This says that the type of `x.Tree:walk().next()` will be the same as the
type of `x`.
(For any `x`. Remember it's defining the type of the *expression*, not the value;
it's defining the namespace that expression will use by default.)

Then you can define BinaryTree like this.
`BinaryTree:walk` becomes an implementation of `Tree:walk`.

    class BinaryTree(Tree):
        left: Tree
        right: Tree

        impl walk(self):
            if self.left:
                yield from self.left.walk()
            yield self
            if self.right:
                yield from self.left.walk()

Note the kewyord is `impl`, not `def`: this ensures that if the `Tree` interface
grows a new method, existing methods of the same name won't magically become
its implementations.
(Though you will get lots of *warnings* about the new method not being implemented
by classes that claim to implement `Tree`.)

Next let's have a class for corporate employees.
An amployee is not a tree, and there's no `Employee:walk` in our model,
but you can still use an employee as a tree node:

    class Employee:
        boss: Employee
        underlings: List[Employee]

        impl Tree:walk(self):
            yield self
            for underling in self.underlings:
                yield from underling.walk()

And you might want to attach a `Tree:walk` to something from some library you
can't easily change, like the stdlib.

    impl Path.Tree:walk(self):
        yield self
        if self.isdir:
            for child:Tree in self.listdir:
                yield from child

The language should probably limit who can do this and where, though.

To step away from Tree for one paragraph:
Since every class derives from `Object`, which has a `to_string` method,
you can write `impl to_string` in any class.
Or you can write `def to_string`, which won't conflict with `Object:to_string`
(though it will raise eyebrows and trip up your linter).
And you can later add `impl Object:to_string`, which won't be aliased to
`YourClass:to_string`.

# Interface conflicts

Consider this class:

    class FamilyMember:
        parents: List[FamilyMember]
        children: List[FamilyMember]

        impl Tree:walk(self):
            # this is not be correct but w/e
            yield self
            for child:Tree in self.children:
                yield from child

Now, if you inherit from both `Employee` and `FamilyMember`, you're in trouble.
The resulting `Tree:walk` should fail loudly, unless you explicitly override it.

# Bags of attributes

“But Petr“, I hear you saying, “I want my `getattr(self, 'visit_' + node.type)`”!
Eh, really? I reply. That looks quite ugly.
I jut explained that I think attribute names should *not* be just names, didn't I?
If you want a collection of things keyed by strings, use a mapping.
You don't even want the keys to be strings here – you want Node subclasses.

That said, you could write `getattr(self, Attribute(Visit, node.type))`,
and implement `Visit:leaf`, where `Visit` is an empty(!) interface.

# That's it for now

I could rant on, about, say, registration conflicts or efficient vtable
references, but let's end it here, throw it at the wall and see if it sticks.


(I welcome comments, by the way – if you have any, send them by e-mail or pull request)

