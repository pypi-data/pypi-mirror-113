Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
function Input(_a) {
    var className = _a.className, otherProps = tslib_1.__rest(_a, ["className"]);
    return (<input className={classnames_1.default('form-control', className)} {...omit_1.default(otherProps, 'children')}/>);
}
exports.default = Input;
//# sourceMappingURL=input.jsx.map