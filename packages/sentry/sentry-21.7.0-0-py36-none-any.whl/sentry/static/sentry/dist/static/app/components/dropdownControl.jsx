Object.defineProperty(exports, "__esModule", { value: true });
exports.Content = exports.DropdownItem = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dropdownBubble_1 = tslib_1.__importDefault(require("app/components/dropdownBubble"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
/*
 * A higher level dropdown component that helps with building complete dropdowns
 * including the button + menu options. Use the `button` or `label` prop to set
 * the button content and `children` to provide menu options.
 */
var DropdownControl = /** @class */ (function (_super) {
    tslib_1.__extends(DropdownControl, _super);
    function DropdownControl() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DropdownControl.prototype.renderButton = function (isOpen, getActorProps) {
        var _a = this.props, label = _a.label, button = _a.button, buttonProps = _a.buttonProps, buttonTooltipTitle = _a.buttonTooltipTitle, priority = _a.priority;
        if (button) {
            return button({ isOpen: isOpen, getActorProps: getActorProps });
        }
        if (buttonTooltipTitle && !isOpen) {
            return (<tooltip_1.default containerDisplayMode="inline-flex" position="top" title={buttonTooltipTitle}>
          <StyledDropdownButton priority={priority} {...getActorProps(buttonProps)} isOpen={isOpen}>
            {label}
          </StyledDropdownButton>
        </tooltip_1.default>);
        }
        return (<StyledDropdownButton priority={priority} {...getActorProps(buttonProps)} isOpen={isOpen}>
        {label}
      </StyledDropdownButton>);
    };
    DropdownControl.prototype.renderChildren = function (isOpen, getMenuProps) {
        var _a = this.props, children = _a.children, alignRight = _a.alignRight, menuWidth = _a.menuWidth, blendWithActor = _a.blendWithActor, priority = _a.priority;
        if (typeof children === 'function') {
            return children({ isOpen: isOpen, getMenuProps: getMenuProps });
        }
        var alignMenu = alignRight ? 'right' : 'left';
        return (<Content {...getMenuProps()} priority={priority} alignMenu={alignMenu} width={menuWidth} isOpen={isOpen} blendWithActor={blendWithActor} blendCorner>
        {children}
      </Content>);
    };
    DropdownControl.prototype.render = function () {
        var _this = this;
        var _a = this.props, alwaysRenderMenu = _a.alwaysRenderMenu, className = _a.className;
        return (<Container className={className}>
        <dropdownMenu_1.default alwaysRenderMenu={alwaysRenderMenu}>
          {function (_a) {
                var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps, getActorProps = _a.getActorProps;
                return (<React.Fragment>
              {_this.renderButton(isOpen, getActorProps)}
              {_this.renderChildren(isOpen, getMenuProps)}
            </React.Fragment>);
            }}
        </dropdownMenu_1.default>
      </Container>);
    };
    DropdownControl.defaultProps = {
        alwaysRenderMenu: true,
        menuWidth: '100%',
    };
    return DropdownControl;
}(React.Component));
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n"], ["\n  display: inline-block;\n  position: relative;\n"])));
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  z-index: ", ";\n  white-space: nowrap;\n"], ["\n  z-index: ", ";\n  white-space: nowrap;\n"])), function (p) { return p.theme.zIndex.dropdownAutocomplete.actor; });
var Content = styled_1.default(dropdownBubble_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: ", ";\n  border-color: ", ";\n"], ["\n  display: ", ";\n  border-color: ", ";\n"])), function (p) { return (p.isOpen ? 'block' : 'none'); }, function (p) { return p.theme.button[p.priority || 'form'].border; });
exports.Content = Content;
var DropdownItem = styled_1.default(menuItem_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
exports.DropdownItem = DropdownItem;
exports.default = DropdownControl;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=dropdownControl.jsx.map