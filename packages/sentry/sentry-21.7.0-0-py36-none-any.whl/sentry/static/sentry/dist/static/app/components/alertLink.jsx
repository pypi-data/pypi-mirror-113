Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var AlertLink = /** @class */ (function (_super) {
    tslib_1.__extends(AlertLink, _super);
    function AlertLink() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AlertLink.prototype.render = function () {
        var _a = this.props, size = _a.size, priority = _a.priority, icon = _a.icon, children = _a.children, onClick = _a.onClick, withoutMarginBottom = _a.withoutMarginBottom, openInNewTab = _a.openInNewTab, to = _a.to, href = _a.href, dataTestId = _a["data-test-id"];
        return (<StyledLink data-test-id={dataTestId} to={to} href={href} onClick={onClick} size={size} priority={priority} withoutMarginBottom={withoutMarginBottom} openInNewTab={openInNewTab}>
        {icon && <IconWrapper>{icon}</IconWrapper>}
        <AlertLinkText>{children}</AlertLinkText>
        <IconLink>
          <icons_1.IconChevron direction="right"/>
        </IconLink>
      </StyledLink>);
    };
    AlertLink.defaultProps = {
        priority: 'warning',
        size: 'normal',
        withoutMarginBottom: false,
        openInNewTab: false,
    };
    return AlertLink;
}(React.Component));
exports.default = AlertLink;
var StyledLink = styled_1.default(function (_a) {
    var openInNewTab = _a.openInNewTab, to = _a.to, href = _a.href, props = tslib_1.__rest(_a, ["openInNewTab", "to", "href"]);
    var linkProps = omit_1.default(props, ['withoutMarginBottom', 'priority', 'size']);
    if (href) {
        return <externalLink_1.default {...linkProps} href={href} openInNewTab={openInNewTab}/>;
    }
    return <link_1.default {...linkProps} to={to || ''}/>;
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  background-color: ", ";\n  color: ", ";\n  border: 1px dashed ", ";\n  padding: ", ";\n  margin-bottom: ", ";\n  border-radius: 0.25em;\n  transition: 0.2s border-color;\n\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", "7f 0 0 0 2px;\n  }\n"], ["\n  display: flex;\n  background-color: ", ";\n  color: ", ";\n  border: 1px dashed ", ";\n  padding: ", ";\n  margin-bottom: ", ";\n  border-radius: 0.25em;\n  transition: 0.2s border-color;\n\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", "7f 0 0 0 2px;\n  }\n"])), function (p) { return p.theme.alert[p.priority].backgroundLight; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.alert[p.priority].border; }, function (p) { return (p.size === 'small' ? space_1.default(1) + " " + space_1.default(1.5) : space_1.default(2)); }, function (p) { return (p.withoutMarginBottom ? 0 : space_1.default(3)); }, function (p) { return p.theme.alert[p.priority].border; });
var IconWrapper = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin: ", " ", " ", " 0;\n"], ["\n  display: flex;\n  margin: ", " ", " ", " 0;\n"])), space_1.default(0.5), space_1.default(1.5), space_1.default(0.5));
var IconLink = styled_1.default(IconWrapper)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space_1.default(0.5));
var AlertLinkText = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  line-height: 1.5;\n  flex-grow: 1;\n"], ["\n  line-height: 1.5;\n  flex-grow: 1;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=alertLink.jsx.map