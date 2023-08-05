Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_autosize_textarea_1 = tslib_1.__importDefault(require("react-autosize-textarea"));
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var input_1 = require("app/styles/input");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var TextAreaControl = React.forwardRef(function TextAreaControl(_a, ref) {
    var autosize = _a.autosize, rows = _a.rows, maxRows = _a.maxRows, p = tslib_1.__rest(_a, ["autosize", "rows", "maxRows"]);
    return autosize ? (<react_autosize_textarea_1.default {...p} async ref={ref} rows={rows ? rows : 2} maxRows={maxRows}/>) : (<textarea ref={ref} {...p}/>);
});
TextAreaControl.displayName = 'TextAreaControl';
var propFilter = function (p) {
    return ['autosize', 'rows', 'maxRows'].includes(p) || is_prop_valid_1.default(p);
};
var TextArea = styled_1.default(TextAreaControl, { shouldForwardProp: propFilter })(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  min-height: 40px;\n  padding: calc(", " - 1px) ", ";\n  line-height: 1.5em;\n  ", "\n"], ["\n  ", ";\n  min-height: 40px;\n  padding: calc(", " - 1px) ", ";\n  line-height: 1.5em;\n  ", "\n"])), input_1.inputStyles, space_1.default(1), space_1.default(1), function (p) {
    return p.autosize &&
        "\n      height: auto;\n      padding: calc(" + space_1.default(1) + " - 2px) " + space_1.default(1) + ";\n      line-height: 1.6em;\n    ";
});
exports.default = TextArea;
var templateObject_1;
//# sourceMappingURL=textarea.jsx.map