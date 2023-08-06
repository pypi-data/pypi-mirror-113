## Clashgap
A per-charecter diff/compression algorithm implementation in python

### How it works
In case if you have two strings:
> "This is a sentence..." and "This is a word..."

you could "clash" both of them together and find their gap, to get an array loking something like:
> \["This is a", \["sentence", "word"\], "..."\]

As you can the clashgap algorithm looks for collisions in the two strings to find the gap

The clashgaped string maybe used for compression or as the diff of the input strings

