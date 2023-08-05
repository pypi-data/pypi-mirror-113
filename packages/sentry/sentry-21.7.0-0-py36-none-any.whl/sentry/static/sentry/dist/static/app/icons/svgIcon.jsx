Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var SvgIcon = React.forwardRef(function SvgIcon(_a, ref) {
    var _b, _c;
    var theme = _a.theme, _d = _a.color, providedColor = _d === void 0 ? 'currentColor' : _d, _e = _a.size, providedSize = _e === void 0 ? 'sm' : _e, _f = _a.viewBox, viewBox = _f === void 0 ? '0 0 16 16' : _f, props = tslib_1.__rest(_a, ["theme", "color", "size", "viewBox"]);
    var color = (_b = theme[providedColor]) !== null && _b !== void 0 ? _b : providedColor;
    var size = (_c = theme.iconSizes[providedSize]) !== null && _c !== void 0 ? _c : providedSize;
    return (<svg {...props} viewBox={viewBox} fill={color} height={size} width={size} ref={ref}/>);
});
exports.default = react_1.withTheme(SvgIcon);
//# sourceMappingURL=svgIcon.jsx.map