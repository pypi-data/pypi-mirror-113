Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var inlineStyle = function (p) {
    return p.inline
        ? react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n        width: 50%;\n        padding-right: 10px;\n        flex-shrink: 0;\n      "], ["\n        width: 50%;\n        padding-right: 10px;\n        flex-shrink: 0;\n      "]))) : react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n        margin-bottom: ", ";\n      "], ["\n        margin-bottom: ", ";\n      "])), space_1.default(1));
};
var FieldDescription = styled_1.default('label')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-weight: normal;\n  margin-bottom: 0;\n\n  ", ";\n"], ["\n  font-weight: normal;\n  margin-bottom: 0;\n\n  ", ";\n"])), inlineStyle);
exports.default = FieldDescription;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=fieldDescription.jsx.map