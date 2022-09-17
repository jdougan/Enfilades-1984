# Enfilades-1984
Several Python 3 implementations of Enfilades.
Currently there is just one implementation, but the plan is to do more later (Model-T, Indirect Data, etc.)
As the source and documentation I've generated this from is under MIT license, this is also.

## Grant Application
`enfilade-grant.py` is based on the base description in the [Xanadu Operating Company's 1984 grant application to the System Development Foundation (SDF)](doc/XanaduSDF1984OCR.pdf).
Note that the pseudo-code samples there don't actually work.
Chip Morningstar claims they are just mistakes as they were trying to show everything to justify the grant, so my earlier theories about deliberate mistakes to keep trade secrets are apparently wrong.
I've tried to debug them based on the declared intent, but I may have misunderstood.
Functions that are suffixed with "Grant" are straight translations of the pseudo-code and are broken.
Some of the support functions (levelPush, levelPop, etc.) seem to be as indicated in the pseudo-code and are working so have no "Grant" suffixed version.
The code is intended for pedagogical purposes and I make no efficiency or universality guarantees; or for that matter it being at all idiomatic Python.
What I have tried to do is convert some of the idiosyncratic Xanadu terminology into modern terminology.

The tests are in `grant-test.py` and currently do not test cuts, recombines or rearranges.
`test-xx.py` is a staging area for tests that are incomplete or experiments used to try to understand the descriptions.
They may be in a failing or erroring state.

#### Notes
* 2022-09-16 Tests have been updated.
Question of how to count depth (should bottom nodes be 0 or 1?) has been resolved in favour of 1, so an empty enfilade can be 0.
Still unsure of how to handle upper nodes with no children.
* 2022-09-14 Tests have been updated.
I'm becoming increasingly certain that levelPush need to have a normalization step.
* 2022-09-04 Finally have retrieve and append working acceptably well.
Need to fix tests next.
* 2022-09-03 I understand now! 
It appears to be intended that the disps of the children of a node should start from keyZero, so the search in the parent node works correctly. 
This normalization can be done by finding the smallest key, subtracting it from each of the child keys, and adding it to the node disp. 
Every child should then be at the same offset and the interval check in the parent retrieve should work.
* 2022-09-01 Append isn't recalculating widths on the way back up from the insertion!
* 2022-08-19 Append isn't searching the child keys the same way as retrieve.
Does however have a similar problem with the top key value disp adjustment.
* 2022-08-14 Append isn't adopting the new child nodes on the way back up  from the insertion!
* 2022-08-09 Append is unclear on how single and empty enfilades are represented.
* 2022-07-?? Retrieve isn't adjusting the key spaces to local before searching children.
Top key value needs adjustment by disp the same way as occurs in the recursive call.


### Issues
* In the pseudo-code there are no checks to see it a node is upper or bottom, which would make more sense than the key checking in the pseudo-code.
* ~~Does~~ Did weird things with zero (.0.) keys, seems they should not be used, but no mention of this or error checking.
    * This was an artifact of relying on key tests for recursion termination instead of checking for a bottom/upper node first.
    * Also influenced  by the disps and widths not being normalized.
    * It wasn't mentioned anywhere that keyZero normalization would be expected.
* Unclear on the possibility of negative key values.
    * It should work now, ~~needs to be tested~~.
* Unclear what empty and single element enfilades should be like.
    * After experimentation decided that empty is Nil/None and single is a upper and bottom normalized.
    * Single bottom nodes now work ~~with some small changes~~.
    * What happens withs an empty Upper Node?
        * Empty enfilade? Error? Remove it?
* There are a couple of possible ways to reconstruct retrieve(), not sure what was intended.
* Node splitting in append was getting disps wrong in the new node.
    * ~~Lots of issues with append~~.
* Appending data elements with a naturalWidth greater than 1 gives unintuitive results on retrieval. Keeping grant app implied semantics for now.

### Sources 
* Announcement of finding the grant app front matter with the curse: http://habitatchronicles.com/2006/06/things-you-find-while-cleaning-your-office/
* Announcement of finding the grant app: http://habitatchronicles.com/2019/03/a-lost-treasure-of-xanadu/
    * [Local copy of original PDF](doc/XanaduSDF1984OCR.pdf)
* Announcement of HTML formatting: https://sentido-labs.com/en/library/#xanadu-1986
* [Online HTML formatting of grant proposal](https://sentido-labs.com/en/library/201904240732/Xanadu%20Hypertext%20Documents.html)
    * [Online DocBook source](https://sentido-labs.com/en/library/201904240732/Xanadu%20Hypertext%20Documents.xml)
    * [Local HTML copy as of 2022-09-06](doc/XHD-20220906/Xanadu%20Hypertext%20Documents.htm)
    * [Local DocBook source copy as of 2022-09-06](doc/Xanadu%20Hypertext%20Documents-20220906.xml)
    * [Local MHTML copy as of 2022-09-06](doc/Xanadu%20Hypertext%20Documents-20220906.mhtml)

### Terms Explained and Substituted
This terminology is mostly Xanadu Green/xu88.1 specific.
Gold/xu92.1 walked back a lot of the Green terminology as well as generating some of its own.

A cleaned up Markdown version of the complete glossary in [the original scanned PDF](doc/XanaduSDF1984OCR.pdf) is in [doc/Glossary-1984.md](doc/Glossary-1984.md).

* crum
    * (tree) node
* loaf
    * child-block
    * children
    * It was split out so I/O packing behavior could be specified.
* wid
    * width
* dsp, disp
    * displacement, position, delta
    * These are keys that are relative to the parent node 
* enwidify()
    * calculateWidth()
* index
    * key
* thing
    * domain
* adopt, disown
	* addChild, removeChild
	* Haven't decided to changed code refs yet.
* childSet
    * Not a set.
    * A pair of nodes, labelled left and right
    * used to carry a cut result for splicing
* cutSet
    * Also not a set.
    * Sorted collection of keys specifying where the enfilade should split nodes, ordered by .<. / keyLessThan().
    * These get modified in place during the cut, but not resorted.

One of the reasons they used the names wids and dsps (besides for abbreviation) is because they connote a specific set of mathematical properties that the enfilade depends on, and functions and types with these properties may not involve actual widths or displacements (see section *General Enfilade Theory*).
They thought introducing new terminology would be clearer as it comes with no expectations.

## Model-T
The claim made by Ted Nelson is that the first enfilade, the Model-T (for Text) was developed in 1971-72 as part of the *Juggler of Text* (JoT) development.
They were kept under trade secret along with other enfilade forms and the general theory until the open source (X11 license) *Udanax* release in 1999.
The *Udanax Green* (aka. *Xanadu 88.1*) code is specifically dependent on enfilades, the later *Udanax Gold*  (aka. *Xanadu 92.1*) is more dependent on an evolution called the *Ent*.

It has been rediscovered independently several times, most notably by Rodney M. Bates (who calls them K-Trees or Sequence Trees) and were first published as Modula-3 code in Dr. Dobbs in 1994.
In 2002 he published a paper outlining them and doing a performance analysis.
In 2022 he republished to GitHub in both Modula-3 and Ada.

The Ropes data structure, which is also very similar to the Model-T and K-Trees, was invented a bit later than K-Trees and published in 1995.

### Sources
* [Udanax web site](http://udanax.xanadu.com/)
* [*Xanadu® Technologies-- An Introduction*, August 23, 1999](https://xanadu.com/tech/)
	* Section starting with "**A BRIEF HISTORY OF ENFILADE WORK AT PROJECT XANADU**"
* [Dr.Dobbs article, September 1994](https://xanadu.com.au/mail/udanax/msg00056.html) not freely available.
* [*Sequence trees: Logarithmic slicing and concatenation of sequences*, Journal of Combinatorial Mathematics and Combinatorial Computing, January 2002](https://www.researchgate.net/publication/266056961_Sequence_trees_Logarithmic_slicing_and_concatenation_of_sequences)
* [Another reference to K-Trees from the old Sunless-Sea wiki , August 2005](https://cxw42.github.io/htdocs/Xanadu-archaeology/articles/text/KTrees.html)
* [K-Trees reference implementations repository, August 2022 at GitHub (MIT license)](https://github.com/RodneyBates/ktrees)
* Boehm, Hans-J; Atkinson, Russ; Plass, Michael (December 1995) [*Ropes: an Alternative to Strings* at Citeseer](https://citeseer.ist.psu.edu/viewdoc/download?doi=10.1.1.14.9450&rep=rep1&type=pdf) (PDF)
* [Wikipedia on Ropes](https://en.wikipedia.org/wiki/Rope_(data_structure))

## Indirect 2D
The grant application mentions that multi-dimensional data can be stored indirectly and implicitly in the key structure of the enfilade. However there are only minimal hints on how to do this.


## General Enfilade Theory
*this is kitbashed together from the below sources and my own understanding. --jrd*

(The reader should understand that this brief introduction is not the whole of the theory, and is referred to the below listed sources, the originators, or Roger Gregory.)

An enfilade is a tree structure for managing data.
The initial Model-T enfilade was one-dimensional, referring to a long continuous row of text characters indexed by integers.

General Enfilade Theory, after some conjectures by William Barus, was discovered and elucidated within the Xanadu group around 1979 (though still not published) by Mark Miller and Stuart Greene (now Stuart Grace).
They discovered that enfilades had two basic properties which could be independently tailored to create powerful data structures as needed.

The two properties were called WIDativity (upwardly-propagating summation properties, such as the WID field of the Model-T enfilade) and DSPativity, which was also present (though implicit and unsuspected) in the Model-T enfilade.
DSP, standing for "displacement", applies to properties which propagate cumulatively downward, being imposed from above.

DSPative properties are the dual of WIDative properties.

Example: in computer graphics, a WIDative property (upwardly cumulative) is the bounding box, which grows as the tree included becomes larger.
A  DSPative property is matrix rotation, such as that of a finger of a hand on an arm, where the movement of a single bone of a single digit is a matrix product of all the motions farther up the tree.

What was the DSPative property in the Model-T?
It was the sequencing of the pointers, which sequenced the text below in a tree of downward imposition.

Both WIDative and DSPative properties must be associative, i.e. for such a property *p*

A *p* (B *p* C) = (A *p* B) *p* C

because there is no telling how the next version will be edited.
However, WIDative properties must be associative horizontally (like the sum of the WIDs in the Model-T enfilade) and DSPative properties must be associative vertically (like the positions of the crums/nodes in the Model-T enfilade).

The next big insight is that the WID and DSP functions are reversible.  This means that you can rebalance the tree as you like without affecting its meaning.
The 1979 design used this freedom for b-tree-like balancing, keeping the worst case log-like.

Enfilades can be generalized to any "spaces" characterized by these mathematical relationships, many of which are not literal geometric spaces.

General Enfilade Theory permits the creation of custom enfilades by the suitable selection and design of WIDative and DSPative properties.


###  Sources
* [*Xanadu® Technologies-- An Introduction*, August 23, 1999](https://xanadu.com/tech/)
	* Section starting with "**A BRIEF HISTORY OF ENFILADE WORK AT PROJECT XANADU**"
* [*EnfTheory-D10: Enfiladics*, Nelson and Miller](https://xanadu.com/EnfTheory-D10)
* Sunless-Sea Wiki: *General Enfilade Theory*
	* http://web.archive.org/web/20050112131720/http://sunless-sea.net/wiki/General%20Enfilade%20Theory
	* https://cxw42.github.io/htdocs/Xanadu-archaeology/articles/text/General%20Enfilade%20Theory.html
* Sunless-Sea Wiki: *Enfilade Theory*
	* https://web.archive.org/web/20041217112415/http://www.sunless-sea.net/wiki/EnfiladeTheory
	* https://cxw42.github.io/htdocs/Xanadu-archaeology/articles/text/EnfiladeTheory.html
* [Wikipedia on Enfilade](https://en.wikipedia.org/wiki/Enfilade_(Xanadu))
* [*General Enfilade Theory* at C2 wiki](http://wiki.c2.com/?GeneralEnfiladeTheory)
* Chris White's github repo for his website at `cxw42.github.io`, [Xanadu Archaeology section](https://github.com/cxw42/cxw42.github.io/tree/master/htdocs/Xanadu-archaeology)
	* [Xanadu text articles extracted from Sunless-sea wiki data](https://github.com/cxw42/cxw42.github.io/tree/master/htdocs/Xanadu-archaeology/articles/text)
* [Steve Witham writes about enfilades he has designed](https://www.aus.xanadu.com/mail/udanax/msg00050.html)
