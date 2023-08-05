Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var MenuHeader = styled_1.default(menuItem_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-transform: uppercase;\n  font-weight: 600;\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n"], ["\n  text-transform: uppercase;\n  font-weight: 600;\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.innerBorder; }, space_1.default(1));
MenuHeader.defaultProps = {
    header: true,
};
exports.default = MenuHeader;
var templateObject_1;
//# sourceMappingURL=menuHeader.jsx.map