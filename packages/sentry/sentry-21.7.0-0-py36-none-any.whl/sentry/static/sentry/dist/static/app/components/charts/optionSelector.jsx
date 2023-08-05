Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var styles_1 = require("app/components/charts/styles");
var dropdownBubble_1 = tslib_1.__importDefault(require("app/components/dropdownBubble"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var dropdownControl_1 = require("app/components/dropdownControl");
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var truncate_1 = tslib_1.__importDefault(require("app/components/truncate"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var defaultProps = {
    menuWidth: 'auto',
};
var OptionSelector = /** @class */ (function (_super) {
    tslib_1.__extends(OptionSelector, _super);
    function OptionSelector() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.menuContainerRef = react_1.createRef();
        return _this;
    }
    OptionSelector.prototype.componentDidMount = function () {
        this.setMenuContainerWidth();
    };
    OptionSelector.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        return !isEqual_1.default(nextProps, this.props) || !isEqual_1.default(nextState, this.state);
    };
    OptionSelector.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.selected !== this.props.selected) {
            this.setMenuContainerWidth();
        }
    };
    OptionSelector.prototype.setMenuContainerWidth = function () {
        var _a, _b;
        var menuContainerWidth = (_b = (_a = this.menuContainerRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetWidth;
        if (menuContainerWidth) {
            this.setState({ menuContainerWidth: menuContainerWidth });
        }
    };
    OptionSelector.prototype.render = function () {
        var menuContainerWidth = this.state.menuContainerWidth;
        var _a = this.props, options = _a.options, onChange = _a.onChange, selected = _a.selected, title = _a.title, menuWidth = _a.menuWidth;
        var selectedOption = options.find(function (opt) { return selected === opt.value; }) || options[0];
        return (<styles_1.InlineContainer>
        <styles_1.SectionHeading>{title}</styles_1.SectionHeading>
        <MenuContainer ref={this.menuContainerRef}>
          <dropdownMenu_1.default alwaysRenderMenu={false}>
            {function (_a) {
                var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps, getActorProps = _a.getActorProps;
                return (<react_1.Fragment>
                <StyledDropdownButton {...getActorProps()} size="zero" isOpen={isOpen}>
                  <TruncatedLabel>{String(selectedOption.label)}</TruncatedLabel>
                </StyledDropdownButton>
                <StyledDropdownBubble {...getMenuProps()} alignMenu="right" width={menuWidth} minWidth={menuContainerWidth} isOpen={isOpen} blendWithActor={false} blendCorner>
                  {options.map(function (opt) { return (<StyledDropdownItem key={opt.value} onSelect={onChange} eventKey={opt.value} disabled={opt.disabled} isActive={selected === opt.value} data-test-id={"option-" + opt.value}>
                      <tooltip_1.default title={opt.tooltip} containerDisplayMode="inline">
                        <StyledTruncate isActive={selected === opt.value} value={String(opt.label)} maxLength={60} expandDirection="left"/>
                      </tooltip_1.default>
                    </StyledDropdownItem>); })}
                </StyledDropdownBubble>
              </react_1.Fragment>);
            }}
          </dropdownMenu_1.default>
        </MenuContainer>
      </styles_1.InlineContainer>);
    };
    OptionSelector.defaultProps = defaultProps;
    return OptionSelector;
}(react_1.Component));
var TruncatedLabel = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  max-width: 400px;\n"], ["\n  ", ";\n  max-width: 400px;\n"])), overflowEllipsis_1.default);
var StyledTruncate = styled_1.default(truncate_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  & span {\n    ", "\n  }\n"], ["\n  & span {\n    ", "\n  }\n"])), function (p) {
    return p.isActive &&
        "\n      color: " + p.theme.white + ";\n      background: " + p.theme.active + ";\n      border: none;\n    ";
});
var MenuContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n"], ["\n  display: inline-block;\n  position: relative;\n"])));
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  font-weight: normal;\n  z-index: ", ";\n"], ["\n  padding: ", " ", ";\n  font-weight: normal;\n  z-index: ", ";\n"])), space_1.default(1), space_1.default(2), function (p) { return (p.isOpen ? p.theme.zIndex.dropdownAutocomplete.actor : 'auto'); });
var StyledDropdownBubble = styled_1.default(dropdownBubble_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: ", ";\n  overflow: visible;\n  ", ";\n"], ["\n  display: ", ";\n  overflow: visible;\n  ", ";\n"])), function (p) { return (p.isOpen ? 'block' : 'none'); }, function (p) {
    return p.minWidth && p.width === 'auto' && "min-width: calc(" + p.minWidth + "px + " + space_1.default(3) + ")";
});
var StyledDropdownItem = styled_1.default(dropdownControl_1.DropdownItem)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  line-height: ", ";\n  white-space: nowrap;\n"], ["\n  line-height: ", ";\n  white-space: nowrap;\n"])), function (p) { return p.theme.text.lineHeightBody; });
exports.default = OptionSelector;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=optionSelector.jsx.map