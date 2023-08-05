Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styles_1 = require("./styles");
var Icon = React.memo(function (_a) {
    var icon = _a.icon, color = _a.color, size = _a.size;
    var Svg = icon;
    return (<styles_1.IconWrapper color={color}>
      <Svg size={size}/>
    </styles_1.IconWrapper>);
});
exports.default = Icon;
//# sourceMappingURL=icon.jsx.map