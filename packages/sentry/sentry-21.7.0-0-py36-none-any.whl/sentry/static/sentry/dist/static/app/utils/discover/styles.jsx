Object.defineProperty(exports, "__esModule", { value: true });
exports.UserIcon = exports.FlexContainer = exports.BarContainer = exports.StyledShortId = exports.OverflowLink = exports.StyledDateTime = exports.NumberContainer = exports.VersionContainer = exports.Container = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var shortId_1 = tslib_1.__importDefault(require("app/components/shortId"));
var iconUser_1 = require("app/icons/iconUser");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
/**
 * Styled components used to render discover result sets.
 */
exports.Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
exports.VersionContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
exports.NumberContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n  ", ";\n"], ["\n  text-align: right;\n  ", ";\n"])), overflowEllipsis_1.default);
exports.StyledDateTime = styled_1.default(dateTime_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  ", ";\n"])), function (p) { return p.theme.gray300; }, overflowEllipsis_1.default);
exports.OverflowLink = styled_1.default(link_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
exports.StyledShortId = styled_1.default(shortId_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-start;\n"], ["\n  justify-content: flex-start;\n"])));
exports.BarContainer = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  max-width: 80px;\n  margin-left: auto;\n"], ["\n  max-width: 80px;\n  margin-left: auto;\n"])));
exports.FlexContainer = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
exports.UserIcon = styled_1.default(iconUser_1.IconUser)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  color: ", ";\n"], ["\n  margin-left: ", ";\n  color: ", ";\n"])), space_1.default(1), function (p) { return p.theme.gray400; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=styles.jsx.map