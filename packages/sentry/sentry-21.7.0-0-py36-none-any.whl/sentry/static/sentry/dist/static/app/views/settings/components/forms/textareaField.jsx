Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var textarea_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/textarea"));
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
function TextareaField(_a) {
    var monospace = _a.monospace, rows = _a.rows, autosize = _a.autosize, props = tslib_1.__rest(_a, ["monospace", "rows", "autosize"]);
    return (<inputField_1.default {...props} field={function (fieldProps) { return (<textarea_1.default {...{ monospace: monospace, rows: rows, autosize: autosize }} {...omit_1.default(fieldProps, ['onKeyDown', 'children'])}/>); }}/>);
}
exports.default = TextareaField;
//# sourceMappingURL=textareaField.jsx.map