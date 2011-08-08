import logging
import StringIO

class BusyboxWgetMiddleware(object):
  def process_request(self, request):
    real_method = request.META.get('HTTP_X_REAL_HTTP_METHOD', request.method)
    real_data = request.META.get('HTTP_X_REAL_HTTP_DATA', request.raw_post_data)

    # NOTE(termie): This is a terrible hack because BusyBox's version of wget
    #               doesn't support POST or anything else.
    request.method = real_method
    request._raw_post_data = real_data
    request._stream = StringIO.StringIO(real_data)
