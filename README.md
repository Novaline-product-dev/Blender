![alt text](https://github.com/jtraffic/jtraffic.github.io/blob/master/img/blend.png "Blender Logo")

<img src="https://github.com/jtraffic/jtraffic.github.io/blob/master/img/blend.png" alt="Drawing" style="width: 200px;"/>
## <span style = "color:#002699">What is Blender? </span>
Blender is a system that combines artificial and human intelligence to increase creativity.  

The current version is preliminary and merely produces stimulus words associated with a particular concept.  The stimulus words are meant to strike a balance between relevance and novelty.

## <span style = "color:#002699">How Does it Work? </span>

1. The user enters a seed term.
2. Blender scrapes text from Google results associated with the seed term.
3. Using latent semantic indexing, Blender recommends new stimulus words that are chosen to be lexically similar to the original seed term (for relevance) but not too similar (novelty).  
4. The new stimulus words are POS-tagged and embedded in a sentence which suggests a way to innovate on the seed term.  For example, if a user entered "3D printing" as a seed term, an output might be: "Try blending 3D printing with a photo."
5. The interpretation of the stimulus term is up to the user, that's the human intelligence part!
6. See [centaurific.com](http://www.centaurific.com/blender) to try it as a web application.  Again, this is preliminary and very unpolished.


## <span style = "color:#002699">Why? </span>
We hypothesize that humans and computers working together can create more efficiently and effectively together than separately.  

## <span style = "color:#002699">What is Next for Blender? </span>
In no particular order, we hope to accomplish the following with Blender:

* Test our above hypothesis and publish the results in an academic journal, using some future version of Blender.
*  Improve Blender by making the suggestions more human-friendly.  
*  Refine our understanding of the intended use-case for Blender.  We expect the current version of Blender to benefit domain specialists more than generalists.
*  Improve Blender by adding functionality, such as 
  1. An automated domain selection tool.  That is, something that would aid users in their choice of seed term, and would likely make use of financial data, patents, and Google trends to aim the seed term at a promising domain.
  2. An automated, domain-specific idea evaluator, in order to process a large volume of new ideas quickly.  The evaluator would need to attempt to predict the feasibility of the idea, whether something similar exists, and whether the idea is likely to succeed.  Blender may need to rely on human expertise for some of this, but we intend to use machine intelligence as much as possible.
  3. A loop mechanism whereby Blender iterates and improves upon its original suggestions in response to user feedback and validation results from previous ideas.
