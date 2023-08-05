Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var radioBoolean_1 = tslib_1.__importDefault(require("./controls/radioBoolean"));
var inputField_1 = tslib_1.__importDefault(require("./inputField"));
function RadioBooleanField(props) {
    return (<inputField_1.default {...props} field={function (fieldProps) { return (<radioBoolean_1.default {...omit_1.default(fieldProps, ['onKeyDown', 'children'])}/>); }}/>);
}
exports.default = RadioBooleanField;
//# sourceMappingURL=radioBooleanField.jsx.map