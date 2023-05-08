# Enfilades-1984
Several Python 3 implementations of Enfilades.
Currently there is just one implementation, but the plan is to do more later (Model-T, Indirect Data, etc.)
As the source and documentation I've generated this from is under MIT license, this is also.

## Grant Application
`enfilade-grant.py` is based on the base description in the [Xanadu Operating Company's 1984 grant application to the System Development Foundation (SDF)](doc/XanaduSDF1984OCR.pdf).

Note that the pseudo-code samples there don't actually work.
Chip Morningstar claims they are just mistakes as they were trying to show everything to justify the grant, so my earlier theories about deliberate mistakes to keep trade secrets are apparently wrong.
I've tried to debug them based on the declared intent, but I may have misunderstood.

The keys are `int` the values are `str` of length 1.
Functions that are suffixed with "Grant" are mostly straight translations of the pseudo-code and are undebugged.
Some of the support functions (levelPush, levelPop, etc.) seem to work as indicated in the pseudo-code so have no "Grant" suffixed version.
I have removed uses of a global that holds the top node of the enfilade (Fulcrum in Xanadu parlance), instead the functions take the top node as argument and modification functions return the (possibly new) top node.
The code is intended for pedagogical purposes and I make no efficiency or universality guarantees; or for that matter it being at all idiomatic Python.
What I have also tried to do is convert some of the idiosyncratic Xanadu terminology into modern terminology. See [Terms Explained and Substituted](#terms-explained-and-substituted)

The tests are in `grant-test.py` and currently do not test cuts, recombines or rearranges.
`test-xx.py` is a staging area for tests that are incomplete or experiments used to try to understand the descriptions.
They may be in a failing or erroring state.
Many of the tests produce markdown formatted output.

#### Notes
* 2023-04-29 First pass at untangling cut() and various support functions.

* 2022-09-17 More Tests.
AFter a bunch of debugging, It seems that data entries that put multiple items of data at the same key, if there is $naturalWidth(data) > 1$ , can cause a `KeyError` while appending.
This is because append first finds a bottom node that contains `whereKey` using the usual search mechanism and there is a chance that, depending on ordering details, it will first find a data item where the non-first element is at the key.
This, of course, causes the key check to fail, giving the key error.
I am uncertain if I'm  going to fix this here, or build a another enfilade that isn't trying to echo the semantics in the pseudo-code version.
There is also a similar issue with retrieves.
* 2022-09-16 Tests have been updated.
Question of how to count depth (should bottom nodes be 0 or 1?) has been resolved in favour of 1, so an empty enfilade can be 0.
Still unsure of how to handle upper nodes with no children.
* 2022-09-14 Tests have been updated.
I'm becoming increasingly certain that `levelPush` need to have a normalization step.
* 2022-09-04 Finally have `retrieve` and `append` working acceptably well.
Need to fix tests next.
* 2022-09-03 I understand now! 
It appears to be intended that the disps of the children of a node should start from `keyZero()`, so the search in the parent node works correctly.
This normalization can be done by finding the smallest key, subtracting it from each of the child keys, and adding it to the node disp. 
Every child should then be at the same offset and the interval check in the parent retrieve should work.
* 2022-09-01 `Append` isn't recalculating widths on the way back up from the insertion!
* 2022-08-19 `Append` isn't searching the child keys the same way as retrieve.
Does however have a similar problem with the top key value disp adjustment.
* 2022-08-14 `Append` isn't adopting the new child nodes on the way back up  from the insertion!
* 2022-08-09 `Append` is unclear on how single and empty enfilades are represented.
* 2022-07-?? `Retrieve` isn't adjusting the key spaces to local before searching children.
Top key value needs adjustment by disp the same way as occurs in the recursive call.


### Issues
* In the pseudo-code there are no checks to see it a node is upper or bottom, which would make more sense than the key checking in the pseudo-code.
* ~~Does~~ Did weird things with `keyZero()` (aka. .0.) keys, seems they should not be used, but no mention of this or error checking.
    * This was an artifact of relying on key tests for recursion termination instead of checking for a bottom/upper node first.
    * Also influenced  by the disps and widths not being normalized.
    * It wasn't mentioned anywhere that `keyZero()` normalization would be expected.
* Unclear on the possibility of negative key values.
    * It should work now, ~~needs to be tested~~.
* Unclear what empty and single element enfilades should be like.
    * After experimentation decided that empty is Nil/None and single is a upper and bottom normalized.
    * Single bottom nodes ~~should~~ now work ~~with some small changes~~.
    * What happens withs an empty Upper Node?
        * Empty enfilade? Error? Remove it?
* There are a couple of possible ways to reconstruct `retrieve()`, not sure what was intended.
	* the key correction to local from root can be done in the calling proc, or in the called part.
	* Decided to do it in the calling proc, since append does a similar thing.
* Node splitting in append was getting disps wrong in the new node.
    * ~~Lots of issues with append~~.
* Appending data elements with a `naturalWidth()` greater than 1 gives unintuitive results on retrieval. Keeping grant app implied semantics for now.
* Cut as written in the grant application makes some weird assumptions:
    * It assumes we never split a full node. However, it can happen and will overflow the children when adding the rightNode, and there is no clear path to handle this case.
    * It assumes we never try to split a bottom node. However, this can happen in the case where the data has a `naturalWidth()`greater than 1. This is data specific so would require bespoke code anyways, but you'd think there would be some indication. I added an assert() to check the node is an upper node, in case if it should get fed data values with a `naturalWidth() > 1`.
    * FIXME TODO It is unclear how well this would work with multiple hit retrieval as outlined in the section in the grant app on retrieve. (confirm?)The split procedure can create can create holes in the index space data that were not there before.
* split() and chopUp() have no hint of any kind of normalization of disps and widths for the split and reassembly. Unclear at the moment if it will matter.  FIXME
* primitiveRecombine() has a similar issue regarding child node overflow.

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

* index
    * key
* crum
    * (tree) node
* fulcrum
	* top node
* loaf0
    * child-block
    * children
    * It was split out so I/O packing behavior could be specified, we don't care for this.
* wid
    * width
* dsp, disp
    * displacement, position, delta
    * These are keys that are relative to the parent node 
    * I'm going with "disp" because it is short.
* enwidify()
    * calculateWidth()
    * index WIDdative function
* naturalWid()
	* naturalWidth()
	* data WIDdative function
* thing
    * domain
* adopt, disown
	* addChild, removeChild
	* Haven't decided to changed code refs yet.
* childSet
    * Not a set.
    * A pair of nodes, labelled left and right
    * used to carry a cut result for splicing
    * In Python we could use a destructuring tuple return for this.
* cutSet
    * Also not a set.
    * Sorted ordered collection of keys specifying where the enfilade should split nodes, ordered by .<. / keyLessThan().
    * These get modified in place during the cut, but not resorted.

One of the reasons they used the names wids and dsps (besides for abbreviation) is because they connote a specific set of mathematical properties that the enfilade depends on, and functions and types with these properties may not involve actual widths or displacements (see [*General Enfilade Theory*]()).
They thought introducing new terminology would be clearer as it comes with no expectations.

## Model-T
*"If I have seen farther than others, it is because I was standing on the shoulders of giants."* -- Isaac Newton  
*"In computer science, we stand on each other's feet."* -- Brian K. Reid

Ted Nelson claims that the first enfilade, the *Model-T* (for Text) was developed around 1971-72 as part of the *Juggler of Text* (JoT) development.
The indexes are integers, the values are text ranges in buffers or on disk storage.
The upward summarizing property is text run length, and the downward imposition property is the sequencing.
They were kept under trade secret along with other enfilade forms and the general theory until the open source (MIT X11 license) *Udanax* release in 1999.

It has been rediscovered independently several times, notably by Rodney M. Bates (who calls them *K-Trees* or *Sequence Trees*) and were first published as Modula-3 code in Dr. Dobbs in 1994.
In 2002 he published a paper outlining them and doing a performance analysis.
In 2022 he republished to GitHub in both Modula-3 and Ada.

The *Ropes* data structure, which is also very similar to the Model-T and K-Trees, was invented a bit later than K-Trees and published in 1995.

The *monoid-cached tree* is a rediscovery of the principles of upward summarization  in 2006 as part of Hinze and Paterson's Finger Tree paper.
Note that the term does not appear in the paper, it appears to be a later construction of unknown origin, along with the term *monoid-cached rope*.

### Sources
* [Udanax web site](http://udanax.xanadu.com/)
* [*Xanadu® Technologies-- An Introduction*, August 23, 1999](https://xanadu.com/tech/)
	* Section starting with "**A BRIEF HISTORY OF ENFILADE WORK AT PROJECT XANADU**"
* [Wikipedia on Enfilades](https://en.wikipedia.org/wiki/Enfilade_(Xanadu))
* [Dr.Dobbs article in K-Trees, September 1994](https://xanadu.com.au/mail/udanax/msg00056.html) not freely available.
* [*Sequence trees: Logarithmic slicing and concatenation of sequences*, Journal of Combinatorial Mathematics and Combinatorial Computing, January 2002](https://www.researchgate.net/publication/266056961_Sequence_trees_Logarithmic_slicing_and_concatenation_of_sequences)
* [Another reference to K-Trees from the old Sunless-Sea wiki , August 2005](https://cxw42.github.io/htdocs/Xanadu-archaeology/articles/text/KTrees.html)
* [K-Trees reference implementations repository, August 2022 at GitHub (MIT license)](https://github.com/RodneyBates/ktrees)
* Boehm, Hans-J; Atkinson, Russ; Plass, Michael (December 1995) [*Ropes: an Alternative to Strings* at Citeseer](https://citeseer.ist.psu.edu/viewdoc/download?doi=10.1.1.14.9450&rep=rep1&type=pdf) (PDF)
* [Wikipedia on Ropes](https://en.wikipedia.org/wiki/Rope_(data_structure))
* Hinze and Paterson, [*Finger trees: A simple general-purpose data structure* at Researchgate](https://www.researchgate.net/publication/220676477_Finger_trees_A_simple_general-purpose_data_structure)
* [Wikipedia on Finger Trees](https://en.wikipedia.org/wiki/Finger_tree)

## Indirect 2D
The grant application mentions that multi-dimensional data can be stored indirectly and implicitly in the key structure of the enfilade. However there are only minimal hints on how to do this.


