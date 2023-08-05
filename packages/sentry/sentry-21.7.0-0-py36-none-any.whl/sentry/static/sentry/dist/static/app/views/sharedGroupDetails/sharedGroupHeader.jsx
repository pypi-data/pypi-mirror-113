Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var eventMessage_1 = tslib_1.__importDefault(require("app/components/events/eventMessage"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var unhandledTag_1 = tslib_1.__importStar(require("../organizationGroupDetails/unhandledTag"));
var SharedGroupHeader = function (_a) {
    var group = _a.group;
    return (<Wrapper>
    <Details>
      <Title>{group.title}</Title>
      <unhandledTag_1.TagAndMessageWrapper>
        {group.isUnhandled && <unhandledTag_1.default />}
        <eventMessage_1.default message={group.culprit}/>
      </unhandledTag_1.TagAndMessageWrapper>
    </Details>
  </Wrapper>);
};
exports.default = SharedGroupHeader;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", " ", " ", ";\n  border-bottom: ", ";\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.03);\n  position: relative;\n  margin: 0 0 ", ";\n"], ["\n  padding: ", " ", " ", " ", ";\n  border-bottom: ", ";\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.03);\n  position: relative;\n  margin: 0 0 ", ";\n"])), space_1.default(3), space_1.default(4), space_1.default(3), space_1.default(4), function (p) { return "1px solid " + p.theme.border; }, space_1.default(3));
var Details = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  max-width: 960px;\n  margin: 0 auto;\n"], ["\n  max-width: 960px;\n  margin: 0 auto;\n"])));
// TODO(style): the color #161319 is not yet in the color object of the theme
var Title = styled_1.default('h3')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: #161319;\n  margin: 0 0 ", ";\n  overflow-wrap: break-word;\n  line-height: 1.2;\n  font-size: ", ";\n  @media (min-width: ", ") {\n    font-size: ", ";\n    line-height: 1.1;\n    ", ";\n  }\n"], ["\n  color: #161319;\n  margin: 0 0 ", ";\n  overflow-wrap: break-word;\n  line-height: 1.2;\n  font-size: ", ";\n  @media (min-width: ", ") {\n    font-size: ", ";\n    line-height: 1.1;\n    ", ";\n  }\n"])), space_1.default(1), function (p) { return p.theme.fontSizeExtraLarge; }, function (props) { return props.theme.breakpoints[0]; }, function (p) { return p.theme.headerFontSize; }, overflowEllipsis_1.default);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sharedGroupHeader.jsx.map