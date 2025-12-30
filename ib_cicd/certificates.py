import os
from functools import lru_cache
from typing import Optional, Tuple, Union


# Environment variables for mTLS cert file paths (used with requests cert parameter)
MTLS_SOURCE_CERT_ENV = "MTLS_SOURCE_CERT"
MTLS_SOURCE_KEY_ENV = "MTLS_SOURCE_KEY"
MTLS_TARGET_CERT_ENV = "MTLS_TARGET_CERT"
MTLS_TARGET_KEY_ENV = "MTLS_TARGET_KEY"


CertType = Optional[Union[str, Tuple[str, str]]]


@lru_cache(maxsize=1)
def get_source_cert() -> CertType:
    """
    Get the source mTLS certificate for requests.
    
    Returns the cert parameter to be used with requests library.
    Can be either a single PEM file path (containing both cert and key)
    or a tuple of (cert_path, key_path).
    
    Environment variables:
        MTLS_SOURCE_CERT: Path to the source certificate PEM file
        MTLS_SOURCE_KEY: Path to the source key PEM file (optional if key is in cert file)
    
    Returns:
        None if no cert configured, str if single file, tuple if separate cert/key files
    """
    cert_path = os.environ.get(MTLS_SOURCE_CERT_ENV)
    if not cert_path:
        return None
    
    key_path = os.environ.get(MTLS_SOURCE_KEY_ENV)
    if key_path:
        return (cert_path, key_path)
    
    return cert_path


@lru_cache(maxsize=1)
def get_target_cert() -> CertType:
    """
    Get the target mTLS certificate for requests.
    
    Returns the cert parameter to be used with requests library.
    Can be either a single PEM file path (containing both cert and key)
    or a tuple of (cert_path, key_path).
    
    Environment variables:
        MTLS_TARGET_CERT: Path to the target certificate PEM file
        MTLS_TARGET_KEY: Path to the target key PEM file (optional if key is in cert file)
    
    Returns:
        None if no cert configured, str if single file, tuple if separate cert/key files
    """
    cert_path = os.environ.get(MTLS_TARGET_CERT_ENV)
    if not cert_path:
        return None
    
    key_path = os.environ.get(MTLS_TARGET_KEY_ENV)
    if key_path:
        return (cert_path, key_path)
    
    return cert_path


def get_cert(source: bool = True) -> CertType:
    """
    Get the mTLS certificate for requests based on source/target flag.
    
    Args:
        source: If True, returns source cert; if False, returns target cert.
    
    Returns:
        The cert parameter to be used with requests library.
    """
    return get_source_cert() if source else get_target_cert()


def clear_certificate_cache() -> None:
    """Helper for tests to clear the cached certificate value."""
    get_source_cert.cache_clear()
    get_target_cert.cache_clear()
