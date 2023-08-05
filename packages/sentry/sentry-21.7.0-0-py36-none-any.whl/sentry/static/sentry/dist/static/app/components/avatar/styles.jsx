Object.defineProperty(exports, "__esModule", { value: true });
exports.imageStyle = void 0;
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var imageStyle = function (props) { return react_1.css(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0px;\n  left: 0px;\n  border-radius: ", ";\n  ", "\n  ", "\n"], ["\n  position: absolute;\n  top: 0px;\n  left: 0px;\n  border-radius: ", ";\n  ", "\n  ", "\n"])), props.round ? '50%' : '3px', props.grayscale && react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n    padding: 1px;\n    filter: grayscale(100%);\n  "], ["\n    padding: 1px;\n    filter: grayscale(100%);\n  "]))), props.suggested && react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n    opacity: 50%;\n  "], ["\n    opacity: 50%;\n  "])))); };
exports.imageStyle = imageStyle;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=styles.jsx.map