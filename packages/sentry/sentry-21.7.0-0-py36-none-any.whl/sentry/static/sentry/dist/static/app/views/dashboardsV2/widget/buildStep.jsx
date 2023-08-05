Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function BuildStep(_a) {
    var title = _a.title, description = _a.description, children = _a.children;
    return (<StyledListItem>
      <Header>
        <Description>{title}</Description>
        <SubDescription>{description}</SubDescription>
      </Header>
      <Content>{children}</Content>
    </StyledListItem>);
}
exports.default = BuildStep;
var StyledListItem = styled_1.default(listItem_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(2));
var Description = styled_1.default('h4')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-weight: 400;\n  margin-bottom: 0;\n"], ["\n  font-weight: 400;\n  margin-bottom: 0;\n"])));
var SubDescription = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; });
var Header = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(0.5));
var Content = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=buildStep.jsx.map