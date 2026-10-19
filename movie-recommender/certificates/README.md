# GroupLens download certificate chain

`grouplens-chain.pem` contains the public InCommon Intermediate CA - OVG3C
certificate and emSign Root TLS CA - G3 certificate. These were obtained from
the issuing CA over verified HTTPS on 2026-10-19:

- https://repository.emsign.com/certs/EEEMIncommonOVG3C.crt
- https://repository.emsign.com/certs/EMIncommonOVG3C.p7c

The server certificate's AIA names the first URL (HTTP form); the intermediate's
AIA names the second. The checked server certificate is for files.grouplens.org,
issued 2026-09-14 and expiring 2026-12-13. It is **not** bundled as a trust anchor.

emSign Root TLS CA - G3 SHA256 fingerprint:
`7DD78D5F4F13459A83DFF9ABBBA62EDBAF6F2D102BF257FD712F4D9F2746ED8D`.

The application appends these certificates to certifi's normal roots only for
the fixed official GroupLens dataset download. TLS hostname, signature and
expiry checks remain enabled. It does not alter global certificate settings.
The downloaded archive must additionally match the pinned SHA256
`8b21cfb7eb1706b4ec0aac894368d90acf26ebdfb6aced3ebd4ad5bd1eb9c6aa`.

When GroupLens changes its issuing chain, update this file from authenticated
CA sources and reverify it instead of disabling TLS checks.
