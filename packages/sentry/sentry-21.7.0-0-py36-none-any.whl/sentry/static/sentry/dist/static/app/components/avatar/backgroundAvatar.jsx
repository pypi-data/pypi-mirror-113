Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/avatar/styles");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
/**
 * Creates an avatar placeholder that is used when showing multiple
 * suggested assignees
 */
var BackgroundAvatar = styled_1.default(function (_a) {
    var _round = _a.round, forwardedRef = _a.forwardedRef, props = tslib_1.__rest(_a, ["round", "forwardedRef"]);
    return (<svg ref={forwardedRef} viewBox="0 0 120 120" {...props}>
      <rect x="0" y="0" width="120" height="120" rx="15" ry="15" fill={theme_1.default.purple100}/>
    </svg>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), styles_1.imageStyle);
BackgroundAvatar.defaultProps = {
    round: false,
    suggested: true,
};
exports.default = React.forwardRef(function (props, ref) { return (<BackgroundAvatar forwardedRef={ref} {...props}/>); });
var templateObject_1;
//# sourceMappingURL=backgroundAvatar.jsx.map