Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var kebabCase_1 = tslib_1.__importDefault(require("lodash/kebabCase"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var eventDataSection_1 = tslib_1.__importStar(require("app/components/events/eventDataSection"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function DataSection(_a) {
    var title = _a.title, description = _a.description, children = _a.children;
    var type = kebabCase_1.default(title);
    return (<StyledEventDataSection type={type} title={<TitleWrapper>
          <guideAnchor_1.default target={type} position="bottom">
            <Title>{title}</Title>
          </guideAnchor_1.default>
          <questionTooltip_1.default size="xs" position="top" title={description}/>
        </TitleWrapper>} wrapTitle={false}>
      {children}
    </StyledEventDataSection>);
}
exports.default = DataSection;
var TitleWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, max-content);\n  grid-gap: ", ";\n  align-items: center;\n  padding: ", " 0;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, max-content);\n  grid-gap: ", ";\n  align-items: center;\n  padding: ", " 0;\n"])), space_1.default(0.5), space_1.default(0.75));
var Title = styled_1.default('h3')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  padding: 0 !important;\n  height: 14px;\n"], ["\n  margin-bottom: 0;\n  padding: 0 !important;\n  height: 14px;\n"])));
var StyledEventDataSection = styled_1.default(eventDataSection_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", " {\n    flex: 1;\n  }\n\n  @media (min-width: ", ") {\n    && {\n      padding: 0;\n      border: 0;\n    }\n  }\n"], ["\n  ", " {\n    flex: 1;\n  }\n\n  @media (min-width: ", ") {\n    && {\n      padding: 0;\n      border: 0;\n    }\n  }\n"])), eventDataSection_1.SectionContents, function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=dataSection.jsx.map