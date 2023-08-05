Object.defineProperty(exports, "__esModule", { value: true });
exports.Background = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var TAG_HEIGHT = '20px';
function Tag(_a) {
    var _b = _a.type, type = _b === void 0 ? 'default' : _b, icon = _a.icon, tooltipText = _a.tooltipText, to = _a.to, onClick = _a.onClick, href = _a.href, onDismiss = _a.onDismiss, children = _a.children, _c = _a.textMaxWidth, textMaxWidth = _c === void 0 ? 150 : _c, props = tslib_1.__rest(_a, ["type", "icon", "tooltipText", "to", "onClick", "href", "onDismiss", "children", "textMaxWidth"]);
    var iconsProps = {
        size: '11px',
        color: theme_1.default.tag[type].iconColor,
    };
    var tag = (<tooltip_1.default title={tooltipText} containerDisplayMode="inline-flex">
      <exports.Background type={type}>
        {tagIcon()}

        <Text type={type} maxWidth={textMaxWidth}>
          {children}
        </Text>

        {utils_1.defined(onDismiss) && (<DismissButton onClick={handleDismiss} size="zero" priority="link" label={locale_1.t('Dismiss')}>
            <icons_1.IconClose isCircled {...iconsProps}/>
          </DismissButton>)}
      </exports.Background>
    </tooltip_1.default>);
    function handleDismiss(event) {
        event.preventDefault();
        onDismiss === null || onDismiss === void 0 ? void 0 : onDismiss();
    }
    function tagIcon() {
        if (React.isValidElement(icon)) {
            return <IconWrapper>{React.cloneElement(icon, tslib_1.__assign({}, iconsProps))}</IconWrapper>;
        }
        if ((utils_1.defined(href) || utils_1.defined(to)) && icon === undefined) {
            return (<IconWrapper>
          <icons_1.IconOpen {...iconsProps}/>
        </IconWrapper>);
        }
        return null;
    }
    function tagWithParent() {
        if (utils_1.defined(href)) {
            return <externalLink_1.default href={href}>{tag}</externalLink_1.default>;
        }
        if (utils_1.defined(to) && utils_1.defined(onClick)) {
            return (<link_1.default to={to} onClick={onClick}>
          {tag}
        </link_1.default>);
        }
        else if (utils_1.defined(to)) {
            return <link_1.default to={to}>{tag}</link_1.default>;
        }
        return tag;
    }
    return <TagWrapper {...props}>{tagWithParent()}</TagWrapper>;
}
var TagWrapper = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
exports.Background = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-flex;\n  align-items: center;\n  height: ", ";\n  border-radius: ", ";\n  background-color: ", ";\n  padding: 0 ", ";\n"], ["\n  display: inline-flex;\n  align-items: center;\n  height: ", ";\n  border-radius: ", ";\n  background-color: ", ";\n  padding: 0 ", ";\n"])), TAG_HEIGHT, TAG_HEIGHT, function (p) { return p.theme.tag[p.type].background; }, space_1.default(1));
var IconWrapper = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n  display: inline-flex;\n"], ["\n  margin-right: ", ";\n  display: inline-flex;\n"])), space_1.default(0.5));
var Text = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  max-width: ", "px;\n  overflow: hidden;\n  white-space: nowrap;\n  text-overflow: ellipsis;\n  line-height: ", ";\n"], ["\n  color: ", ";\n  max-width: ", "px;\n  overflow: hidden;\n  white-space: nowrap;\n  text-overflow: ellipsis;\n  line-height: ", ";\n"])), function (p) { return (['black', 'focus'].includes(p.type) ? p.theme.white : p.theme.gray500); }, function (p) { return p.maxWidth; }, TAG_HEIGHT);
var DismissButton = styled_1.default(button_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  border: none;\n"], ["\n  margin-left: ", ";\n  border: none;\n"])), space_1.default(0.5));
exports.default = Tag;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=tag.jsx.map