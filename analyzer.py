import nltk
from nltk.tokenize import TweetTokenizer

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.positive_words = set()
        file = open(positives, "r")
        
        for line in file:
            if line.startswith(";"):
                continue
            self.positive_words.add(line.strip())
            
        file.close()
        
        self.negative_words = set()    
        file = open(negatives, "r")
        for line in file:
            if line.startswith(";"):
                continue
            self.negative_words.add(line.strip())
        
        file.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        if text is None:
            print('No text')
            exit(1)
        
        score = 0     
        tokenizer = nltk.tokenize.TweetTokenizer(preserve_case=False)
        tokens = tokenizer.tokenize(text)
        
        for token in tokens:
            if token in self.positive_words:
                score +=1
        
            if token in self.negative_words:
                score -=1
        
        return score
