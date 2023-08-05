Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ExternalLink = React.forwardRef(function ExternalLink(_a, ref) {
    var _b = _a.openInNewTab, openInNewTab = _b === void 0 ? true : _b, props = tslib_1.__rest(_a, ["openInNewTab"]);
    var anchorProps = openInNewTab ? { target: '_blank', rel: 'noreferrer noopener' } : {};
    return <a ref={ref} {...anchorProps} {...props}/>;
});
exports.default = ExternalLink;
//# sourceMappingURL=externalLink.jsx.map