from .genres import router as genres_router
from .movies import router as movies_router
from .persons import router as persons_router

__all__ = (
    'movies_router',
    'genres_router',
    'persons_router',
)
