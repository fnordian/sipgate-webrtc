from webassets.filter import Filter
from react.jsx import JSXTransformer


class ReactFilter(Filter):
    name = 'react'

    def output(self, _in, out, **kw):
        content = _in.read()
        transformer = JSXTransformer()
        js = transformer.transform_string(content)
        out.write(self._moduleIntro())
        out.write(js)
        out.write(self._moduleOutro())

    def _moduleIntro(self):
        return "define([\"react\"], function(React) {\n"

    def _moduleOutro(self):
        return "\n" \
               "return self;\n" \
               "});"