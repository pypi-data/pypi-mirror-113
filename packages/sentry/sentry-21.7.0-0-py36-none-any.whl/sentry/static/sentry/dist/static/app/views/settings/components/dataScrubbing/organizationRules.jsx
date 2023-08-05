Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var rules_1 = tslib_1.__importDefault(require("./rules"));
var OrganizationRules = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationRules, _super);
    function OrganizationRules() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isCollapsed: true,
        };
        _this.rulesRef = react_1.createRef();
        _this.handleToggleCollapsed = function () {
            _this.setState(function (prevState) { return ({
                isCollapsed: !prevState.isCollapsed,
            }); });
        };
        return _this;
    }
    OrganizationRules.prototype.componentDidUpdate = function () {
        this.loadContentHeight();
    };
    OrganizationRules.prototype.loadContentHeight = function () {
        var _a;
        if (!this.state.contentHeight) {
            var contentHeight = (_a = this.rulesRef.current) === null || _a === void 0 ? void 0 : _a.offsetHeight;
            if (contentHeight) {
                this.setState({ contentHeight: contentHeight + "px" });
            }
        }
    };
    OrganizationRules.prototype.render = function () {
        var rules = this.props.rules;
        var _a = this.state, isCollapsed = _a.isCollapsed, contentHeight = _a.contentHeight;
        if (rules.length === 0) {
            return (<Wrapper>
          {locale_1.t('There are no data scrubbing rules at the organization level')}
        </Wrapper>);
        }
        return (<Wrapper isCollapsed={isCollapsed} contentHeight={contentHeight}>
        <Header onClick={this.handleToggleCollapsed}>
          <div>{locale_1.t('Organization Rules')}</div>
          <button_1.default title={isCollapsed
                ? locale_1.t('Expand Organization Rules')
                : locale_1.t('Collapse Organization Rules')} icon={<icons_1.IconChevron size="xs" direction={isCollapsed ? 'down' : 'up'}/>} size="xsmall"/>
        </Header>
        <Content>
          <rules_1.default rules={rules} ref={this.rulesRef} disabled/>
        </Content>
      </Wrapper>);
    };
    return OrganizationRules;
}(react_1.Component));
exports.default = OrganizationRules;
var Content = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;\n  height: 0;\n  overflow: hidden;\n"], ["\n  transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;\n  height: 0;\n  overflow: hidden;\n"])));
var Header = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  cursor: pointer;\n  display: grid;\n  grid-template-columns: 1fr auto;\n  align-items: center;\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n"], ["\n  cursor: pointer;\n  display: grid;\n  grid-template-columns: 1fr auto;\n  align-items: center;\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n"])), function (p) { return p.theme.border; }, space_1.default(1), space_1.default(2));
var Wrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  background: ", ";\n  ", ";\n  ", ";\n  ", "\n"], ["\n  color: ", ";\n  background: ", ";\n  ", ";\n  ", ";\n  ", "\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return !p.contentHeight && "padding: " + space_1.default(1) + " " + space_1.default(2); }, function (p) { return !p.isCollapsed && " border-bottom: 1px solid " + p.theme.border; }, function (p) {
    return !p.isCollapsed &&
        p.contentHeight &&
        "\n      " + Content + " {\n        height: " + p.contentHeight + ";\n      }\n    ";
});
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=organizationRules.jsx.map