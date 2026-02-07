"""
Service for generating embeddings from text.
Embeddings are numerical representations that capture semantic meaning.
"""

from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

from app.models import DocumentChunk
from app.config import get_settings