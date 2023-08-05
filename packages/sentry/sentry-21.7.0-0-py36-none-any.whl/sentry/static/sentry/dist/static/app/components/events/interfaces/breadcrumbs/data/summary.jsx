Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var contextData_1 = tslib_1.__importDefault(require("app/components/contextData"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function Summary(_a) {
    var kvData = _a.kvData, children = _a.children;
    if (!kvData || !Object.keys(kvData).length) {
        if (!children) {
            return null;
        }
        return (<Wrapper>
        <StyledCode>{children}</StyledCode>
      </Wrapper>);
    }
    return (<Wrapper>
      {children && <StyledCode>{children}</StyledCode>}
      <ContextDataWrapper>
        <contextData_1.default data={kvData} withAnnotatedText/>
      </ContextDataWrapper>
    </Wrapper>);
}
exports.default = Summary;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  max-height: 100%;\n  height: 100%;\n  word-break: break-all;\n  font-size: ", ";\n  font-family: ", ";\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  max-height: 100%;\n  height: 100%;\n  word-break: break-all;\n  font-size: ", ";\n  font-family: ", ";\n  display: grid;\n  grid-gap: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.text.familyMono; }, space_1.default(0.5));
var ContextDataWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  background: ", ";\n  border-radius: ", ";\n  max-height: 100%;\n  height: 100%;\n  overflow: hidden;\n\n  pre {\n    background: ", ";\n    margin: 0;\n    padding: 0;\n    overflow: hidden;\n    overflow-y: auto;\n    max-height: 100%;\n  }\n"], ["\n  padding: ", ";\n  background: ", ";\n  border-radius: ", ";\n  max-height: 100%;\n  height: 100%;\n  overflow: hidden;\n\n  pre {\n    background: ", ";\n    margin: 0;\n    padding: 0;\n    overflow: hidden;\n    overflow-y: auto;\n    max-height: 100%;\n  }\n"])), space_1.default(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.backgroundSecondary; });
var StyledCode = styled_1.default('code')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  line-height: 26px;\n  color: inherit;\n  font-size: inherit;\n  white-space: pre-wrap;\n  background: none;\n  padding: 0;\n"], ["\n  line-height: 26px;\n  color: inherit;\n  font-size: inherit;\n  white-space: pre-wrap;\n  background: none;\n  padding: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=summary.jsx.map