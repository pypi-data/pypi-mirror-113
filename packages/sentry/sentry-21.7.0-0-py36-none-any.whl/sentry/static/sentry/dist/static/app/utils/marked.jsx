Object.defineProperty(exports, "__esModule", { value: true });
exports.singleLineRenderer = void 0;
var tslib_1 = require("tslib");
var dompurify_1 = tslib_1.__importDefault(require("dompurify"));
var marked_1 = tslib_1.__importDefault(require("marked")); // eslint-disable-line no-restricted-imports
var constants_1 = require("app/constants");
// Only https and mailto, (e.g. no javascript, vbscript, data protocols)
var safeLinkPattern = /^(https?:|mailto:)/i;
var safeImagePattern = /^https?:\/\/./i;
function isSafeHref(href, pattern) {
    try {
        return pattern.test(decodeURIComponent(unescape(href)));
    }
    catch (_a) {
        return false;
    }
}
/**
 * Implementation of marked.Renderer which additonally sanitizes URLs.
 */
var SafeRenderer = /** @class */ (function (_super) {
    tslib_1.__extends(SafeRenderer, _super);
    function SafeRenderer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SafeRenderer.prototype.link = function (href, title, text) {
        // For a bad link, just return the plain text href
        if (!isSafeHref(href, safeLinkPattern)) {
            return href;
        }
        var out = "<a href=\"" + href + "\"" + (title ? " title=\"" + title + "\"" : '') + ">" + text + "</a>";
        return dompurify_1.default.sanitize(out);
    };
    SafeRenderer.prototype.image = function (href, title, text) {
        // For a bad image, return an empty string
        if (this.options.sanitize && !isSafeHref(href, safeImagePattern)) {
            return '';
        }
        return "<img src=\"" + href + "\" alt=\"" + text + "\"" + (title ? " title=\"" + title + "\"" : '') + " />";
    };
    return SafeRenderer;
}(marked_1.default.Renderer));
var NoParagraphRenderer = /** @class */ (function (_super) {
    tslib_1.__extends(NoParagraphRenderer, _super);
    function NoParagraphRenderer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NoParagraphRenderer.prototype.paragraph = function (text) {
        return text;
    };
    return NoParagraphRenderer;
}(SafeRenderer));
marked_1.default.setOptions({
    renderer: new SafeRenderer(),
    sanitize: true,
    // Silence sanitize deprecation warning in test / ci (CI sets NODE_NV
    // to production, but specifies `CI`).
    //
    // [!!] This has the side effect of causing failed markdown content to render
    //      as a html error, instead of throwing an exception, however none of
    //      our tests are rendering failed markdown so this is likely a safe
    //      tradeoff to turn off off the deprecation warning.
    silent: !!constants_1.IS_ACCEPTANCE_TEST || constants_1.NODE_ENV === 'test',
});
var sanitizedMarked = function () {
    var args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        args[_i] = arguments[_i];
    }
    return dompurify_1.default.sanitize(marked_1.default.apply(void 0, tslib_1.__spreadArray([], tslib_1.__read(args))));
};
var singleLineRenderer = function (text, options) {
    if (options === void 0) { options = {}; }
    return sanitizedMarked(text, tslib_1.__assign(tslib_1.__assign({}, options), { renderer: new NoParagraphRenderer() }));
};
exports.singleLineRenderer = singleLineRenderer;
exports.default = sanitizedMarked;
//# sourceMappingURL=marked.jsx.map