"""General-purpose utilities."""
"""Utilities found here."""
from dane_discovery.identity import Identity
from jwcrypto import jwk


class Util:
    """General-purpose utilities."""

    @classmethod
    def build_dns_uri(cls, device_id):
        """Return a DNS URI for the device identity."""
        kid = "dns://{}?type=TLSA".format(device_id)
        return kid

    @classmethod
    def get_name_from_dns_uri(cls, dns_uri):
        """Return the DNS name from dns_uri.

        Support hostname extraction from input format consistent with relative
        and authoritative records as defined in
        https://tools.ietf.org/html/rfc4501.

        Args:
            dns_uri (str): DNS URI.

        Return:
            str: DNS name.

        Raise:
            ValueError: If format is wrong, raise an error.
        """
        preamble = "dns:"
        ending = "?type=TLSA"
        if not dns_uri.startswith(preamble):
            raise ValueError("Bad format. See RFC 4501.")
        if not dns_uri.endswith(ending):
            raise ValueError("Bad format. See RFC 4501.")
        reduced = dns_uri.replace(preamble, "").replace(ending, "")
        hostname = reduced.split("/")[-1]
        return hostname

    @classmethod
    def get_pubkey_from_dns(cls, dns_name, dane_type=None, strict=True):
        """Return JWK for DNS-based identity.

        Args:
            dns_name (str): DNS name for locating TLSArr.
            dane_type (str): ``PKIX-EE``, ``DANE-EE``, or ``PKIX-CD``. This
                indicates the type of certificate we are interested in retrieving.
                Defaults to ``None``, which will cause the first entity certificate 
                to be returned.
            strict (bool): Fail if unable to validate certificate using a 
                signature via DNSSEC (or PKI for PKIX-CD)

        Return:
            JWK: Javascript Web Key containing public
                key retrieved from DNS.

        """
        identity = Identity(dns_name)
        if dane_type is not None:
            cert = identity.get_first_entity_certificate_by_type(dane_type, 
                                                                 strict=strict)
        else:
            cert = identity.get_first_entity_certificate(strict=strict)
        pubkey = jwk.JWK()
        pubkey.import_from_pyca(cert.public_key())
        return pubkey
