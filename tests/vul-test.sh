#!/bin/bash
FQDN=`terraform output fqdn | tr -d '"'`

curl -L "$FQDN/vulnpy/cmdi/os-system/?user_input=ls"
curl -L "$FQDN/vulnpy/deserialization/pickle-load/?user_input=data"
curl -L "$FQDN/vulnpy/hash/hashlib-md5/?user_input=data"
curl -L "$FQDN/vulnpy/hash/hashlib-sha1/?user_input=data"
curl -L "$FQDN/vulnpy/parameter_pollution/"
curl -L "$FQDN/vulnpy/pt/io-open/?user_input=test.txt"
curl -L "$FQDN/vulnpy/rand/random/?user_input=10"
curl -L "$FQDN/vulnpy/redos/re-match/?user_input=test"
curl -L "$FQDN/vulnpy/sqli/sqlite3-execute/?user_input=Anakin%20Skywalker"
curl -L "$FQDN/vulnpy/ssrf/legacy-urlopen/?user_input=http%3A%2F%2Flinkedin.com"
curl -L "$FQDN/vulnpy/unsafe_code_exec/exec/?user_input=2%2B2"
curl -L "$FQDN/vulnpy/xss/raw/?user_input=david"
curl -L "$FQDN/vulnpy/xxe/lxml-etree-fromstring/?user_input=%3Cnote%3E+%3Cto%3ETove%3C%2Fto%3E+%3Cfrom%3EJani%3C%2Ffrom%3E+%3Cheading%3EReminder%3C%2Fheading%3E+%3Cbody%3EDon%27t+forget+me+this+weekend%21%3C%2Fbody%3E+%3C%2Fnote%3E"
curl -L "$FQDN/vulnpy/xpath/lxml-etree-findall/?user_input=Kepler"
