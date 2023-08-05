Object.defineProperty(exports, "__esModule", { value: true });
var locale_1 = require("app/locale");
exports.default = {
    'base-uri': locale_1.t("The <code>base-uri</code> directive defines the URIs that a user agent\n  may use as the document base URL. If this value is absent, then any URI\n  is allowed. If this directive is absent, the user agent will use the\n  value in the <code>&lt;base&gt;</code> element."),
    'child-src': locale_1.t("The <code>child-src</code> directive defines the valid sources for\n  web workers and nested browsing contexts loaded using elements such as\n  <code>&lt;frame&gt;</code> and <code>&lt;iframe&gt;</code>."),
    'connect-src': locale_1.t("The <code>connect-src</code> directive defines valid sources for fetch,\n  <code>XMLHttpRequest</code>, <code>WebSocket</code>, and\n  <code>EventSource</code> connections."),
    'font-src': locale_1.t("The <code>font-src</code> directive specifies valid sources for fonts\n  loaded using <code>@font-face</code>."),
    'form-action': locale_1.t("The <code>form-action</code> directive specifies valid endpoints for\n  <code>&lt;form&gt;</code> submissions."),
    'frame-ancestors': locale_1.t("The <code>frame-ancestors</code> directive specifies valid parents that\n  may embed a page using the <code>&lt;frame&gt;</code> and\n  <code>&lt;iframe&gt;</code> elements."),
    'img-src': locale_1.t("The <code>img-src</code> directive specifies valid sources of images and\n  favicons."),
    'prefetch-src': locale_1.t("The <code>prefetch-src</code> directive restricts the URLs\n      from which resources may be prefetched or prerendered."),
    'manifest-src': locale_1.t("The <code>manifest-src</code> directive specifies which manifest can be\n  applied to the resource."),
    'media-src': locale_1.t("The <code>media-src</code> directive specifies valid sources for loading\n  media using the <code>&lt;audio&gt;</code> and <code>&lt;video&gt;</code>\n  elements."),
    'object-src': locale_1.t("The <code>object-src</code> directive specifies valid sources for the\n  <code>&lt;object&gt;</code>, <code>&lt;embed&gt;</code>, and\n  <code>&lt;applet&gt;</code> elements."),
    'plugin-types': locale_1.t("The <code>plugin-types</code> directive specifies the valid plugins that\n  the user agent may invoke."),
    referrer: locale_1.t("The <code>referrer</code> directive specifies information in the\n  <code>Referer</code> header for links away from a page."),
    'script-src': locale_1.t("The <code>script-src</code> directive specifies valid sources\n  for JavaScript. When either the <code>script-src</code> or the\n  <code>default-src</code> directive is included, inline script and\n  <code>eval()</code> are disabled unless you specify 'unsafe-inline'\n  and 'unsafe-eval', respectively."),
    'script-src-elem': locale_1.t("The <code>script-src-elem</code> directive applies to all script requests\n      and element contents. It does not apply to scripts defined in attributes."),
    'script-src-attr': locale_1.t("The <code>script-src-attr</code> directive applies to event handlers and, if present,\n      it will override the <code>script-src</code> directive for relevant checks."),
    'style-src': locale_1.t("The <code>style-src</code> directive specifies valid sources for\n  stylesheets. This includes both externally-loaded stylesheets and inline\n  use of the <code>&lt;style&gt;</code> element and HTML style attributes.\n  Stylesheets from sources that aren't included in the source list are not\n  requested or loaded. When either the <code>style-src</code> or the\n  <code>default-src</code> directive is included, inline use of the\n  <code>&lt;style&gt;</code> element and HTML style attributes are disabled\n  unless you specify 'unsafe-inline'."),
    'style-src-elem': locale_1.t("The <code>style-src-elem</code> directive applies to all styles except\n      those defined in inline attributes."),
    'style-src-attr': locale_1.t("The <code>style-src-attr</code> directive applies to inline style attributes and, if present,\n      it will override the <code>style-src</code> directive for relevant checks."),
    'frame-src': locale_1.t("The <code>frame-src</code> directive specifies valid sources for nested\n  browsing contexts loading using elements such as\n  <code>&lt;frame&gt;</code> and <code>&lt;iframe&gt;</code>."),
    'worker-src': locale_1.t("The <code>worker-src</code> directive specifies valid sources for\n  <code>Worker<code>, <code>SharedWorker</code>, or\n  <code>ServiceWorker</code> scripts."),
};
//# sourceMappingURL=effectiveDirectives.jsx.map