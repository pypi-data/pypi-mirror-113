Object.defineProperty(exports, "__esModule", { value: true });
exports.SectionSubtext = exports.MetaData = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function MetaData(_a) {
    var headingText = _a.headingText, tooltipText = _a.tooltipText, bodyText = _a.bodyText, subtext = _a.subtext, badge = _a.badge;
    return (<HeaderInfo>
      <StyledSectionHeading>
        {headingText}
        <questionTooltip_1.default position="top" size="sm" containerDisplayMode="block" title={tooltipText}/>
        {badge && <StyledFeatureBadge type={badge}/>}
      </StyledSectionHeading>
      <SectionBody>{bodyText}</SectionBody>
      <exports.SectionSubtext>{subtext}</exports.SectionSubtext>
    </HeaderInfo>);
}
exports.MetaData = MetaData;
var HeaderInfo = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 78px;\n"], ["\n  height: 78px;\n"])));
var StyledSectionHeading = styled_1.default(styles_1.SectionHeading)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var SectionBody = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  padding: ", " 0;\n  max-height: 32px;\n"], ["\n  font-size: ", ";\n  padding: ", " 0;\n  max-height: 32px;\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space_1.default(0.5));
var StyledFeatureBadge = styled_1.default(featureBadge_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
exports.SectionSubtext = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return (p.type === 'error' ? p.theme.error : p.theme.subText); }, function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=styles.jsx.map