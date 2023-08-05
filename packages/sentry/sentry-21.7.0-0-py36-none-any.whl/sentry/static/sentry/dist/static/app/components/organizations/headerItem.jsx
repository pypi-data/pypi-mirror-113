Object.defineProperty(exports, "__esModule", { value: true });
exports.SettingsIconLink = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var HeaderItem = /** @class */ (function (_super) {
    tslib_1.__extends(HeaderItem, _super);
    function HeaderItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClear = function (e) {
            var _a, _b;
            e.stopPropagation();
            (_b = (_a = _this.props).onClear) === null || _b === void 0 ? void 0 : _b.call(_a);
        };
        return _this;
    }
    HeaderItem.prototype.render = function () {
        var _a = this.props, children = _a.children, isOpen = _a.isOpen, hasSelected = _a.hasSelected, allowClear = _a.allowClear, icon = _a.icon, locked = _a.locked, lockedMessage = _a.lockedMessage, settingsLink = _a.settingsLink, hint = _a.hint, loading = _a.loading, forwardRef = _a.forwardRef, props = tslib_1.__rest(_a, ["children", "isOpen", "hasSelected", "allowClear", "icon", "locked", "lockedMessage", "settingsLink", "hint", "loading", "forwardRef"]);
        var textColorProps = {
            locked: locked,
            isOpen: isOpen,
            hasSelected: hasSelected,
        };
        return (<StyledHeaderItem ref={forwardRef} loading={!!loading} {...omit_1.default(props, 'onClear')} {...textColorProps}>
        <IconContainer {...textColorProps}>{icon}</IconContainer>
        <Content>
          <StyledContent>{children}</StyledContent>

          {settingsLink && (<exports.SettingsIconLink to={settingsLink}>
              <icons_1.IconSettings />
            </exports.SettingsIconLink>)}
        </Content>
        {hint && (<Hint>
            <tooltip_1.default title={hint} position="bottom">
              <icons_1.IconInfo size="sm"/>
            </tooltip_1.default>
          </Hint>)}
        {hasSelected && !locked && allowClear && (<StyledClose {...textColorProps} onClick={this.handleClear}/>)}
        {!locked && !loading && (<ChevronWrapper>
            <StyledChevron isOpen={!!isOpen} direction={isOpen ? 'up' : 'down'} size="sm"/>
          </ChevronWrapper>)}
        {locked && (<tooltip_1.default title={lockedMessage || locale_1.t('This selection is locked')} position="bottom">
            <StyledLock color="gray300"/>
          </tooltip_1.default>)}
      </StyledHeaderItem>);
    };
    HeaderItem.defaultProps = {
        allowClear: true,
    };
    return HeaderItem;
}(React.Component));
// Infer props here because of styled/theme
var getColor = function (p) {
    if (p.locked) {
        return p.theme.gray300;
    }
    return p.isOpen || p.hasSelected ? p.theme.textColor : p.theme.gray300;
};
var StyledHeaderItem = styled_1.default('div', {
    shouldForwardProp: function (p) { return typeof p === 'string' && is_prop_valid_1.default(p) && p !== 'loading'; },
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  padding: 0 ", ";\n  align-items: center;\n  cursor: ", ";\n  color: ", ";\n  transition: 0.1s color;\n  user-select: none;\n"], ["\n  display: flex;\n  padding: 0 ", ";\n  align-items: center;\n  cursor: ", ";\n  color: ", ";\n  transition: 0.1s color;\n  user-select: none;\n"])), space_1.default(4), function (p) { return (p.loading ? 'progress' : p.locked ? 'text' : 'pointer'); }, getColor);
var Content = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  white-space: nowrap;\n  overflow: hidden;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  flex: 1;\n  white-space: nowrap;\n  overflow: hidden;\n  margin-right: ", ";\n"])), space_1.default(1.5));
var StyledContent = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])));
var IconContainer = styled_1.default('span', { shouldForwardProp: is_prop_valid_1.default })(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-right: ", ";\n  display: flex;\n  font-size: ", ";\n"], ["\n  color: ", ";\n  margin-right: ", ";\n  display: flex;\n  font-size: ", ";\n"])), getColor, space_1.default(1.5), function (p) { return p.theme.fontSizeMedium; });
var Hint = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  top: ", ";\n  margin-right: ", ";\n"], ["\n  position: relative;\n  top: ", ";\n  margin-right: ", ";\n"])), space_1.default(0.25), space_1.default(1));
var StyledClose = styled_1.default(icons_1.IconClose, { shouldForwardProp: is_prop_valid_1.default })(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  height: ", ";\n  width: ", ";\n  stroke-width: 1.5;\n  padding: ", ";\n  box-sizing: content-box;\n  margin: -", " 0px -", " -", ";\n"], ["\n  color: ", ";\n  height: ", ";\n  width: ", ";\n  stroke-width: 1.5;\n  padding: ", ";\n  box-sizing: content-box;\n  margin: -", " 0px -", " -", ";\n"])), getColor, space_1.default(1.5), space_1.default(1.5), space_1.default(1), space_1.default(1), space_1.default(1), space_1.default(1));
var ChevronWrapper = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  width: ", ";\n  height: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  width: ", ";\n  height: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])), space_1.default(2), space_1.default(2));
var StyledChevron = styled_1.default(icons_1.IconChevron, { shouldForwardProp: is_prop_valid_1.default })(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), getColor);
exports.SettingsIconLink = styled_1.default(react_router_1.Link)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  align-items: center;\n  display: inline-flex;\n  justify-content: space-between;\n  margin-right: ", ";\n  margin-left: ", ";\n  transition: 0.5s opacity ease-out;\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  align-items: center;\n  display: inline-flex;\n  justify-content: space-between;\n  margin-right: ", ";\n  margin-left: ", ";\n  transition: 0.5s opacity ease-out;\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, space_1.default(1.5), space_1.default(1.0), function (p) { return p.theme.textColor; });
var StyledLock = styled_1.default(icons_1.IconLock)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  stroke-width: 1.5;\n"], ["\n  margin-top: ", ";\n  stroke-width: 1.5;\n"])), space_1.default(0.75));
exports.default = React.forwardRef(function (props, ref) { return (<HeaderItem forwardRef={ref} {...props}/>); });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=headerItem.jsx.map