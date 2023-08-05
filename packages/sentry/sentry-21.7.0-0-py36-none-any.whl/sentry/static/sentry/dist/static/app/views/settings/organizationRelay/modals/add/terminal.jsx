Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Terminal = function (_a) {
    var command = _a.command;
    return (<Wrapper>
    <Prompt>{'\u0024'}</Prompt>
    {command}
  </Wrapper>);
};
exports.default = Terminal;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  padding: ", " ", ";\n  font-family: ", ";\n  color: ", ";\n  border-radius: ", ";\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"], ["\n  background: ", ";\n  padding: ", " ", ";\n  font-family: ", ";\n  color: ", ";\n  border-radius: ", ";\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"])), function (p) { return p.theme.gray500; }, space_1.default(1.5), space_1.default(3), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.white; }, function (p) { return p.theme.borderRadius; }, space_1.default(0.75));
var Prompt = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=terminal.jsx.map