Object.defineProperty(exports, "__esModule", { value: true });
exports.IconArrow = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var svgIcon_1 = tslib_1.__importDefault(require("./svgIcon"));
var IconArrow = React.forwardRef(function IconArrow(_a, ref) {
    var _b = _a.direction, direction = _b === void 0 ? 'up' : _b, props = tslib_1.__rest(_a, ["direction"]);
    return (<svgIcon_1.default {...props} ref={ref} css={direction
            ? direction === 'down'
                ? // Down arrows have a zoom issue with Firefox inside of tables due to rotate.
                 
                // Since arrows are symmetric, scaling to only flip vertically works to fix the issue.
                react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                transform: scale(1, -1);\n              "], ["\n                transform: scale(1, -1);\n              "]))) : react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n                transform: rotate(", "deg);\n              "], ["\n                transform: rotate(", "deg);\n              "])), theme_1.default.iconDirections[direction])
            : undefined}>
      <path d="M13.76,7.32a.74.74,0,0,1-.53-.22L8,1.87,2.77,7.1A.75.75,0,1,1,1.71,6L7.47.28a.74.74,0,0,1,1.06,0L14.29,6a.75.75,0,0,1,0,1.06A.74.74,0,0,1,13.76,7.32Z"/>
      <path d="M8,15.94a.75.75,0,0,1-.75-.75V.81a.75.75,0,0,1,1.5,0V15.19A.75.75,0,0,1,8,15.94Z"/>
    </svgIcon_1.default>);
});
exports.IconArrow = IconArrow;
IconArrow.displayName = 'IconArrow';
var templateObject_1, templateObject_2;
//# sourceMappingURL=iconArrow.jsx.map