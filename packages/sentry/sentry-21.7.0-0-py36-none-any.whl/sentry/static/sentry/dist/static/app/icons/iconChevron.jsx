Object.defineProperty(exports, "__esModule", { value: true });
exports.IconChevron = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var svgIcon_1 = tslib_1.__importDefault(require("./svgIcon"));
var IconChevron = React.forwardRef(function IconChevron(_a, ref) {
    var _b = _a.isCircled, isCircled = _b === void 0 ? false : _b, _c = _a.direction, direction = _c === void 0 ? 'up' : _c, props = tslib_1.__rest(_a, ["isCircled", "direction"]);
    return (<svgIcon_1.default {...props} ref={ref} css={direction
            ? react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n              transition: transform 120ms ease-in-out;\n              transform: rotate(", "deg);\n            "], ["\n              transition: transform 120ms ease-in-out;\n              transform: rotate(", "deg);\n            "])), theme_1.default.iconDirections[direction]) : undefined}>
      {isCircled ? (<React.Fragment>
          <path d="M8,16a8,8,0,1,1,8-8A8,8,0,0,1,8,16ZM8,1.53A6.47,6.47,0,1,0,14.47,8,6.47,6.47,0,0,0,8,1.53Z"/>
          <path d="M11.12,9.87a.73.73,0,0,1-.53-.22L8,7.07,5.41,9.65a.74.74,0,0,1-1.06,0,.75.75,0,0,1,0-1.06L7.47,5.48a.74.74,0,0,1,1.06,0l3.12,3.11a.75.75,0,0,1,0,1.06A.74.74,0,0,1,11.12,9.87Z"/>
        </React.Fragment>) : (<path d="M14,11.75a.74.74,0,0,1-.53-.22L8,6.06,2.53,11.53a.75.75,0,0,1-1.06-1.06l6-6a.75.75,0,0,1,1.06,0l6,6a.75.75,0,0,1,0,1.06A.74.74,0,0,1,14,11.75Z"/>)}
    </svgIcon_1.default>);
});
exports.IconChevron = IconChevron;
IconChevron.displayName = 'IconChevron';
var templateObject_1;
//# sourceMappingURL=iconChevron.jsx.map