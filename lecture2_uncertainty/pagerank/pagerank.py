import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_distribution = dict()

    # same distribution for all if current page has no links
    if len(corpus[page]) == 0:
        for corpus_page in corpus.keys():
            prob_distribution[corpus_page] = 1 / len(corpus)
        return prob_distribution

    prob_from_corpus = (1 - damping_factor) / len(corpus)
    prob_from_link = damping_factor / len(corpus[page])

    # probability for every page in corpus that page is chosen randomly
    for corpus_page in corpus.keys():
        prob_distribution[corpus_page] = prob_from_corpus

    # add probability for pages linked to from current page
    for link in corpus[page]:
        prob_distribution[link] += prob_from_link

    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageviews = dict()
    for page in corpus.keys():
        pageviews[page] = 0

    current_page = random.choice(list(pageviews.keys()))

    # count which page was viewed by each sample
    for _ in range(n):
        pageviews[current_page] += 1
        transition = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            population=list(transition.keys()),
            weights=list(transition.values()),
            k=1
        )[0]

    # pageranks consists of pageviews in relation to sample size
    pageranks = dict()
    for page in pageviews.keys():
        pageranks[page] = pageviews[page] / n

    return pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # equal distribution as starting point
    pagerank = dict()
    for page in corpus.keys():
        pagerank[page] = 1 / len(corpus)
    
    while True:
        new_pagerank = dict()

        # calculate pagerank for each page
        for page in pagerank.keys():
            sigma_linking_pages = 0

            # check for pages linking to page in corpus to calculate sigma
            for linking_page in corpus.keys():
                # if page is linked
                if page in corpus[linking_page]:
                    sigma_linking_pages += pagerank[linking_page] / len(corpus[linking_page])
                # if no link on linking_page, treat it like having links to all pages
                if len(corpus[linking_page]) == 0:
                    sigma_linking_pages += pagerank[linking_page] / len(corpus)
            
            # apply PageRank formula
            new_pagerank[page] = (1 - damping_factor) / len(corpus) + damping_factor * sigma_linking_pages

        # compare values for pagerank and new_pagerank
        deviation = False
        for page in pagerank.keys():
            if abs(pagerank[page] - new_pagerank[page]) >= 0.001:
                deviation = True

        # return if no value changed by more than 0.001
        if not deviation:
            return new_pagerank
        else:
            # set pagerank to new values
            pagerank = copy.deepcopy(new_pagerank)    


if __name__ == "__main__":
    main()
