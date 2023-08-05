Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var inlineStyle = function (p) {
    return p.inline
        ? react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n        align-items: center;\n      "], ["\n        align-items: center;\n      "]))) : react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n        flex-direction: column;\n        align-items: stretch;\n      "], ["\n        flex-direction: column;\n        align-items: stretch;\n      "])));
};
var getPadding = function (p) {
    return p.stacked && !p.inline
        ? react_1.css(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n        padding: 0 ", " ", " 0;\n      "], ["\n        padding: 0 ", " ", " 0;\n      "])), p.hasControlState ? 0 : space_1.default(2), space_1.default(2)) : react_1.css(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n        padding: ", " ", " ", " ", ";\n      "], ["\n        padding: ", " ", " ", " ", ";\n      "])), space_1.default(2), p.hasControlState ? 0 : space_1.default(2), space_1.default(2), space_1.default(2));
};
var FieldWrapper = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  ", "\n  ", "\n  display: flex;\n  transition: background 0.15s;\n\n  ", "\n\n  ", "\n\n\n  /* Better padding with form inside of a modal */\n  ", "\n\n  &:last-child {\n    border-bottom: none;\n    ", ";\n  }\n"], ["\n  ", "\n  ", "\n  display: flex;\n  transition: background 0.15s;\n\n  ", "\n\n  ", "\n\n\n  /* Better padding with form inside of a modal */\n  ", "\n\n  &:last-child {\n    border-bottom: none;\n    ", ";\n  }\n"])), getPadding, inlineStyle, function (p) {
    return !p.stacked && react_1.css(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n      border-bottom: 1px solid ", ";\n    "], ["\n      border-bottom: 1px solid ", ";\n    "])), p.theme.innerBorder);
}, function (p) {
    return p.highlighted && react_1.css(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n      position: relative;\n\n      &:after {\n        content: '';\n        display: block;\n        position: absolute;\n        top: -1px;\n        left: -1px;\n        right: -1px;\n        bottom: -1px;\n        border: 1px solid ", ";\n        pointer-events: none;\n      }\n    "], ["\n      position: relative;\n\n      &:after {\n        content: '';\n        display: block;\n        position: absolute;\n        top: -1px;\n        left: -1px;\n        right: -1px;\n        bottom: -1px;\n        border: 1px solid ", ";\n        pointer-events: none;\n      }\n    "])), p.theme.purple300);
}, function (p) {
    return !p.hasControlState && react_1.css(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n      [role='document'] & {\n        padding-right: 0;\n      }\n    "], ["\n      [role='document'] & {\n        padding-right: 0;\n      }\n    "])));
}, function (p) { return (p.stacked ? 'padding-bottom: 0' : ''); });
exports.default = FieldWrapper;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=fieldWrapper.jsx.map