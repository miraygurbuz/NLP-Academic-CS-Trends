import string

ACADEMIC_STOPWORDS = {
    "abstract", "introduction", "background", "related", "work", "literature", "review",
    "conclusion", "paper", "research", "study", "studies", "results", "findings", "finding",
    "discussion", "method", "methods", "methodology", "analysis", "approach", "data",
    "dataset", "datasets", "information", "knowledge", "technique", "techniques",
    "model", "models", "system", "systems", "architecture", "framework", "design",
    "experiment", "experiments", "evaluation", "performance", "implementation",
    "proposed", "propose", "proposing", "based", "using", "used", "use", "apply", "applied",
    "application", "applications", "result", "observation", "observations", "obtain", "obtained",
    "figure", "fig", "figs", "table", "tab", "tabs", "et", "al", "e.g", "i.e", "etc",
    "significant", "significantly", "demonstrate", "demonstrated", "demonstration",
    "present", "presents", "presented", "conducted", "show", "shown", "evaluate", "evaluated",
    "compare", "comparison", "compared", "effect", "effects", "effective", "effectively",
    "improve", "improvement", "enhance", "enhancement", "contribute", "contribution",
    "contributions", "novel", "new", "future", "direction", "directions", "perspective",
    "goal", "objective", "objectives", "aim", "aims", "paper's", "researcher", "researchers",
    "field", "fields", "domain", "domains", "context", "scope", "organization", "structure",
    "section", "sections", "overview", "introduction", "summary", "limitations", "limitation",
    "general", "specific", "problem", "problems", "solving", "solution", "solutions",
    "significance", "motivation", "consider", "considered", "assume", "assumed",
    "validate", "validated", "validation", "hypothesis", "theory", "theoretical",
    "practical", "empirical", "application", "implementation", "software", "hardware",
    "conference", "proceedings", "journal", "article", "paper"
}

NORMALIZATION_PATTERNS = {
    'html_tags': r'<.*?>',
    'urls': r'http\S+',
    'numbers': r'\d+',
    'multiple_spaces': r'\s+',
    'punctuation': string.punctuation
}

CONFIG = {
    'data_path': '../data/raw/merged.csv',
    'cleaned_output': '../data/processed/cleaned.csv',
    'processed_output': '../data/processed/processed.csv',
    'url_replacement': '[URL]',
    'min_token_length': 2,
    'normalization_lowercase': True,
    'normalization_patterns': NORMALIZATION_PATTERNS
}