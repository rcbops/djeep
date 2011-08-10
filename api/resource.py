from piston import resource


_callmap = resource.Resource.callmap.copy()

# Related: http://www.ietf.org/rfc/rfc2324.txt
_callmap['BREW'] = 'brew'

class Resource(resource.Resource):
  callmap = _callmap
