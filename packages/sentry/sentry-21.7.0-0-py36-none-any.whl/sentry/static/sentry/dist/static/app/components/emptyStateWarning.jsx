Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var EmptyStateWarning = function (_a) {
    var _b = _a.small, small = _b === void 0 ? false : _b, _c = _a.withIcon, withIcon = _c === void 0 ? true : _c, children = _a.children, className = _a.className;
    return small ? (<emptyMessage_1.default className={className}>
      <SmallMessage>
        {withIcon && <StyledIconSearch color="gray300" size="lg"/>}
        {children}
      </SmallMessage>
    </emptyMessage_1.default>) : (<EmptyStreamWrapper data-test-id="empty-state" className={className}>
      {withIcon && <icons_1.IconSearch size="54px"/>}
      {children}
    </EmptyStreamWrapper>);
};
var EmptyStreamWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-align: center;\n  font-size: 22px;\n  padding: 48px ", ";\n\n  p {\n    line-height: 1.2;\n    margin: 0 auto 20px;\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  svg {\n    fill: ", ";\n    margin-bottom: ", ";\n  }\n"], ["\n  text-align: center;\n  font-size: 22px;\n  padding: 48px ", ";\n\n  p {\n    line-height: 1.2;\n    margin: 0 auto 20px;\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  svg {\n    fill: ", ";\n    margin-bottom: ", ";\n  }\n"])), space_1.default(1), function (p) { return p.theme.gray200; }, space_1.default(2));
var SmallMessage = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  line-height: 1em;\n"], ["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  line-height: 1em;\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeExtraLarge; });
var StyledIconSearch = styled_1.default(icons_1.IconSearch)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
exports.default = EmptyStateWarning;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=emptyStateWarning.jsx.map