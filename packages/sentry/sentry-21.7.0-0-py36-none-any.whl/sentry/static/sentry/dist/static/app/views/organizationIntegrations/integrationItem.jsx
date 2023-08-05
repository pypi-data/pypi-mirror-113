Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationIcon_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationIcon"));
var IntegrationItem = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationItem, _super);
    function IntegrationItem() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IntegrationItem.prototype.render = function () {
        var _a = this.props, integration = _a.integration, compact = _a.compact;
        return (<Flex>
        <div>
          <integrationIcon_1.default size={compact ? 22 : 32} integration={integration}/>
        </div>
        <Labels compact={compact}>
          <IntegrationName data-test-id="integration-name">
            {integration.name}
          </IntegrationName>
          <DomainName compact={compact}>{integration.domainName}</DomainName>
        </Labels>
      </Flex>);
    };
    IntegrationItem.defaultProps = {
        compact: false,
    };
    return IntegrationItem;
}(react_1.Component));
exports.default = IntegrationItem;
var Flex = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Labels = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  box-sizing: border-box;\n  display: flex;\n  ", ";\n  flex-direction: ", ";\n  padding-left: ", ";\n  min-width: 0;\n  justify-content: center;\n"], ["\n  box-sizing: border-box;\n  display: flex;\n  ", ";\n  flex-direction: ", ";\n  padding-left: ", ";\n  min-width: 0;\n  justify-content: center;\n"])), function (p) { return (p.compact ? 'align-items: center;' : ''); }, function (p) { return (p.compact ? 'row' : 'column'); }, space_1.default(1));
var IntegrationName = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: 1.6rem;\n"], ["\n  font-size: 1.6rem;\n"])));
// Not using the overflowEllipsis style import here
// as it sets width 100% which causes layout issues in the
// integration list.
var DomainName = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-left: ", ";\n  margin-top: ", ";\n  font-size: 1.4rem;\n  line-height: 1.2;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  color: ", ";\n  margin-left: ", ";\n  margin-top: ", ";\n  font-size: 1.4rem;\n  line-height: 1.2;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return (p.compact ? p.theme.gray200 : p.theme.gray400); }, function (p) { return (p.compact ? space_1.default(1) : 'inherit'); }, function (p) { return (!p.compact ? space_1.default(0.25) : 'inherit'); });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=integrationItem.jsx.map