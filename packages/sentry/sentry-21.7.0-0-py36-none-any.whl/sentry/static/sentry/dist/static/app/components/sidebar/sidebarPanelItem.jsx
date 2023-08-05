Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var locale_1 = require("../../locale");
var externalLink_1 = tslib_1.__importDefault(require("../links/externalLink"));
var SidebarPanelItem = function (_a) {
    var hasSeen = _a.hasSeen, title = _a.title, image = _a.image, message = _a.message, link = _a.link, cta = _a.cta, children = _a.children;
    return (<SidebarPanelItemRoot>
    {title && <Title hasSeen={hasSeen}>{title}</Title>}
    {image && (<ImageBox>
        <img src={image}/>
      </ImageBox>)}
    {message && <Message>{message}</Message>}

    {children}

    {link && (<Text>
        <externalLink_1.default href={link}>{cta || locale_1.t('Read More')}</externalLink_1.default>
      </Text>)}
  </SidebarPanelItemRoot>);
};
exports.default = SidebarPanelItem;
var SidebarPanelItemRoot = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  line-height: 1.5;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  font-size: ", ";\n  padding: ", ";\n"], ["\n  line-height: 1.5;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  font-size: ", ";\n  padding: ", ";\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.background; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(3));
var ImageBox = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border: 1px solid #e1e4e5;\n  padding: ", ";\n  border-radius: 2px;\n"], ["\n  border: 1px solid #e1e4e5;\n  padding: ", ";\n  border-radius: 2px;\n"])), space_1.default(2));
var Title = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n  color: ", ";\n  ", ";\n\n  .culprit {\n    font-weight: normal;\n  }\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n  color: ", ";\n  ", ";\n\n  .culprit {\n    font-weight: normal;\n  }\n"])), function (p) { return p.theme.fontSizeLarge; }, space_1.default(1), function (p) { return p.theme.textColor; }, function (p) { return !p.hasSeen && 'font-weight: 600;'; });
var Text = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n\n  &:last-child {\n    margin-bottom: 0;\n  }\n"], ["\n  margin-bottom: ", ";\n\n  &:last-child {\n    margin-bottom: 0;\n  }\n"])), space_1.default(0.5));
var Message = styled_1.default(Text)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=sidebarPanelItem.jsx.map