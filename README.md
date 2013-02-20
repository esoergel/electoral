### A better electoral process
Choosing one candidate amongst a pool of many is not a very good way of representing your preferences.  People's opinions are more complex than that.  This leads to strategic voting - where the way one votes does not directly correspond to their actual feelings; they must factor in things such as the likelihood of a particular candidate winning.

The best way to represent someone's opinion is to have them rank their top n favorite candidates.  This results in a much more complicated data set, with many different ways to interpret the results.  Many of these methods, such as points systems, still incentivize strategic voting.  An ideal system would allow voters to put whomever they want at the top of their list, without hurting the chances of their second favorite candidate in the event that number 1 candidate proves unsuccessful.

The two-party system, while it does impose a false compartmentalization, has the advantage that it's binary.  This allows voters (who in practice have only two options) to vote for a shift in the liberal-conservative spectrum.  An ideal democratic government stands in the median of the political spectrum.  A shift to one side leaves more people on the other side, so subsequent elections will favor a shift the other way.  In this manner, the government oscillates about the median, which is about the best form of representation we can hope for in choosing one individual person/platform.  There are of course a host of other problems - political views don't really lie cleanly on a one-dimensional spectrum, tyranny of the majority, and inadequate representation of smaller demographics and ideologies.  This system does not address any of that, it is simply a better (more representative) method of choosing one option from many.

#### The Analysis
My system (which I conceived of in high school, and has been on my mind ever since) attempts to combine the benefits of selecting from binary choices (you have to make *a* decision) with the more representative ranking of candidates.  Given a set of voters' ranking lists, it is trivial to determine the outcome of any two-candiate race.  If candidate A appears higher than candidate B on a voter's ranking (or B does not appear at all), then that candidate prefers A to B.  One vote for A.  Note that only the relative positions matter - candidate A could be the voter's least favorite candidate they ranked, yet that voter gives the same benefit to candidate A as A's mom, who likely put A at the top.  This way, a voter can put Mickey Mouse (or any equally unlikely *actual* candidate) as their favorite candidate, without reducing their voting power with respect to more realistic candidates in the event Mickey doesn't make the cut.

This method can be used to determine the outcome of any runoff.  The election can proceed as a sort-of bracket system.  Pit two candidates against each other, and the winner goes on to the next round.  The problem there is that order matters.  This is what I call "The Rock Paper Scissors Problem."  If candidate rock faces candidate paper, candidate paper goes on to lose to candidate scissors.  Each ordering would result in a different outcome.  

My program takes the top n candidates (by how many ballots they appear on; if a candidate is on fewer than 5% of the ballots, for example, they are not going to win anyways), and runs *all* the orderings.  I did a few million simulations of this using randomly generated ballots, and I never found a case where there was a winner who didn't win all orderings.  This does not mean this isn't possible, but I don't think it is.

#### Benefits and Pitfalls
This system is more representative, no question about it.  It would allow people to vote their conscience without worrying about "wasting" their vote.  It would also generate a lot of data about the other candidates and parties.  This would show what level of support there is for fringe platforms, which will incentivize politicians to appeal to those views as well.  Under the current system, minor political parties have more supporters than votes, precisely because many people would rather affect the outcome of an election than take an ideological stance.

The chief problem with this system is that it is untested and difficult to understand.  Happily, the voters do not need to understand the analysis to vote, they only need to know that they should rank their favorite candidates in order.

#### Next Steps
I'd like to make a web app which performs a simulated election for "favorite president ever."  I'm hoping that real data will expose some of the benefits of this system, and prove that it's understandable.

