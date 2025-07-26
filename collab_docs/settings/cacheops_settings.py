"""
Cacheops configuration for the collaborative document editing platform.
"""
# Cache timeout constants
CACHE_TIMEOUT = 7200  # 2 hours

# Cacheops configuration
CACHEOPS_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 1,
    'socket_timeout': 3,
}

CACHEOPS_OPS = ('get', 'filter', 'exists')
CACHEOPS = {
    'documents.document': {
        'ops': CACHEOPS_OPS,
        'timeout': CACHE_TIMEOUT,
    },
    'documents.collaborator': {
        'ops': CACHEOPS_OPS,
        'timeout': CACHE_TIMEOUT,  # 2 hours
    },
    'documents.documentversion': {
        'ops': CACHEOPS_OPS,
        'timeout': CACHE_TIMEOUT,  # 2 hours
    },
    
    'users.customuser': {
        'ops': ('get', 'exists'),
        'timeout': CACHE_TIMEOUT,  # 2 hours
    },
    
    'auth.group': {
        'ops': ('get', 'filter'),
        'timeout': 86400,  # 24 hours (rarely change)
    },
    'auth.permission': {
        'ops': ('get', 'filter'),
        'timeout': 86400,  # 24 hours (rarely change)
    },
}

# Cache invalidation settings
CACHEOPS_DEGRADE_ON_FAILURE = True
CACHEOPS_DEFAULTS = {
    'timeout': CACHE_TIMEOUT,
    'ops': CACHEOPS_OPS,
}

# Prefix for cache keys
CACHEOPS_PREFIX = 'collab_docs'

# Enable cache statistics
CACHEOPS_ENABLED = True
