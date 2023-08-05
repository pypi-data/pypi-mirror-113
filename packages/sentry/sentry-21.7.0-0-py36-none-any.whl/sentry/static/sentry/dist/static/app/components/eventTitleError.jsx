Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function EventTitleError() {
    return (<Wrapper>
      <Title>{locale_1.t('<unknown>')}</Title>
      <ErrorMessage>{locale_1.t('There was an error rendering the title')}</ErrorMessage>
    </Wrapper>);
}
exports.default = EventTitleError;
var Wrapper = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var Title = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.5));
var ErrorMessage = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  background: ", ";\n  font-size: ", ";\n  padding: 0 ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n"], ["\n  color: ", ";\n  background: ", ";\n  font-size: ", ";\n  padding: 0 ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n"])), function (p) { return p.theme.alert.error.iconColor; }, function (p) { return p.theme.alert.error.backgroundLight; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(0.5), function (p) { return p.theme.borderRadius; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=eventTitleError.jsx.map