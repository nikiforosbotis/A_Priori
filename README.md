# A_Priori

This repository includes the implementation of the [A_Priori algorithm](https://en.wikipedia.org/wiki/Apriori_algorithm), which was proposed by Agrawal and Srikant (1994), in Python.

# A-Priori Algorithm

![68747470733a2f2f75706c6f61642e77696b696d656469612e6f72672f6d6174682f342f662f622f34666265646231663837386434663862343964643030356433633064643837332e706e67](https://cloud.githubusercontent.com/assets/9116253/17077517/8d6f0f08-50db-11e6-807b-429a24b65dd8.png)

In several applications (study the consumer behavior, plagiarism identification, etc.) it is required to find frequent item sets. One way of achieving that is by applying the algorithm of Agrawal and Srikant (1994).

The baskets of items are included in a `CSV` file. Each line of such a file has the following structure:

```
item_1, item_2, ..., item_n
```
For example, one such file can be:

```
Cat, and, dog, bites
Yahoo, news, claims, a, cat, mated, with, a, dog, and, produced, viable, offspring
Cat, killer, likely, is, a, big, dog
Professional, free, advice, on, dog, training, puppy, training
Cat, and, kitten, training, and, behavior
Dog, &, Cat, provides, dog, training, in Eugene, Oregon
"Dog, and, cat", is, a, slang, term, used, by, police, officers, for, a, male-female, relationship
Shop, for, your, show, dog, grooming, and, pet, supplies
```

This program reads a file like the above one, finds the frequent item sets according to the threshold that is given by the user and extracts the results in `CSV`.

The script can be called like this:
```bash
python a_priori.py [-n] [-p] [-o OUTPUT] support filename
```
  * The parameter `-n` is optional. If given, the program deems the item sets as arithmetic (no strings).
  * The parameter `-p` is optional. If given, the program deems that the minimum value of support that is given through the parameter `-s`, is the *percentage* of the baskets in which the item set should be existing in order to be considered as important.
  * The parameter `-o OUTPUT` is optional. If given, the program saves the results in the file `OUTPUT`. Otherwise, the results are shown in the screen.
  * The parameter `support` is compulsory and is the lowest level of support which will be used by the script in order to deem an item set important.
  * The parameter `filename` is compulsory and is the name of the input file.

For example, the program can be called in the following way:

```
python a_priori.py -n 2 a_priori_example_2.csv
```

Indicative input and output files of the script:

* [example_1.csv](examples.csv/example_1.csv), support: 3, will produce:
```
('a',):3;('and',):4;('cat',):5;('dog',):6;('training',):3
('and', 'cat'):3;('and', 'dog'):3;('cat', 'dog'):4
```
* [example_2.csv](examples.csv/example_2.csv), support: 2 (considering the item sets as arithmetic), will produce:
```
(1,):2;(2,):3;(3,):3;(5,):3
(1, 3):2;(2, 3):2;(2, 5):3;(3, 5):2
(2, 3, 5):2
```
* [example_3.csv](examples.csv/example_3.csv), support: 2 (considering the item sets as arithmetic), will produce:
```
(1,):3;(2,):6;(3,):4;(4,):5
(1, 2):3;(1, 4):2;(2, 3):3;(2, 4):4;(3, 4):3
(1, 2, 4):2;(2, 3, 4):2
```

The full program's description (in Greek) can be found [here](https://github.com/dmst-algorithms-course/assignment-2015-3).
