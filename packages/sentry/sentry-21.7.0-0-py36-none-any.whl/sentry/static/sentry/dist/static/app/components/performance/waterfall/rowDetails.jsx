Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrorTitle = exports.ErrorLevel = exports.ErrorDot = exports.ErrorMessageContent = exports.ErrorMessageTitle = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.ErrorMessageTitle = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
exports.ErrorMessageContent = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-template-columns: 16px 72px auto;\n  grid-gap: ", ";\n  margin-top: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-template-columns: 16px 72px auto;\n  grid-gap: ", ";\n  margin-top: ", ";\n"])), space_1.default(0.75), space_1.default(0.75));
exports.ErrorDot = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  content: '';\n  width: ", ";\n  min-width: ", ";\n  height: ", ";\n  margin-right: ", ";\n  border-radius: 100%;\n  flex: 1;\n"], ["\n  background-color: ", ";\n  content: '';\n  width: ", ";\n  min-width: ", ";\n  height: ", ";\n  margin-right: ", ";\n  border-radius: 100%;\n  flex: 1;\n"])), function (p) { return p.theme.level[p.level]; }, space_1.default(1), space_1.default(1), space_1.default(1), space_1.default(1));
exports.ErrorLevel = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  width: 80px;\n"], ["\n  width: 80px;\n"])));
exports.ErrorTitle = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=rowDetails.jsx.map