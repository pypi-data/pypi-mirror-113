Object.defineProperty(exports, "__esModule", { value: true });
exports.alertStyles = void 0;
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importStar(require("react"));
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var DEFAULT_TYPE = 'info';
var IconWrapper = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-right: ", ";\n\n  /* Give the wrapper an explicit height so icons are line height with the\n   * (common) line height. */\n  height: 22px;\n  align-items: center;\n"], ["\n  display: flex;\n  margin-right: ", ";\n\n  /* Give the wrapper an explicit height so icons are line height with the\n   * (common) line height. */\n  height: 22px;\n  align-items: center;\n"])), space_1.default(1));
var getAlertColorStyles = function (_a) {
    var backgroundLight = _a.backgroundLight, border = _a.border, iconColor = _a.iconColor;
    return react_2.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  border: 1px solid ", ";\n  ", " {\n    color: ", ";\n  }\n"], ["\n  background: ", ";\n  border: 1px solid ", ";\n  ", " {\n    color: ", ";\n  }\n"])), backgroundLight, border, IconWrapper, iconColor);
};
var getSystemAlertColorStyles = function (_a) {
    var backgroundLight = _a.backgroundLight, border = _a.border, iconColor = _a.iconColor;
    return react_2.css(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  border: 0;\n  border-radius: 0;\n  border-bottom: 1px solid ", ";\n  ", " {\n    color: ", ";\n  }\n"], ["\n  background: ", ";\n  border: 0;\n  border-radius: 0;\n  border-bottom: 1px solid ", ";\n  ", " {\n    color: ", ";\n  }\n"])), backgroundLight, border, IconWrapper, iconColor);
};
var alertStyles = function (_a) {
    var theme = _a.theme, _b = _a.type, type = _b === void 0 ? DEFAULT_TYPE : _b, system = _a.system;
    return react_2.css(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  margin: 0 0 ", ";\n  padding: ", " ", ";\n  font-size: 15px;\n  box-shadow: ", ";\n  border-radius: ", ";\n  background: ", ";\n  border: 1px solid ", ";\n\n  a:not([role='button']) {\n    color: ", ";\n    border-bottom: 1px dotted ", ";\n  }\n\n  ", ";\n  ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  margin: 0 0 ", ";\n  padding: ", " ", ";\n  font-size: 15px;\n  box-shadow: ", ";\n  border-radius: ", ";\n  background: ", ";\n  border: 1px solid ", ";\n\n  a:not([role='button']) {\n    color: ", ";\n    border-bottom: 1px dotted ", ";\n  }\n\n  ", ";\n  ", ";\n"])), space_1.default(3), space_1.default(1.5), space_1.default(2), theme.dropShadowLight, theme.borderRadius, theme.backgroundSecondary, theme.border, theme.textColor, theme.textColor, getAlertColorStyles(theme.alert[type]), system && getSystemAlertColorStyles(theme.alert[type]));
};
exports.alertStyles = alertStyles;
var StyledTextBlock = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  line-height: 1.5;\n  position: relative;\n  margin-right: auto;\n"], ["\n  line-height: 1.5;\n  position: relative;\n  margin-right: auto;\n"])));
var MessageContainer = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  width: 100%;\n"], ["\n  display: flex;\n  width: 100%;\n"])));
var ExpandContainer = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(", ", 1fr) 30fr 1fr;\n  grid-template-areas: '. details details';\n  padding: ", " 0;\n"], ["\n  display: grid;\n  grid-template-columns: minmax(", ", 1fr) 30fr 1fr;\n  grid-template-areas: '. details details';\n  padding: ", " 0;\n"])), space_1.default(4), space_1.default(1.5));
var DetailsContainer = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  grid-area: details;\n"], ["\n  grid-area: details;\n"])));
var ExpandIcon = styled_1.default(function (props) { return (<IconWrapper {...props}>{<icons_1.IconChevron size="md"/>}</IconWrapper>); })(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  transform: ", ";\n  cursor: pointer;\n  justify-self: flex-end;\n"], ["\n  transform: ", ";\n  cursor: pointer;\n  justify-self: flex-end;\n"])), function (props) { return (props.isExpanded ? 'rotate(0deg)' : 'rotate(180deg)'); });
var Alert = styled_1.default(function (_a) {
    var type = _a.type, icon = _a.icon, children = _a.children, className = _a.className, expand = _a.expand, expandIcon = _a.expandIcon, onExpandIconClick = _a.onExpandIconClick, _system = _a.system, // don't forward to `div`
    props = tslib_1.__rest(_a, ["type", "icon", "children", "className", "expand", "expandIcon", "onExpandIconClick", "system"]);
    var _b = tslib_1.__read(react_1.useState(false), 2), isExpanded = _b[0], setIsExpanded = _b[1];
    var showExpand = expand && expand.length;
    var showExpandItems = showExpand && isExpanded;
    var handleOnExpandIconClick = onExpandIconClick ? onExpandIconClick : setIsExpanded;
    return (<div className={classnames_1.default(type ? "ref-" + type : '', className)} {...props}>
        <MessageContainer>
          {icon && <IconWrapper>{icon}</IconWrapper>}
          <StyledTextBlock>{children}</StyledTextBlock>
          {showExpand && (<div onClick={function () { return handleOnExpandIconClick(!isExpanded); }}>
              {expandIcon || <ExpandIcon isExpanded={isExpanded}/>}
            </div>)}
        </MessageContainer>
        {showExpandItems && (<ExpandContainer>
            <DetailsContainer>{(expand || []).map(function (item) { return item; })}</DetailsContainer>
          </ExpandContainer>)}
      </div>);
})(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), alertStyles);
Alert.defaultProps = {
    type: DEFAULT_TYPE,
};
exports.default = Alert;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=alert.jsx.map