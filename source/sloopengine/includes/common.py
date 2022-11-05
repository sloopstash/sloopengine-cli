# Import community modules.
import os
import validators
from termcolor import cprint


# Validate path.
def path_validate(path):
  if path:
    if os.path.isabs(path) is True:
      return True
    else:
      cprint('Invalid path.','red')
  else:
    cprint('Cannot accept empty path.','red')

# Validate FQDN.
def fqdn_validate(fqdn):
  if fqdn:
    if validators.domain(fqdn) is True:
      return True
    else:
      cprint('Invalid FQDN.','red')
  else:
    cprint('Cannot accept empty FQDN.','red')

# Validate url.
def url_validate(url):
  if url:
    if validators.url(url) is True:
      return True
    else:
      cprint('Invalid url.','red')
  else:
    cprint('Cannot accept empty url.','red')

# Validate token.
def token_validate(token):
  if token:
    return True
  else:
    cprint('Cannot accept empty token.','red')
