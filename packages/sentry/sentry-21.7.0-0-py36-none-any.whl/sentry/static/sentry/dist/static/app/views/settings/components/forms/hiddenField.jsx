Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var inputField_1 = tslib_1.__importDefault(require("./inputField"));
function HiddenField(props) {
    return <HiddenInputField {...props} type="hidden"/>;
}
exports.default = HiddenField;
var HiddenInputField = styled_1.default(inputField_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: none;\n"], ["\n  display: none;\n"])));
var templateObject_1;
//# sourceMappingURL=hiddenField.jsx.map