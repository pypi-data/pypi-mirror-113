Object.defineProperty(exports, "__esModule", { value: true });
exports.KeyValueTableRow = exports.KeyValueTable = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.KeyValueTable = styled_1.default('dl')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 50% 50%;\n"], ["\n  display: grid;\n  grid-template-columns: 50% 50%;\n"])));
var KeyValueTableRow = function (_a) {
    var keyName = _a.keyName, value = _a.value;
    return (<React.Fragment>
      <Key>{keyName}</Key>
      <Value>{value}</Value>
    </React.Fragment>);
};
exports.KeyValueTableRow = KeyValueTableRow;
var commonStyles = function (_a) {
    var theme = _a.theme;
    return "\nfont-size: " + theme.fontSizeMedium + ";\npadding: " + space_1.default(0.5) + " " + space_1.default(1) + ";\nfont-weight: normal;\nline-height: inherit;\n" + overflowEllipsis_1.default + ";\n&:nth-of-type(2n-1) {\n  background-color: " + theme.backgroundSecondary + ";\n}\n";
};
var Key = styled_1.default('dt')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", ";\n  color: ", ";\n"], ["\n  ", ";\n  color: ", ";\n"])), commonStyles, function (p) { return p.theme.textColor; });
var Value = styled_1.default('dd')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", ";\n  color: ", ";\n  text-align: right;\n"], ["\n  ", ";\n  color: ", ";\n  text-align: right;\n"])), commonStyles, function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=keyValueTable.jsx.map