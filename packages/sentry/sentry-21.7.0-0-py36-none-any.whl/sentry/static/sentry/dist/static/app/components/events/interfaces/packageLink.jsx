Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("app/components/events/interfaces/frame/utils");
var stacktracePreview_1 = require("app/components/stacktracePreview");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/utils");
var PackageLink = /** @class */ (function (_super) {
    tslib_1.__extends(PackageLink, _super);
    function PackageLink() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function (event) {
            var _a = _this.props, isClickable = _a.isClickable, onClick = _a.onClick;
            if (isClickable) {
                onClick(event);
            }
        };
        return _this;
    }
    PackageLink.prototype.render = function () {
        var _a = this.props, packagePath = _a.packagePath, isClickable = _a.isClickable, withLeadHint = _a.withLeadHint, children = _a.children, includeSystemFrames = _a.includeSystemFrames, isHoverPreviewed = _a.isHoverPreviewed;
        return (<Package onClick={this.handleClick} isClickable={isClickable} withLeadHint={withLeadHint} includeSystemFrames={includeSystemFrames}>
        {utils_2.defined(packagePath) ? (<tooltip_1.default title={packagePath} delay={isHoverPreviewed ? stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY : undefined}>
            <PackageName isClickable={isClickable} withLeadHint={withLeadHint} includeSystemFrames={includeSystemFrames}>
              {utils_1.trimPackage(packagePath)}
            </PackageName>
          </tooltip_1.default>) : (<span>{'<unknown>'}</span>)}
        {children}
      </Package>);
    };
    return PackageLink;
}(React.Component));
var Package = styled_1.default('a')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 13px;\n  font-weight: bold;\n  padding: 0 0 0 ", ";\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n  cursor: ", ";\n  display: flex;\n  align-items: center;\n\n  ", "\n\n  @media (min-width: ", ") and (max-width: ", ") {\n    ", "\n  }\n"], ["\n  font-size: 13px;\n  font-weight: bold;\n  padding: 0 0 0 ", ";\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n  cursor: ", ";\n  display: flex;\n  align-items: center;\n\n  ", "\n\n  @media (min-width: ", ") and (max-width: ", ") {\n    ", "\n  }\n"])), space_1.default(0.5), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; }, function (p) { return (p.isClickable ? 'pointer' : 'default'); }, function (p) {
    return p.withLeadHint && (p.includeSystemFrames ? "max-width: 89px;" : "max-width: 76px;");
}, function (p) { return p.theme.breakpoints[2]; }, function (p) {
    return p.theme.breakpoints[3];
}, function (p) {
    return p.withLeadHint && (p.includeSystemFrames ? "max-width: 76px;" : "max-width: 63px;");
});
var PackageName = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  max-width: ", ";\n  ", "\n"], ["\n  max-width: ", ";\n  ", "\n"])), function (p) {
    return p.withLeadHint && p.isClickable && !p.includeSystemFrames ? '45px' : '104px';
}, overflowEllipsis_1.default);
exports.default = PackageLink;
var templateObject_1, templateObject_2;
//# sourceMappingURL=packageLink.jsx.map