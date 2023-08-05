Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
exports.default = react_1.forwardRef(function MultiSelectControl(props, ref) {
    return <selectControl_1.default forwardedRef={ref} {...props} multiple/>;
});
//# sourceMappingURL=multiSelectControl.jsx.map