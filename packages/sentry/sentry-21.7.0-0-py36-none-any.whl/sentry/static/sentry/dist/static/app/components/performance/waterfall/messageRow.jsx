Object.defineProperty(exports, "__esModule", { value: true });
exports.MessageRow = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var constants_1 = require("app/components/performance/waterfall/constants");
var row_1 = require("app/components/performance/waterfall/row");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.MessageRow = styled_1.default(row_1.Row)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: block;\n  cursor: auto;\n  line-height: ", "px;\n  padding-left: ", ";\n  padding-right: ", ";\n  color: ", ";\n  background-color: ", ";\n  outline: 1px solid ", ";\n  font-size: ", ";\n\n  z-index: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: block;\n  cursor: auto;\n  line-height: ", "px;\n  padding-left: ", ";\n  padding-right: ", ";\n  color: ", ";\n  background-color: ", ";\n  outline: 1px solid ", ";\n  font-size: ", ";\n\n  z-index: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"])), constants_1.ROW_HEIGHT, space_1.default(1), space_1.default(1), function (p) { return p.theme.gray300; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.zIndex.traceView.rowInfoMessage; }, space_1.default(2));
var templateObject_1;
//# sourceMappingURL=messageRow.jsx.map