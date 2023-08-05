Object.defineProperty(exports, "__esModule", { value: true });
exports.Icon = exports.ButtonLabel = exports.StyledButton = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var mergeRefs_1 = tslib_1.__importDefault(require("app/utils/mergeRefs"));
var BaseButton = /** @class */ (function (_super) {
    tslib_1.__extends(BaseButton, _super);
    function BaseButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Intercept onClick and propagate
        _this.handleClick = function (e) {
            var _a = _this.props, disabled = _a.disabled, busy = _a.busy, onClick = _a.onClick;
            // Don't allow clicks when disabled or busy
            if (disabled || busy) {
                e.preventDefault();
                e.stopPropagation();
                return;
            }
            if (typeof onClick !== 'function') {
                return;
            }
            onClick(e);
        };
        _this.getUrl = function (prop) {
            return _this.props.disabled ? undefined : prop;
        };
        return _this;
    }
    BaseButton.prototype.render = function () {
        var _a = this.props, size = _a.size, to = _a.to, href = _a.href, title = _a.title, icon = _a.icon, children = _a.children, label = _a.label, borderless = _a.borderless, align = _a.align, priority = _a.priority, disabled = _a.disabled, tooltipProps = _a.tooltipProps, 
        // destructure from `buttonProps`
        // not necessary, but just in case someone re-orders props
        _onClick = _a.onClick, buttonProps = tslib_1.__rest(_a, ["size", "to", "href", "title", "icon", "children", "label", "borderless", "align", "priority", "disabled", "tooltipProps", "onClick"]);
        // For `aria-label`
        var screenReaderLabel = label || (typeof children === 'string' ? children : undefined);
        // Buttons come in 4 flavors: <Link>, <ExternalLink>, <a>, and <button>.
        // Let's use props to determine which to serve up, so we don't have to think about it.
        // *Note* you must still handle tabindex manually.
        var button = (<StyledButton aria-label={screenReaderLabel} aria-disabled={disabled} disabled={disabled} to={this.getUrl(to)} href={this.getUrl(href)} size={size} priority={priority} borderless={borderless} {...buttonProps} onClick={this.handleClick} role="button">
        <ButtonLabel align={align} size={size} priority={priority} borderless={borderless}>
          {icon && (<Icon size={size} hasChildren={!!children}>
              {icon}
            </Icon>)}
          {children}
        </ButtonLabel>
      </StyledButton>);
        // Doing this instead of using `Tooltip`'s `disabled` prop so that we can minimize snapshot nesting
        if (title) {
            return (<tooltip_1.default skipWrapper {...tooltipProps} title={title}>
          {button}
        </tooltip_1.default>);
        }
        return button;
    };
    BaseButton.defaultProps = {
        disabled: false,
        align: 'center',
    };
    return BaseButton;
}(React.Component));
var Button = React.forwardRef(function (props, ref) { return (<BaseButton forwardRef={ref} {...props}/>); });
Button.displayName = 'Button';
exports.default = Button;
var getFontSize = function (_a) {
    var size = _a.size, priority = _a.priority, theme = _a.theme;
    if (priority === 'link') {
        return 'inherit';
    }
    switch (size) {
        case 'xsmall':
        case 'small':
            return theme.fontSizeSmall;
        default:
            return theme.fontSizeMedium;
    }
};
var getFontWeight = function (_a) {
    var priority = _a.priority, borderless = _a.borderless;
    return "font-weight: " + (priority === 'link' || borderless ? 'inherit' : 600) + ";";
};
var getBoxShadow = function (active) {
    return function (_a) {
        var priority = _a.priority, borderless = _a.borderless, disabled = _a.disabled;
        if (disabled || borderless || priority === 'link') {
            return 'box-shadow: none';
        }
        return "box-shadow: " + (active ? 'inset' : '') + " 0 2px rgba(0, 0, 0, 0.05)";
    };
};
var getColors = function (_a) {
    var priority = _a.priority, disabled = _a.disabled, borderless = _a.borderless, theme = _a.theme;
    var themeName = disabled ? 'disabled' : priority || 'default';
    var _b = theme.button[themeName], color = _b.color, colorActive = _b.colorActive, background = _b.background, backgroundActive = _b.backgroundActive, border = _b.border, borderActive = _b.borderActive, focusShadow = _b.focusShadow;
    return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n    color: ", ";\n    background-color: ", ";\n    border: 1px solid\n      ", ";\n\n    &:hover {\n      color: ", ";\n    }\n\n    &:hover,\n    &:focus,\n    &:active {\n      color: ", ";\n      background: ", ";\n      border-color: ", ";\n    }\n\n    &.focus-visible {\n      ", "\n    }\n  "], ["\n    color: ", ";\n    background-color: ", ";\n    border: 1px solid\n      ", ";\n\n    &:hover {\n      color: ", ";\n    }\n\n    &:hover,\n    &:focus,\n    &:active {\n      color: ", ";\n      background: ", ";\n      border-color: ", ";\n    }\n\n    &.focus-visible {\n      ", "\n    }\n  "])), color, background, priority !== 'link' && !borderless && !!border ? border : 'transparent', color, colorActive || color, backgroundActive, priority !== 'link' && !borderless && (borderActive || border)
        ? borderActive || border
        : 'transparent', focusShadow && "box-shadow: " + focusShadow + " 0 0 0 3px;");
};
var StyledButton = styled_1.default(React.forwardRef(function (_a, forwardRefAlt) {
    // XXX: There may be two forwarded refs here, one potentially passed from a
    // wrapped Tooltip, another from callers of Button.
    var forwardRef = _a.forwardRef, _size = _a.size, external = _a.external, to = _a.to, href = _a.href, otherProps = tslib_1.__rest(_a, ["forwardRef", "size", "external", "to", "href"]);
    var ref = mergeRefs_1.default([forwardRef, forwardRefAlt]);
    // only pass down title to child element if it is a string
    var title = otherProps.title, props = tslib_1.__rest(otherProps, ["title"]);
    if (typeof title === 'string') {
        props[title] = title;
    }
    // Get component to use based on existence of `to` or `href` properties
    // Can be react-router `Link`, `a`, or `button`
    if (to) {
        return <react_router_1.Link ref={ref} to={to} {...props}/>;
    }
    if (!href) {
        return <button ref={ref} {...props}/>;
    }
    if (external && href) {
        return <externalLink_1.default ref={ref} href={href} {...props}/>;
    }
    return <a ref={ref} {...props} href={href}/>;
}), {
    shouldForwardProp: function (prop) {
        return prop === 'forwardRef' ||
            prop === 'external' ||
            (typeof prop === 'string' && is_prop_valid_1.default(prop) && prop !== 'disabled');
    },
})(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  line-height: 1;\n  border-radius: ", ";\n  padding: 0;\n  text-transform: none;\n  ", ";\n  font-size: ", ";\n  ", ";\n  ", ";\n  cursor: ", ";\n  opacity: ", ";\n\n  &:active {\n    ", ";\n  }\n  &:focus {\n    outline: none;\n  }\n\n  ", ";\n"], ["\n  display: inline-block;\n  line-height: 1;\n  border-radius: ", ";\n  padding: 0;\n  text-transform: none;\n  ", ";\n  font-size: ", ";\n  ", ";\n  ", ";\n  cursor: ", ";\n  opacity: ", ";\n\n  &:active {\n    ", ";\n  }\n  &:focus {\n    outline: none;\n  }\n\n  ", ";\n"])), function (p) { return p.theme.button.borderRadius; }, getFontWeight, getFontSize, getColors, getBoxShadow(false), function (p) { return (p.disabled ? 'not-allowed' : 'pointer'); }, function (p) { return (p.busy || p.disabled) && '0.65'; }, getBoxShadow(true), function (p) { return (p.borderless || p.priority === 'link') && 'border-color: transparent'; });
exports.StyledButton = StyledButton;
/**
 * Get label padding determined by size
 */
var getLabelPadding = function (_a) {
    var size = _a.size, priority = _a.priority;
    if (priority === 'link') {
        return '0';
    }
    switch (size) {
        case 'zero':
            return '0';
        case 'xsmall':
            return '5px 8px';
        case 'small':
            return '9px 12px';
        default:
            return '12px 16px';
    }
};
var buttonLabelPropKeys = ['size', 'priority', 'borderless', 'align'];
var ButtonLabel = styled_1.default('span', {
    shouldForwardProp: function (prop) {
        return typeof prop === 'string' && is_prop_valid_1.default(prop) && !buttonLabelPropKeys.includes(prop);
    },
})(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  justify-content: ", ";\n  padding: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  justify-content: ", ";\n  padding: ", ";\n"])), function (p) { return p.align; }, getLabelPadding);
exports.ButtonLabel = ButtonLabel;
var getIconMargin = function (_a) {
    var size = _a.size, hasChildren = _a.hasChildren;
    // If button is only an icon, then it shouldn't have margin
    if (!hasChildren) {
        return '0';
    }
    return size && size.endsWith('small') ? '6px' : '8px';
};
var Icon = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n  height: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n  height: ", ";\n"])), getIconMargin, getFontSize);
exports.Icon = Icon;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=button.jsx.map