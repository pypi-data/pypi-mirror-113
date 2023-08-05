Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function OnboardingPanel(_a) {
    var className = _a.className, image = _a.image, children = _a.children;
    return (<panels_1.Panel className={className}>
      <Container>
        <IlloBox>{image}</IlloBox>
        <StyledBox>{children}</StyledBox>
      </Container>
    </panels_1.Panel>);
}
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  position: relative;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n    flex-direction: row;\n    justify-content: center;\n    flex-wrap: wrap;\n    min-height: 300px;\n    max-width: 1000px;\n    margin: 0 auto;\n  }\n\n  @media (min-width: ", ") {\n    min-height: 350px;\n  }\n"], ["\n  padding: ", ";\n  position: relative;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n    flex-direction: row;\n    justify-content: center;\n    flex-wrap: wrap;\n    min-height: 300px;\n    max-width: 1000px;\n    margin: 0 auto;\n  }\n\n  @media (min-width: ", ") {\n    min-height: 350px;\n  }\n"])), space_1.default(3), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; });
var StyledBox = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  z-index: 1;\n\n  @media (min-width: ", ") {\n    flex: 2;\n  }\n"], ["\n  z-index: 1;\n\n  @media (min-width: ", ") {\n    flex: 2;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var IlloBox = styled_1.default(StyledBox)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  min-height: 100px;\n  max-width: 300px;\n  margin: ", " auto;\n\n  @media (min-width: ", ") {\n    flex: 1;\n    margin: ", ";\n    max-width: auto;\n  }\n"], ["\n  position: relative;\n  min-height: 100px;\n  max-width: 300px;\n  margin: ", " auto;\n\n  @media (min-width: ", ") {\n    flex: 1;\n    margin: ", ";\n    max-width: auto;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; }, space_1.default(3));
exports.default = OnboardingPanel;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=onboardingPanel.jsx.map