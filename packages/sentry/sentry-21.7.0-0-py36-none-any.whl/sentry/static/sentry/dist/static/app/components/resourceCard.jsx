Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var ResourceCard = function (_a) {
    var title = _a.title, link = _a.link, imgUrl = _a.imgUrl;
    return (<ResourceCardWrapper onClick={function () { return analytics_1.analytics('orgdash.resource_clicked', { link: link, title: title }); }}>
    <StyledLink href={link}>
      <StyledImg src={imgUrl} alt={title}/>
      <StyledTitle>{title}</StyledTitle>
    </StyledLink>
  </ResourceCardWrapper>);
};
exports.default = ResourceCard;
var ResourceCardWrapper = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  padding: ", ";\n  margin-bottom: 0;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  padding: ", ";\n  margin-bottom: 0;\n"])), space_1.default(3));
var StyledLink = styled_1.default(externalLink_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var StyledImg = styled_1.default('img')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: block;\n  margin: 0 auto ", " auto;\n  height: 160px;\n"], ["\n  display: block;\n  margin: 0 auto ", " auto;\n  height: 160px;\n"])), space_1.default(3));
var StyledTitle = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  text-align: center;\n  font-weight: bold;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  text-align: center;\n  font-weight: bold;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeLarge; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=resourceCard.jsx.map