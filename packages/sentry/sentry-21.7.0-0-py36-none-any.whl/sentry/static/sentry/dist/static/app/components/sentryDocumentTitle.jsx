Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
function SentryDocumentTitle(_a) {
    var title = _a.title, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, children = _a.children;
    function getDocTitle() {
        if (!orgSlug && !projectSlug) {
            return title;
        }
        if (orgSlug && projectSlug) {
            return title + " - " + orgSlug + " - " + projectSlug;
        }
        if (orgSlug) {
            return title + " - " + orgSlug;
        }
        return title + " - " + projectSlug;
    }
    var docTitle = getDocTitle();
    return (<react_document_title_1.default title={docTitle + " - Sentry"}>
      {children}
    </react_document_title_1.default>);
}
exports.default = SentryDocumentTitle;
//# sourceMappingURL=sentryDocumentTitle.jsx.map