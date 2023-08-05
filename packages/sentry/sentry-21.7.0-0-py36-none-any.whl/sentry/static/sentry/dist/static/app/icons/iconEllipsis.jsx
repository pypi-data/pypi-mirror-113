Object.defineProperty(exports, "__esModule", { value: true });
exports.IconEllipsis = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var svgIcon_1 = tslib_1.__importDefault(require("./svgIcon"));
var IconEllipsis = React.forwardRef(function IconEllipsis(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <circle cx="8" cy="8" r="1.31"/>
      <circle cx="1.31" cy="8" r="1.31"/>
      <circle cx="14.69" cy="8" r="1.31"/>
    </svgIcon_1.default>);
});
exports.IconEllipsis = IconEllipsis;
IconEllipsis.displayName = 'IconEllipsis';
//# sourceMappingURL=iconEllipsis.jsx.map